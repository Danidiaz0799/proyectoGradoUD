import sqlite3
from datetime import datetime

# Conectar a la base de datos
def get_db_connection():
    conn = sqlite3.connect('/home/stevpi/Desktop/raspServer/sensor_data.db')  # Actualizar la ruta de la base de datos
    conn.row_factory = sqlite3.Row
    return conn

# Guardar datos del dht11 en la base de datos
def save_dht11_data(temperature, humidity):
    conn = get_db_connection()
    conn.execute('INSERT INTO dht_data (timestamp, temperature, humidity) VALUES (?, ?, ?)',
                    (datetime.now().isoformat(), temperature, humidity))
    conn.commit()
    conn.close()

# Obtener todos los datos de dht11 desde la base de datos
def get_all_dht11_data(page, page_size):
    conn = get_db_connection()
    data = conn.execute('SELECT * FROM dht_data ORDER BY timestamp DESC LIMIT ? OFFSET ?',
                        (page_size, (page - 1) * page_size)).fetchall()
    conn.close()
    return data

# Guardar datos del bmp280 en la base de datos
def save_bmp280_data(temperature, pressure):
    conn = get_db_connection()
    conn.execute('INSERT INTO bmp280_data (timestamp, temperature, pressure) VALUES (?, ?, ?)',
                    (datetime.now().isoformat(), temperature, pressure))
    conn.commit()
    conn.close()

# Obtener todos los datos de bmp280 desde la base de datos
def get_all_bmp280_data(page, page_size):
    conn = get_db_connection()
    data = conn.execute('SELECT * FROM bmp280_data ORDER BY timestamp DESC LIMIT ? OFFSET ?',
                        (page_size, (page - 1) * page_size)).fetchall()
    conn.close()
    return data

# Guardar datos del gy302 en la base de datos
def save_gy302_data(light_level):
    conn = get_db_connection()
    conn.execute('INSERT INTO gy302_data (timestamp, light_level) VALUES (?, ?)',
                    (datetime.now().isoformat(), light_level))
    conn.commit()
    conn.close()

# Obtener todos los datos de gy302 desde la base de datos
def get_all_gy302_data(page, page_size):
    conn = get_db_connection()
    data = conn.execute('SELECT * FROM gy302_data ORDER BY timestamp DESC LIMIT ? OFFSET ?',
                        (page_size, (page - 1) * page_size)).fetchall()
    conn.close()
    return data
