from flask import Blueprint, request, jsonify
from models.app_state import get_app_state, update_app_state

app_state_bp = Blueprint('app_state_bp', __name__)

# API para obtener el estado de la aplicación
@app_state_bp.route('/getState', methods=['GET'])
def get_app_state_endpoint():
    try:
        state = get_app_state()
        if state:
            return jsonify({"mode": state}), 200
        else:
            return jsonify({"message": "Estado de la aplicacion no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API para actualizar el estado de la aplicación
@app_state_bp.route('/updateState', methods=['PUT'])
def update_app_state_endpoint():
    try:
        data = request.json
        mode = data.get('mode')
        if mode in ['manual', 'automatico']:
            update_app_state(mode)
            return jsonify({"message": "Estado de la aplicacion actualizado exitosamente"}), 200
        else:
            return jsonify({"error": "Modo invalido"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
