import sqlite3
from datetime import datetime
from .sensor_data import get_db_connection

# Guardar evento en la base de datos
def save_event(message, topic):
    conn = get_db_connection()
    conn.execute('INSERT INTO events (timestamp, message, topic) VALUES (?, ?, ?)',
                    (datetime.now().isoformat(), message, topic))
    conn.commit()
    conn.close()

# Obtener todos los eventos desde la base de datos con paginacion
def get_all_events(page, page_size):
    conn = get_db_connection()
    data = conn.execute('SELECT * FROM events ORDER BY timestamp DESC LIMIT ? OFFSET ?',
                        (page_size, (page - 1) * page_size)).fetchall()
    conn.close()
    return data

# Actualizar un evento en la base de datos
def update_event(id, message, topic):
    conn = get_db_connection()
    conn.execute('UPDATE events SET message = ?, timestamp = ?, topic = ? WHERE id = ?',
                    (message, datetime.now().isoformat(), topic, id))
    conn.commit()
    conn.close()
