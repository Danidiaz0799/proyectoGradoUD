from flask import Blueprint, request, jsonify
from mqtt_client import publish_message
from models.actuator import save_actuator_state, update_actuator_state, get_all_actuators, get_actuator_by_name
from models.client import client_exists

actuator_bp = Blueprint('actuator_bp', __name__)

# API para encender/apagar la luz del Raspberry
@actuator_bp.route('/clients/<client_id>/Actuator/toggle_light', methods=['POST'])
async def toggle_light(client_id):
    # Verificar que el cliente existe
    if not await client_exists(client_id):
        return jsonify({"error": "Cliente no encontrado"}), 404
        
    data = request.get_json()
    state = data.get('state')
    if state is not None:
        await publish_message(f'clients/{client_id}/light', str(state).lower())
        # Buscar el actuador por nombre
        actuator = await get_actuator_by_name(client_id, "Iluminacion")
        if actuator:
            await update_actuator_state(client_id, actuator['id'], state)
        return jsonify({"message": "Senal enviada correctamente"}), 200
    else:
        return jsonify({"error": "Datos incompletos"}), 400

# API para encender/apagar el ventilador del Raspberry
@actuator_bp.route('/clients/<client_id>/Actuator/toggle_fan', methods=['POST'])
async def toggle_fan(client_id):
    # Verificar que el cliente existe
    if not await client_exists(client_id):
        return jsonify({"error": "Cliente no encontrado"}), 404
        
    data = request.get_json()
    state = data.get('state')
    if state is not None:
        await publish_message(f'clients/{client_id}/fan', str(state).lower())
        # Buscar el actuador por nombre
        actuator = await get_actuator_by_name(client_id, "Ventilacion")
        if actuator:
            await update_actuator_state(client_id, actuator['id'], state)
        return jsonify({"message": "Senal enviada correctamente"}), 200
    else:
        return jsonify({"error": "Datos incompletos"}), 400

# API para encender/apagar el humidificador del Raspberry
@actuator_bp.route('/clients/<client_id>/Actuator/toggle_humidifier', methods=['POST'])
async def toggle_humidifier(client_id):
    # Verificar que el cliente existe
    if not await client_exists(client_id):
        return jsonify({"error": "Cliente no encontrado"}), 404
        
    data = request.get_json()
    state = data.get('state')
    if state is not None:
        await publish_message(f'clients/{client_id}/humidifier', str(state).lower())
        # Buscar el actuador por nombre
        actuator = await get_actuator_by_name(client_id, "Humidificador")
        if actuator:
            await update_actuator_state(client_id, actuator['id'], state)
        return jsonify({"message": "Senal enviada correctamente"}), 200
    else:
        return jsonify({"error": "Datos incompletos"}), 400

# API para encender/apagar el motor del Raspberry
@actuator_bp.route('/clients/<client_id>/Actuator/toggle_motor', methods=['POST'])
async def toggle_motor(client_id):
    # Verificar que el cliente existe
    if not await client_exists(client_id):
        return jsonify({"error": "Cliente no encontrado"}), 404
        
    data = request.get_json()
    state = data.get('state')
    if state is not None:
        await publish_message(f'clients/{client_id}/motor', str(state).lower())
        # Buscar el actuador por nombre
        actuator = await get_actuator_by_name(client_id, "Motor")
        if actuator:
            await update_actuator_state(client_id, actuator['id'], state)
        return jsonify({"message": "Senal enviada correctamente"}), 200
    else:
        return jsonify({"error": "Datos incompletos"}), 400

# API para obtener actuadores desde la base de datos
@actuator_bp.route('/clients/<client_id>/Actuator', methods=['GET'])
async def get_actuators(client_id):
    # Verificar que el cliente existe
    if not await client_exists(client_id):
        return jsonify({"error": "Cliente no encontrado"}), 404
        
    data = await get_all_actuators(client_id)
    return jsonify([dict(row) for row in data])

# API para agregar un nuevo actuador
@actuator_bp.route('/clients/<client_id>/Actuator', methods=['POST'])
async def add_actuator(client_id):
    # Verificar que el cliente existe
    if not await client_exists(client_id):
        return jsonify({"error": "Cliente no encontrado"}), 404
        
    data = request.get_json()
    name = data.get('name')
    state = data.get('state')
    if name and state is not None:
        await save_actuator_state(client_id, name, state)
        return jsonify({"message": "Actuador agregado correctamente"}), 201
    else:
        return jsonify({"error": "Datos incompletos"}), 400

# API para actualizar el estado de un actuador
@actuator_bp.route('/clients/<client_id>/Actuator/<int:id>', methods=['PUT'])
async def update_actuator(client_id, id):
    # Verificar que el cliente existe
    if not await client_exists(client_id):
        return jsonify({"error": "Cliente no encontrado"}), 404
        
    data = request.get_json()
    state = data.get('state')
    if state is not None:
        await update_actuator_state(client_id, id, state)
        return jsonify({"message": "Estado del actuador actualizado correctamente"}), 200
    else:
        return jsonify({"error": "Datos incompletos"}), 400
