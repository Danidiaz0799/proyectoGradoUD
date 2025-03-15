from flask import Blueprint, request, jsonify
import requests
from models.sensor_data import get_all_sht3x_data, get_all_gy302_data, get_ideal_params, update_ideal_params, get_sensor_data_by_date
from models.actuator import update_actuator_state, get_all_actuators
from mqtt_client import publish_message

# Crear un Blueprint para las rutas de sensores
sensor_bp = Blueprint('sensor_bp', __name__)

def update_actuator_and_log(actuator_id, state, description, topic):
    update_actuator_state(actuator_id, state)
    publish_message(topic, str(state).lower())

# API para obtener datos de sensor sht3x desde la base de datos
@sensor_bp.route('/Sht3xSensor', methods=['GET'])
def get_sht3x_sensor_data():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('pageSize', 10))

    # Obtener parametros ideales
    ideal_temp_params = get_ideal_params('temperatura')
    ideal_humidity_params = get_ideal_params('humedad')

    if not ideal_temp_params or not ideal_humidity_params:
        return jsonify({"message": "No se encontraron parametros ideales"}), 404

    min_temp = ideal_temp_params['min_value']
    max_temp = ideal_temp_params['max_value']
    min_humidity = ideal_humidity_params['min_value']
    max_humidity = ideal_humidity_params['max_value']

    # Obtener datos del sensor
    data = get_all_sht3x_data(page, page_size)

    if data:
        latest_data = dict(data[0])
        latest_temp = latest_data['temperature']
        latest_humidity = latest_data['humidity']

        # Validar temperatura
        if latest_temp < min_temp:
            update_actuator_and_log(1, 'true', "Temperatura baja", 'raspberry/light')
            update_actuator_and_log(2, 'false', "Ventilador apagado", 'raspberry/fan')
        elif latest_temp > max_temp:
            update_actuator_and_log(1, 'false', "Temperatura alta", 'raspberry/light')
            update_actuator_and_log(2, 'true', "Ventilador encendido", 'raspberry/fan')
        else:
            update_actuator_and_log(1, 'false', "Temperatura normal", 'raspberry/light')
            update_actuator_and_log(2, 'false', "Ventilador apagado", 'raspberry/fan')

        # Validar humedad
        if latest_humidity < min_humidity:
            update_actuator_and_log(3, 'true', "Humedad baja", 'raspberry/humidifier')
            update_actuator_and_log(4, 'false', "Motor apagado", 'raspberry/motor')
        elif latest_humidity > max_humidity:
            update_actuator_and_log(3, 'false', "Humedad alta", 'raspberry/humidifier')
            update_actuator_and_log(4, 'true', "Motor encendido", 'raspberry/motor')
        else:
            update_actuator_and_log(3, 'false', "Humedad normal", 'raspberry/humidifier')
            update_actuator_and_log(4, 'false', "Motor apagado", 'raspberry/motor')

    return jsonify([dict(row) for row in data])

# API para obtener datos de sensores GY-302 desde la base de datos
@sensor_bp.route('/Gy302Sensor', methods=['GET'])
def get_gy302_sensor_data():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('pageSize', 10))
    data = get_all_gy302_data(page, page_size)
    return jsonify([dict(row) for row in data])

# API para obtener parametros ideales
@sensor_bp.route('/IdealParams/<param_type>', methods=['GET'])
def get_ideal_params_data(param_type):
    params = get_ideal_params(param_type)
    if params:
        return jsonify(dict(params))
    else:
        return jsonify({"message": "Parametros no encontrados"}), 404

# API para actualizar parametros ideales
@sensor_bp.route('/IdealParams/<param_type>', methods=['PUT'])
def update_ideal_params_data(param_type):
    data = request.json
    min_value = data.get('min_value')
    max_value = data.get('max_value')
    update_ideal_params(param_type, min_value, max_value)
    return jsonify({"message": "Parametros ideales actualizados exitosamente"}), 200

# API para filtrar data de sensores por fecha con paginación
@sensor_bp.route('/SensorData', methods=['GET'])
def get_sensor_data_by_date_range():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('pageSize', 10))
    if not start_date or not end_date:
        return jsonify({"message": "Por favor, proporcione fecha inicial y fecha final"}), 400
    data = get_sensor_data_by_date(start_date, end_date, page, page_size)
    return jsonify(data)
