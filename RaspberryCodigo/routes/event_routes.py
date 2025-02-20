from flask import Blueprint, request, jsonify
from models.event import save_event, get_db_connection

event_bp = Blueprint('event_bp', __name__)

# API para obtener eventos desde la base de datos
@event_bp.route('/Event', methods=['GET'])
def get_events():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('pageSize', 10))
    conn = get_db_connection()
    data = conn.execute('SELECT * FROM events ORDER BY timestamp DESC LIMIT ? OFFSET ?',
                        (page_size, (page - 1) * page_size)).fetchall()
    conn.close()
    return jsonify([dict(row) for row in data])

# API para insertar eventos en la base de datos
@event_bp.route('/add_event', methods=['POST'])
def add_event():
    data = request.get_json()
    message = data.get('message')
    if message:
        save_event(message)
        return jsonify({"message": "Evento guardado correctamente"}), 201
    else:
        return jsonify({"error": "Mensaje del evento es requerido"}), 400
