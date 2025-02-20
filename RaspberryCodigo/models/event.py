import sqlite3
from datetime import datetime
from .sensor_data import get_db_connection

# Guardar eventos en la base de datos
def save_event(message):
    conn = get_db_connection()
    conn.execute('INSERT INTO events (timestamp, message) VALUES (?, ?)',
                    (datetime.now().isoformat(), message))
    conn.commit()
    conn.close()
