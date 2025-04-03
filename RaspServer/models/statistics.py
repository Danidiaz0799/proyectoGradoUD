import numpy as np
from datetime import datetime, timedelta
from collections import Counter
from models.sensor_data import execute_query_with_retry

async def get_sht3x_statistics(client_id, days=7):
    """
    Obtiene estadisticas de temperatura y humedad de los ultimos dias
    Args:
        client_id: ID del cliente para el que se obtienen las estadisticas
        days: Cantidad de dias hacia atras para analizar (por defecto 7)
    Returns:
        Diccionario con estadisticas de temperatura y humedad
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    query = """
        SELECT temperature, humidity
        FROM sht3x_data
        WHERE client_id = ? AND timestamp BETWEEN ? AND ?
        ORDER BY timestamp DESC
    """
    params = (client_id, start_date.isoformat(), end_date.isoformat())
    result = await execute_query_with_retry(query, params)
    if not result:
        return {
            "temperature": {
                "count": 0,
                "mean": 0,
                "median": 0,
                "mode": 0,
                "min": 0,
                "max": 0,
                "std_dev": 0
            },
            "humidity": {
                "count": 0,
                "mean": 0,
                "median": 0,
                "mode": 0,
                "min": 0,
                "max": 0,
                "std_dev": 0
            }
        }
    # Extraer datos usando numpy para mejor rendimiento
    data = np.array([(row['temperature'], row['humidity']) for row in result])
    temperatures = data[:, 0]
    humidity_values = data[:, 1]
    def calculate_stats(values):
        """Calcula todas las estadisticas para un conjunto de valores"""
        return {
            "count": len(values),
            "mean": float(np.mean(values)),
            "median": float(np.median(values)),
            "mode": float(Counter(values).most_common(1)[0][0]) if len(values) > 0 else 0,
            "min": float(np.min(values)),
            "max": float(np.max(values)),
            "std_dev": float(np.std(values))
        }
    return {
        "temperature": calculate_stats(temperatures),
        "humidity": calculate_stats(humidity_values)
    }