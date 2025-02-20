from flask import Blueprint, request, jsonify
from models.actuator import save_actuator_state, get_db_connection

actuator_bp = Blueprint('actuator_bp', __name__)

# API para obtener estados de actuadores desde la base de datos
@actuator_bp.route('/Actuator', methods=['GET'])
def get_actuators():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('pageSize', 10))
    conn = get_db_connection()
    data = conn.execute('SELECT * FROM actuators ORDER BY timestamp DESC LIMIT ? OFFSET ?',
                        (page_size, (page - 1) * page_size)).fetchall()
    conn.close()
    return jsonify([dict(row) for row in data])

# API para insertar estados de actuadores en la base de datos
@actuator_bp.route('/add_actuator_state', methods=['POST'])
def add_actuator_state():
    data = request.get_json()
    name = data.get('name')
    state = data.get('state')
    if name and state is not None:
        save_actuator_state(name, state)
        return jsonify({"message": "Estado del actuador guardado correctamente"}), 201
    else:
        return jsonify({"error": "Datos incompletos"}), 400
