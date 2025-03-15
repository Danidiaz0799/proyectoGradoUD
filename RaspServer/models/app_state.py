import sqlite3
from datetime import datetime
from .sensor_data import get_db_connection

def get_app_state():
    conn = get_db_connection()
    state = conn.execute('SELECT mode FROM app_state ORDER BY timestamp DESC LIMIT 1').fetchone()
    conn.close()
    return state['mode'] if state else None

def update_app_state(mode):
    conn = get_db_connection()
    conn.execute('INSERT INTO app_state (mode, timestamp) VALUES (?, ?)', (mode, datetime.now().isoformat()))
    conn.commit()
    conn.close()
