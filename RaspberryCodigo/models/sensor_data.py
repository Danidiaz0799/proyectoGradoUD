import sqlite3
from datetime import datetime

# Conectar a la base de datos
def get_db_connection():
    conn = sqlite3.connect('/home/stevpi/Desktop/raspServer/sensor_data.db')  # Actualizar la ruta de la base de datos
    conn.row_factory = sqlite3.Row
    return conn

# Guardar datos del sensor en la base de datos
def save_sensor_data(temperature, humidity):
    conn = get_db_connection()
    conn.execute('INSERT INTO dht_data (timestamp, temperature, humidity) VALUES (?, ?, ?)',
                    (datetime.now().isoformat(), temperature, humidity))
    conn.commit()
    conn.close()

# Obtener todos los datos de sensores desde la base de datos
def get_all_sensor_data(page, page_size):
    conn = get_db_connection()
    data = conn.execute('SELECT * FROM dht_data ORDER BY timestamp DESC LIMIT ? OFFSET ?',
                        (page_size, (page - 1) * page_size)).fetchall()
    conn.close()
    return data
