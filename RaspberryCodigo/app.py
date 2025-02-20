# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request
from flask_cors import CORS
import paho.mqtt.client as mqtt
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}})

# Variables globales para almacenar los datos del sensor
temperatura = None
humedad = None

# Conectar a la base de datos
def get_db_connection():
    conn = sqlite3.connect('sensor_data.db')
    conn.row_factory = sqlite3.Row
    return conn

# Guardar datos del sensor en la base de datos
def save_sensor_data(temperature, humidity):
    conn = get_db_connection()
    conn.execute('INSERT INTO dht_data (timestamp, temperature, humidity) VALUES (?, ?, ?)',
                    (datetime.now().isoformat(), temperature, humidity))
    conn.commit()
    conn.close()

# Guardar eventos en la base de datos
def save_event(message):
    conn = get_db_connection()
    conn.execute('INSERT INTO events (timestamp, message) VALUES (?, ?)',
                    (datetime.now().isoformat(), message))
    conn.commit()
    conn.close()

# Guardar estado de actuadores en la base de datos
def save_actuator_state(name, state):
    conn = get_db_connection()
    conn.execute('INSERT INTO actuators (timestamp, name, state) VALUES (?, ?, ?)',
                    (datetime.now().isoformat(), name, state))
    conn.commit()
    conn.close()

# Funcion de callback cuando se recibe un mensaje MQTT
def on_message(client, userdata, msg):
    global temperatura, humedad
    try:
        # Decodificar el mensaje en UTF-8 y manejar errores
        data = msg.payload.decode('utf-8', errors='ignore').split(',')
        if len(data) == 2:
            temperatura, humedad = data[0], data[1]  # Separar temperatura y humedad
            save_sensor_data(temperatura, humedad)  # Guardar datos en la base de datos
        print(f'Temperatura: {temperatura}, Humedad: {humedad}')
    except Exception as e:
        print(f'Error al procesar el mensaje: {e}')

# Configuracion del cliente MQTT
def connect_mqtt():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect('localhost', 1883, 60)  # Conectarse al broker local de la Raspberry
    client.subscribe('temperatura_humedad')  # Suscribirse al topico donde el ESP32 publica
    client.loop_start()  # Iniciar el loop en segundo plano para recibir mensajes

# API para enviar datos al frontend
@app.route('/data')
def get_data():
    try:
        return jsonify(temperatura=temperatura, humedad=humedad)
    except Exception as e:
        print(f'Error al enviar datos: {e}')
        return jsonify(temperatura='--', humedad='--')

# API para obtener datos de sensores desde la base de datos
@app.route('/DhtSensor')
def get_dht_sensor_data():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('pageSize', 10))
    conn = get_db_connection()
    data = conn.execute('SELECT * FROM dht_data ORDER BY timestamp DESC LIMIT ? OFFSET ?',
                        (page_size, (page - 1) * page_size)).fetchall()
    conn.close()
    return jsonify([dict(row) for row in data])

# API para obtener eventos desde la base de datos
@app.route('/Event')
def get_events():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('pageSize', 10))
    conn = get_db_connection()
    data = conn.execute('SELECT * FROM events ORDER BY timestamp DESC LIMIT ? OFFSET ?',
                        (page_size, (page - 1) * page_size)).fetchall()
    conn.close()
    return jsonify([dict(row) for row in data])

# API para obtener estados de actuadores desde la base de datos
@app.route('/Actuator')
def get_actuators():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('pageSize', 10))
    conn = get_db_connection()
    data = conn.execute('SELECT * FROM actuators ORDER BY timestamp DESC LIMIT ? OFFSET ?',
                        (page_size, (page - 1) * page_size)).fetchall()
    conn.close()
    return jsonify([dict(row) for row in data])

# API para insertar datos de sensores en la base de datos
@app.route('/add_sensor_data', methods=['POST'])
def add_sensor_data():
    data = request.get_json()
    temperature = data.get('temperature')
    humidity = data.get('humidity')
    if temperature is not None and humidity is not None:
        save_sensor_data(temperature, humidity)
        return jsonify({"message": "Datos del sensor guardados correctamente"}), 201
    else:
        return jsonify({"error": "Datos incompletos"}), 400

# API para insertar eventos en la base de datos
@app.route('/add_event', methods=['POST'])
def add_event():
    data = request.get_json()
    message = data.get('message')
    if message:
        save_event(message)
        return jsonify({"message": "Evento guardado correctamente"}), 201
    else:
        return jsonify({"error": "Mensaje del evento es requerido"}), 400

# API para insertar estados de actuadores en la base de datos
@app.route('/add_actuator_state', methods=['POST'])
def add_actuator_state():
    data = request.get_json()
    name = data.get('name')
    state = data.get('state')
    if name and state is not None:
        save_actuator_state(name, state)
        return jsonify({"message": "Estado del actuador guardado correctamente"}), 201
    else:
        return jsonify({"error": "Datos incompletos"}), 400

# Iniciar la aplicacion
if __name__ == '__main__':
    connect_mqtt()  # Conectar al broker MQTT
    app.run(host='0.0.0.0', port=5000, debug=True)  # Iniciar el servidor Flask
