from flask import Blueprint, request, jsonify
from models.event import save_event, get_all_events, update_event, get_events_by_topic, delete_event
from models.client import client_exists

event_bp = Blueprint('event_bp', __name__)

# API para obtener eventos desde la base de datos con paginacion
@event_bp.route('/clients/<client_id>/Event', methods=['GET'])
async def get_events(client_id):
    # Verificar que el cliente existe
    if not await client_exists(client_id):
        return jsonify({"error": "Cliente no encontrado"}), 404
        
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('pageSize', 10))
    data = await get_all_events(client_id, page, page_size)
    return jsonify([dict(row) for row in data])

# API para insertar eventos en la base de datos
@event_bp.route('/clients/<client_id>/Event', methods=['POST'])
async def add_event(client_id):
    # Verificar que el cliente existe
    if not await client_exists(client_id):
        return jsonify({"error": "Cliente no encontrado"}), 404
        
    data = request.get_json()
    message = data.get('message')
    topic = data.get('topic')
    if message and topic:
        await save_event(client_id, message, topic)
        return jsonify({"message": "Evento guardado correctamente"}), 201
    else:
        return jsonify({"error": "Mensaje y topico del evento son requeridos"}), 400

# API para obtener eventos filtrados por tema con paginacion
@event_bp.route('/clients/<client_id>/Event/FilterByTopic', methods=['GET'])
async def get_events_by_topic_endpoint(client_id):
    # Verificar que el cliente existe
    if not await client_exists(client_id):
        return jsonify({"error": "Cliente no encontrado"}), 404
        
    topic = request.args.get('topic')
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('pageSize', 10))
    if topic:
        data = await get_events_by_topic(client_id, topic, page, page_size)
        return jsonify([dict(row) for row in data])
    else:
        return jsonify({"error": "El tema es requerido"}), 400

# API para eliminar un evento por ID
@event_bp.route('/clients/<client_id>/Event/<int:id>', methods=['DELETE'])
async def delete_event_endpoint(client_id, id):
    # Verificar que el cliente existe
    if not await client_exists(client_id):
        return jsonify({"error": "Cliente no encontrado"}), 404
        
    try:
        await delete_event(client_id, id)
        return jsonify({"message": "Evento eliminado correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
