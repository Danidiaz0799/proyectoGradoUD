from flask import Blueprint, request, jsonify
import asyncio
from models.statistics import get_sht3x_statistics
from models.client import client_exists

# Crear un Blueprint para las rutas de estadisticas
statistics_bp = Blueprint('statistics_bp', __name__)

# API para obtener informacion completa de estadisticas (dashboard)
@statistics_bp.route('/clients/<client_id>/statistics/dashboard', methods=['GET'])
async def get_dashboard_statistics(client_id):
    # Verificar que el cliente existe
    if not await client_exists(client_id):
        return jsonify({"error": "Cliente no encontrado"}), 404
        
    days = int(request.args.get('days', 7))  # Periodo predeterminado: 7 dias
    # Obtener estadísticas de temperatura y humedad
    sht3x_stats = await get_sht3x_statistics(client_id, days)
    # Organizar los resultados
    dashboard_data = {
        "sht3x_stats": sht3x_stats
    }
    return jsonify(dashboard_data)