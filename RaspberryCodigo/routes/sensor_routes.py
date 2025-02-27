from flask import Blueprint, request, jsonify
from models.sensor_data import get_all_dht11_data

# Crear un Blueprint para las rutas de sensores
sensor_bp = Blueprint('sensor_bp', __name__)

# API para obtener datos de sensores desde la base de datos
@sensor_bp.route('/DhtSensor', methods=['GET'])
def get_dht_sensor_data():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('pageSize', 10))
    data = get_all_dht11_data(page, page_size)
    return jsonify([dict(row) for row in data])
