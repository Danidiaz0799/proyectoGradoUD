from flask import Blueprint, request, jsonify
from models.actuator import save_actuator_state, get_db_connection
from mqtt_client import publish_message

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

# API para encender/apagar la luz del ESP32
@actuator_bp.route('/toggle_light', methods=['POST'])
def toggle_light():
    data = request.get_json()
    state = data.get('state')
    if state is not None:
        publish_message('esp32/light', str(state).lower())
        return jsonify({"message": "Senal enviada correctamente"}), 200
    else:
        return jsonify({"error": "Datos incompletos"}), 400
