from flask import Blueprint, request, jsonify
from models.event import save_event, get_all_events, update_event

event_bp = Blueprint('event_bp', __name__)

# API para obtener eventos desde la base de datos
@event_bp.route('/Event', methods=['GET'])
def get_events():
    data = get_all_events()
    return jsonify([dict(row) for row in data])

# API para insertar eventos en la base de datos
@event_bp.route('/Event', methods=['POST'])
def add_event():
    data = request.get_json()
    message = data.get('message')
    if message:
        save_event(message)
        return jsonify({"message": "Evento guardado correctamente"}), 201
    else:
        return jsonify({"error": "Mensaje del evento es requerido"}), 400

# API para actualizar un evento en la base de datos
@event_bp.route('/Event/<int:id>', methods=['PUT'])
def update_event_endpoint(id):
    data = request.get_json()
    message = data.get('message')
    if message:
        update_event(id, message)
        return jsonify({"message": "Evento actualizado correctamente"}), 200
    else:
        return jsonify({"error": "Mensaje del evento es requerido"}), 400
