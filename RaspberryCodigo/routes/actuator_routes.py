from flask import Blueprint, request, jsonify
from mqtt_client import publish_message
from models.event import save_event  # Importar la funcion para guardar eventos

actuator_bp = Blueprint('actuator_bp', __name__)

# API para encender/apagar la luz del ESP32
@actuator_bp.route('/Actuator/toggle_light', methods=['POST'])
def toggle_light():
    data = request.get_json()
    state = data.get('state')
    if state is not None:
        publish_message('esp32/light', str(state).lower())
        save_event(f"Actuador Iluminacion cambiado a {state}")  # Guardar evento
        return jsonify({"message": "Senal enviada correctamente"}), 200
    else:
        return jsonify({"error": "Datos incompletos"}), 400
