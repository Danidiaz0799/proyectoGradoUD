from flask import Blueprint, request, jsonify
from models.sensor_data import save_sensor_data, get_db_connection

# Crear un Blueprint para las rutas de sensores
sensor_bp = Blueprint('sensor_bp', __name__)

# API para obtener datos de sensores desde la base de datos
@sensor_bp.route('/DhtSensor', methods=['GET'])
def get_dht_sensor_data():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('pageSize', 10))
    conn = get_db_connection()
    data = conn.execute('SELECT * FROM dht_data ORDER BY timestamp DESC LIMIT ? OFFSET ?',
                        (page_size, (page - 1) * page_size)).fetchall()
    conn.close()
    return jsonify([dict(row) for row in data])

# API para insertar datos de sensores en la base de datos
@sensor_bp.route('/add_sensor_data', methods=['POST'])
def add_sensor_data():
    data = request.get_json()
    temperature = data.get('temperature')
    humidity = data.get('humidity')
    if temperature is not None and humidity is not None:
        save_sensor_data(temperature, humidity)
        return jsonify({"message": "Datos del sensor guardados correctamente"}), 201
    else:
        return jsonify({"error": "Datos incompletos"}), 400
