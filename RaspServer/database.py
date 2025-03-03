import sqlite3

# Funcion para crear las tablas en la base de datos
def create_tables():
    conn = sqlite3.connect('/home/stevpi/Desktop/raspServer/sensor_data.db')
    c = conn.cursor()

    # Crear tabla para datos de sensore DHT11
    c.execute('''
        CREATE TABLE IF NOT EXISTS dht_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            temperature REAL NOT NULL,
            humidity REAL NOT NULL
        )
    ''')
    print("Tabla dht_data creada o ya existe.")

    # Crear tabla para datos de sensore BMP280
    c.execute('''
        CREATE TABLE IF NOT EXISTS bmp280_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            temperature REAL NOT NULL,
            pressure REAL NOT NULL
        )
    ''')
    print("Tabla bmp280_data creada o ya existe.")

    # Crear tabla para datos de sensore GY-302
    c.execute('''
        CREATE TABLE IF NOT EXISTS gy302_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            light_level REAL NOT NULL
        )
    ''')
    print("Tabla gy302_data creada o ya existe.")

    # Crear tabla para eventos
    c.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            topic TEXT NOT NULL
        )
    ''')
    print("Tabla events creada o ya existe.")

    # Crear tabla para actuadores
    c.execute('''
        CREATE TABLE IF NOT EXISTS actuators (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            state BOOLEAN NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    print("Tabla actuators creada o ya existe.")

    # Crear tabla para parametros ideales
    c.execute('''
        CREATE TABLE IF NOT EXISTS ideal_params (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            param_type TEXT NOT NULL,
            min_value REAL NOT NULL,
            max_value REAL NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    print("Tabla ideal_params creada o ya existe.")

    # Insertar parametros ideales predeterminados para temperatura y humedad
    c.execute('SELECT COUNT(*) FROM ideal_params WHERE param_type = "temperatura"')
    if c.fetchone()[0] == 0:
        c.execute('''
            INSERT INTO ideal_params (param_type, min_value, max_value, timestamp)
            VALUES ('temperatura', 15, 30, datetime('now'))
        ''')
        print("Parametros ideales para 'temperatura' insertados.")

    c.execute('SELECT COUNT(*) FROM ideal_params WHERE param_type = "humedad"')
    if c.fetchone()[0] == 0:
        c.execute('''
            INSERT INTO ideal_params (param_type, min_value, max_value, timestamp)
            VALUES ('humedad', 30, 100, datetime('now'))
        ''')
        print("Parametros ideales para 'humedad' insertados.")

    # Verificar si los actuadores predeterminados ya existen
    c.execute('SELECT COUNT(*) FROM actuators WHERE name = "Iluminacion"')
    if c.fetchone()[0] == 0:
        c.execute('''
            INSERT INTO actuators (name, state, timestamp)
            VALUES ('Iluminacion', 0, datetime('now'))
        ''')
        print("Actuador 'Iluminacion' insertado.")

    c.execute('SELECT COUNT(*) FROM actuators WHERE name = "Ventilacion"')
    if c.fetchone()[0] == 0:
        c.execute('''
            INSERT INTO actuators (name, state, timestamp)
            VALUES ('Ventilacion', 0, datetime('now'))
        ''')
        print("Actuador 'Ventilacion' insertado.")

    conn.commit()
    conn.close()
    print("Base de datos creada y tablas inicializadas.")

# Ejecutar la funcion para crear las tablas si el archivo se ejecuta directamente
if __name__ == '__main__':
    create_tables()
