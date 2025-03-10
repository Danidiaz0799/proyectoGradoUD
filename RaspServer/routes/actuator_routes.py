from flask import Blueprint, request, jsonify
from mqtt_client import publish_message
from models.event import save_event  # Importar la funcion para guardar eventos
from models.actuator import save_actuator_state, update_actuator_state, get_all_actuators

actuator_bp = Blueprint('actuator_bp', __name__)

# API para encender/apagar la luz del Raspberry
@actuator_bp.route('/Actuator/toggle_light', methods=['POST'])
def toggle_light():
    data = request.get_json()
    state = data.get('state')
    if state is not None:
        publish_message('raspberry/light', str(state).lower())
        save_event(f"Actuador Iluminacion cambiado a {state}", "iluminacion")  # Guardar evento
        update_actuator_state(1, state)  # Actualizar estado del actuador en la base de datos
        return jsonify({"message": "Senal enviada correctamente"}), 200
    else:
        return jsonify({"error": "Datos incompletos"}), 400

# API para encender/apagar el ventilador del Raspberry
@actuator_bp.route('/Actuator/toggle_fan', methods=['POST'])
def toggle_fan():
    data = request.get_json()
    state = data.get('state')
    if state is not None:
        publish_message('raspberry/fan', str(state).lower())
        save_event(f"Actuador Ventilador cambiado a {state}", "ventilador")  # Guardar evento
        update_actuator_state(2, state)
        return jsonify({"message": "Senal enviada correctamente"}), 200
    else:
        return jsonify({"error": "Datos incompletos"}), 400

# API para encender/apagar el humidificador del Raspberry
@actuator_bp.route('/Actuator/toggle_humidifier', methods=['POST'])
def toggle_humidifier():
    data = request.get_json()
    state = data.get('state')
    if state is not None:
        publish_message('raspberry/humidifier', str(state).lower())
        save_event(f"Actuador Humidificador cambiado a {state}", "humidificador")  # Guardar evento
        update_actuator_state(3, state)
        return jsonify({"message": "Senal enviada correctamente"}), 200
    else:
        return jsonify({"error": "Datos incompletos"}), 400

# API para encender/apagar el motor del Raspberry
@actuator_bp.route('/Actuator/toggle_motor', methods=['POST'])
def toggle_motor():
    data = request.get_json()
    state = data.get('state')
    if state is not None:
        publish_message('raspberry/motor', str(state).lower())
        save_event(f"Actuador Motor cambiado a {state}", "motor")  # Guardar evento
        update_actuator_state(4, state)
        return jsonify({"message": "Senal enviada correctamente"}), 200
    else:
        return jsonify({"error": "Datos incompletos"}), 400

# API para obtener actuadores desde la base de datos
@actuator_bp.route('/Actuator', methods=['GET'])
def get_actuators():
    data = get_all_actuators()
    return jsonify([dict(row) for row in data])

# API para agregar un nuevo actuador
@actuator_bp.route('/Actuator', methods=['POST'])
def add_actuator():
    data = request.get_json()
    name = data.get('name')
    state = data.get('state')
    if name and state is not None:
        save_actuator_state(name, state)
        return jsonify({"message": "Actuador agregado correctamente"}), 201
    else:
        return jsonify({"error": "Datos incompletos"}), 400

# API para actualizar el estado de un actuador
@actuator_bp.route('/Actuator/<int:id>', methods=['PUT'])
def update_actuator(id):
    data = request.get_json()
    state = data.get('state')
    if state is not None:
        update_actuator_state(id, state)
        return jsonify({"message": "Estado del actuador actualizado correctamente"}), 200
    else:
        return jsonify({"error": "Datos incompletos"}), 400
