from flask import Blueprint, request, jsonify
import asyncio
from models.sensor_data import get_all_sht3x_data, get_all_gy302_data, get_ideal_params, update_ideal_params, get_sensor_data_by_date
from mqtt_client import publish_message

# Crear un Blueprint para las rutas de sensores
sensor_bp = Blueprint('sensor_bp', __name__)

# API para obtener datos de sensor sht3x desde la base de datos
@sensor_bp.route('/Sht3xSensor', methods=['GET'])
async def get_sht3x_sensor_data():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('pageSize', 10))
    data = await get_all_sht3x_data(page, page_size)
    return jsonify([dict(row) for row in data])

# API para obtener datos de sensor sht3x desde la base de datos sin automatización
@sensor_bp.route('/Sht3xSensorManual', methods=['GET'])
async def get_sht3x_sensor_data_manual():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('pageSize', 10))
    data = await get_all_sht3x_data(page, page_size)
    return jsonify([dict(row) for row in data])

# API para obtener datos de sensores GY-302 desde la base de datos
@sensor_bp.route('/Gy302Sensor', methods=['GET'])
async def get_gy302_sensor_data():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('pageSize', 10))
    data = await get_all_gy302_data(page, page_size)
    return jsonify([dict(row) for row in data])

# API para obtener parametros ideales
@sensor_bp.route('/IdealParams/<param_type>', methods=['GET'])
async def get_ideal_params_data(param_type):
    params = await get_ideal_params(param_type)
    if params:
        return jsonify(dict(params))
    else:
        return jsonify({"message": "Parametros no encontrados"}), 404

# API para actualizar parametros ideales
@sensor_bp.route('/IdealParams/<param_type>', methods=['PUT'])
async def update_ideal_params_data(param_type):
    data = request.json
    min_value = data.get('min_value')
    max_value = data.get('max_value')
    await update_ideal_params(param_type, min_value, max_value)
    return jsonify({"message": "Parametros ideales actualizados exitosamente"}), 200

# API para filtrar data de sensores por fecha con paginación
@sensor_bp.route('/SensorData', methods=['GET'])
async def get_sensor_data_by_date_range():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('pageSize', 10))
    if not start_date or not end_date:
        return jsonify({"message": "Por favor, proporcione fecha inicial y fecha final"}), 400
    data = await get_sensor_data_by_date(start_date, end_date, page, page_size)
    return jsonify(data)
