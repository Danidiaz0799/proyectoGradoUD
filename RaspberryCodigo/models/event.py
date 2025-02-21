import sqlite3
from datetime import datetime
from .sensor_data import get_db_connection

# Guardar evento en la base de datos
def save_event(message):
    conn = get_db_connection()
    conn.execute('INSERT INTO events (timestamp, message) VALUES (?, ?)',
                    (datetime.now().isoformat(), message))
    conn.commit()
    conn.close()

# Obtener todos los eventos desde la base de datos con paginación
def get_all_events(page, page_size):
    conn = get_db_connection()
    data = conn.execute('SELECT * FROM events ORDER BY timestamp DESC LIMIT ? OFFSET ?',
                        (page_size, (page - 1) * page_size)).fetchall()
    conn.close()
    return data

# Actualizar un evento en la base de datos
def update_event(id, message):
    conn = get_db_connection()
    conn.execute('UPDATE events SET message = ?, timestamp = ? WHERE id = ?',
                    (message, datetime.now().isoformat(), id))
    conn.commit()
    conn.close()
