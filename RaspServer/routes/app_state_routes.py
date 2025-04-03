from flask import Blueprint, request, jsonify
from models.app_state import get_app_state, update_app_state
from models.client import client_exists

app_state_bp = Blueprint('app_state_bp', __name__)

# API para obtener el estado de la aplicación
@app_state_bp.route('/clients/<client_id>/getState', methods=['GET'])
async def get_app_state_endpoint(client_id):
    try:
        # Verificar que el cliente existe
        if not await client_exists(client_id):
            return jsonify({"error": "Cliente no encontrado"}), 404
            
        state = await get_app_state(client_id)
        if state:
            return jsonify({"mode": state}), 200
        else:
            return jsonify({"message": "Estado de la aplicacion no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API para actualizar el estado de la aplicación
@app_state_bp.route('/clients/<client_id>/updateState', methods=['PUT'])
async def update_app_state_endpoint(client_id):
    try:
        # Verificar que el cliente existe
        if not await client_exists(client_id):
            return jsonify({"error": "Cliente no encontrado"}), 404
            
        data = request.json
        mode = data.get('mode')
        if mode in ['manual', 'automatico']:
            await update_app_state(client_id, mode)
            return jsonify({"message": "Estado de la aplicacion actualizado exitosamente"}), 200
        else:
            return jsonify({"error": "Modo invalido"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
