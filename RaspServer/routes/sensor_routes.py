from flask import Blueprint, request, jsonify
import asyncio
from models.sensor_data import get_all_sht3x_data, get_ideal_params, update_ideal_params
from models.client import client_exists
from mqtt_client import publish_message

# Crear un Blueprint para las rutas de sensores
sensor_bp = Blueprint('sensor_bp', __name__)

# API para obtener datos de sensor sht3x desde la base de datos
@sensor_bp.route('/clients/<client_id>/Sht3xSensor', methods=['GET'])
async def get_sht3x_sensor_data(client_id):
    # Verificar que el cliente existe
    if not await client_exists(client_id):
        return jsonify({"error": "Cliente no encontrado"}), 404
        
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('pageSize', 10))
    data = await get_all_sht3x_data(client_id, page, page_size)
    return jsonify([dict(row) for row in data])

# API para obtener datos de sensor sht3x desde la base de datos sin automatización
@sensor_bp.route('/clients/<client_id>/Sht3xSensorManual', methods=['GET'])
async def get_sht3x_sensor_data_manual(client_id):
    # Verificar que el cliente existe
    if not await client_exists(client_id):
        return jsonify({"error": "Cliente no encontrado"}), 404
        
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('pageSize', 10))
    data = await get_all_sht3x_data(client_id, page, page_size)
    return jsonify([dict(row) for row in data])

# API para obtener parametros ideales
@sensor_bp.route('/clients/<client_id>/IdealParams/<param_type>', methods=['GET'])
async def get_ideal_params_data(client_id, param_type):
    # Verificar que el cliente existe
    if not await client_exists(client_id):
        return jsonify({"error": "Cliente no encontrado"}), 404
        
    params = await get_ideal_params(client_id, param_type)
    if params:
        return jsonify(dict(params))
    else:
        return jsonify({"message": "Parametros no encontrados"}), 404

# API para actualizar parametros ideales
@sensor_bp.route('/clients/<client_id>/IdealParams/<param_type>', methods=['PUT'])
async def update_ideal_params_data(client_id, param_type):
    # Verificar que el cliente existe
    if not await client_exists(client_id):
        return jsonify({"error": "Cliente no encontrado"}), 404
        
    data = request.json
    min_value = data.get('min_value')
    max_value = data.get('max_value')
    await update_ideal_params(client_id, param_type, min_value, max_value)
    return jsonify({"message": "Parametros ideales actualizados exitosamente"}), 200
