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

# Editar estado de actuadores en la base de datos
def update_actuator_state(id, state):
    conn = get_db_connection()
    conn.execute('UPDATE actuators SET state = ?, timestamp = ? WHERE id = ?',
                    (state, datetime.now().isoformat(), id))
    conn.commit()
    conn.close()

# Obtener todos los actuadores desde la base de datos
def get_all_actuators():
    conn = get_db_connection()
    data = conn.execute('SELECT * FROM actuators').fetchall()
    conn.close()
    return data
