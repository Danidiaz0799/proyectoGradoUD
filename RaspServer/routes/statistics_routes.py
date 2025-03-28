from flask import Blueprint, request, jsonify
import asyncio
from models.statistics import get_sht3x_statistics

# Crear un Blueprint para las rutas de estadisticas
statistics_bp = Blueprint('statistics_bp', __name__)

# API para obtener informacion completa de estadisticas (dashboard)
@statistics_bp.route('/statistics/dashboard', methods=['GET'])
async def get_dashboard_statistics():
    days = int(request.args.get('days', 7))  # Periodo predeterminado: 7 dias
    # Obtener estadísticas de temperatura y humedad
    sht3x_stats = await get_sht3x_statistics(days)
    # Organizar los resultados
    dashboard_data = {
        "sht3x_stats": sht3x_stats
    }
    return jsonify(dashboard_data)