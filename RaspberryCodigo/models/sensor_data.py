import sqlite3
from datetime import datetime

# Conectar a la base de datos
def get_db_connection():
    conn = sqlite3.connect('/home/stevpi/Desktop/proyectoGradoUD/sensor_data.db')  # Actualizar la ruta de la base de datos
    conn.row_factory = sqlite3.Row
    return conn

# Guardar datos del sensor en la base de datos
def save_sensor_data(temperature, humidity):
    conn = get_db_connection()
    conn.execute('INSERT INTO dht_data (timestamp, temperature, humidity) VALUES (?, ?, ?)',
                    (datetime.now().isoformat(), temperature, humidity))
    conn.commit()
    conn.close()
