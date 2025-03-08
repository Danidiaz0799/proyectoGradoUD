import sqlite3
from datetime import datetime

# Conectar a la base de datos
def get_db_connection():
    conn = sqlite3.connect('/home/stevpi/Desktop/raspServer/sensor_data.db')  # Actualizar la ruta de la base de datos
    conn.row_factory = sqlite3.Row
    return conn

# Guardar datos del sht3x en la base de datos
def save_sht3x_data(temperature, humidity):
    conn = get_db_connection()
    conn.execute('INSERT INTO sht3x_data (timestamp, temperature, humidity) VALUES (?, ?, ?)',
                    (datetime.now().isoformat(), temperature, humidity))
    conn.commit()
    conn.close()

# Obtener todos los datos de sht3x desde la base de datos
def get_all_sht3x_data(page, page_size):
    conn = get_db_connection()
    data = conn.execute('SELECT * FROM sht3x_data ORDER BY timestamp DESC LIMIT ? OFFSET ?',
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

# Obtener data de sensores por fecha inicial y fecha final con paginación
def get_sensor_data_by_date(start_date, end_date, page, page_size):
    conn = get_db_connection()
    sht3x_data = conn.execute('SELECT * FROM sht3x_data WHERE timestamp BETWEEN ? AND ? ORDER BY timestamp DESC LIMIT ? OFFSET ?', 
                            (start_date, end_date, page_size, (page - 1) * page_size)).fetchall()
    gy302_data = conn.execute('SELECT * FROM gy302_data WHERE timestamp BETWEEN ? AND ? ORDER BY timestamp DESC LIMIT ? OFFSET ?', 
                              (start_date, end_date, page_size, (page - 1) * page_size)).fetchall()
    conn.close()
    return {
        "sht3x_data": [dict(row) for row in sht3x_data],
        "gy302_data": [dict(row) for row in gy302_data]
    }

# Obtener parametros ideales desde la base de datos
def get_ideal_params(param_type):
    conn = get_db_connection()
    params = conn.execute('SELECT * FROM ideal_params WHERE param_type = ? ORDER BY timestamp DESC LIMIT 1',
                        (param_type,)).fetchone()
    conn.close()
    return params

# Actualizar parametros ideales en la base de datos
def update_ideal_params(param_type, min_value, max_value):
    conn = get_db_connection()
    conn.execute('''
        UPDATE ideal_params
        SET min_value = ?, max_value = ?, timestamp = ?
        WHERE param_type = ?
    ''', (min_value, max_value, datetime.now().isoformat(), param_type))
    conn.commit()
    conn.close()
