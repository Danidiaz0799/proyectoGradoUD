import sqlite3
from datetime import datetime
from .sensor_data import get_db_connection

# Guardar estado de actuadores en la base de datos
def save_actuator_state(name, state):
    conn = get_db_connection()
    conn.execute('INSERT INTO actuators (timestamp, name, state) VALUES (?, ?, ?)',
                    (datetime.now().isoformat(), name, state))
    conn.commit()
    conn.close()
