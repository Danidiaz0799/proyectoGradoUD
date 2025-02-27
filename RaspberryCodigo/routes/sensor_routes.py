from flask import Blueprint, request, jsonify
from models.sensor_data import get_all_dht11_data, get_all_bmp280_data, get_all_gy302_data

# Crear un Blueprint para las rutas de sensores
sensor_bp = Blueprint('sensor_bp', __name__)

# API para obtener datos de sensores DHT11 desde la base de datos
@sensor_bp.route('/DhtSensor', methods=['GET'])
def get_dht_sensor_data():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('pageSize', 10))
    data = get_all_dht11_data(page, page_size)
    return jsonify([dict(row) for row in data])

# API para obtener datos de sensores BMP280 desde la base de datos
@sensor_bp.route('/Bmp280Sensor', methods=['GET'])
def get_bmp280_sensor_data():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('pageSize', 10))
    data = get_all_bmp280_data(page, page_size)
    return jsonify([dict(row) for row in data])

# API para obtener datos de sensores GY-302 desde la base de datos
@sensor_bp.route('/Gy302Sensor', methods=['GET'])
def get_gy302_sensor_data():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('pageSize', 10))
    data = get_all_gy302_data(page, page_size)
    return jsonify([dict(row) for row in data])
