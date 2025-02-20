# -*- coding: utf-8 -*-

from flask import Flask, render_template, jsonify
import paho.mqtt.client as mqtt
import os

app = Flask(__name__)

# Variables globales para almacenar los datos del sensor
temperatura = None
humedad = None

# Función de callback cuando se recibe un mensaje MQTT
def on_message(client, userdata, msg):
    global temperatura, humedad
    try:
        # Decodificar el mensaje en UTF-8 y manejar errores
        data = msg.payload.decode('utf-8', errors='ignore').split(',')
        if len(data) == 2:
            temperatura, humedad = data[0], data[1]  # Separar temperatura y humedad
        print(f'Temperatura: {temperatura}, Humedad: {humedad}')
    except Exception as e:
        print(f'Error al procesar el mensaje: {e}')

# Configuración del cliente MQTT
def connect_mqtt():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect('localhost', 1883, 60)  # Conectarse al broker local de la Raspberry
    client.subscribe('temperatura_humedad')  # Suscribirse al tópico donde el ESP32 publica
    client.loop_start()  # Iniciar el loop en segundo plano para recibir mensajes

# Ruta principal (página de inicio)
@app.route('/')
def index():
    try:
        # Asegurarse de que Flask pueda encontrar la carpeta de plantillas
        current_path = os.path.dirname(os.path.abspath(__file__))
        templates_path = os.path.join(current_path, 'templates')
        if not os.path.exists(templates_path):
            print(f"Directorio de plantillas no encontrado: {templates_path}")
        return render_template('index.html')
    except Exception as e:
        print(f"Error al renderizar el template: {e}")
        return "Error interno en el servidor", 500

# API para enviar datos al frontend
@app.route('/data')
def get_data():
    try:
        return jsonify(temperatura=temperatura, humedad=humedad)
    except Exception as e:
        print(f'Error al enviar datos: {e}')
        return jsonify(temperatura='--', humedad='--')

# Iniciar la aplicación
if __name__ == '__main__':
    connect_mqtt()  # Conectar al broker MQTT
    app.run(host='0.0.0.0', port=5000, debug=True)  # Iniciar el servidor Flask
