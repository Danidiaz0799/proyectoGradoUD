import sqlite3

# Funcion para crear las tablas en la base de datos
def create_tables():
    conn = sqlite3.connect('/home/stevpi/Desktop/raspServer/sensor_data.db')
    c = conn.cursor()

    # Crear tabla para datos de sensore SHT3x
    c.execute('''
        CREATE TABLE IF NOT EXISTS sht3x_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            temperature REAL NOT NULL,
            humidity REAL NOT NULL
        )
    ''')
    print("Tabla sht3x_data creada o ya existe.")

    # Crear tabla para eventos
    c.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id TEXT NOT NULL,
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
            client_id TEXT NOT NULL,
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
            client_id TEXT NOT NULL,
            param_type TEXT NOT NULL,
            min_value REAL NOT NULL,
            max_value REAL NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    print("Tabla ideal_params creada o ya existe.")

    # Crear tabla para el estado de la aplicacion
    c.execute('''
        CREATE TABLE IF NOT EXISTS app_state (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id TEXT NOT NULL,
            mode TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    print("Tabla app_state creada o ya existe.")
    
    # Crear tabla para registro de clientes
    c.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            last_seen TEXT,
            status TEXT DEFAULT 'offline',
            created_at TEXT NOT NULL
        )
    ''')
    print("Tabla clients creada o ya existe.")

    # Insertar cliente predeterminado si no existe
    c.execute('SELECT COUNT(*) FROM clients WHERE client_id = "mushroom1"')
    if c.fetchone()[0] == 0:
        c.execute('''
            INSERT INTO clients (client_id, name, description, last_seen, status, created_at)
            VALUES ('mushroom1', 'Cliente 1', 'Cliente predeterminado', datetime('now'), 'offline', datetime('now'))
        ''')
        print("Cliente predeterminado 'mushroom1' insertado.")

    # Insertar parametros ideales predeterminados para temperatura y humedad
    c.execute('SELECT COUNT(*) FROM ideal_params WHERE param_type = "temperatura" AND client_id = "mushroom1"')
    if c.fetchone()[0] == 0:
        c.execute('''
            INSERT INTO ideal_params (client_id, param_type, min_value, max_value, timestamp)
            VALUES ('mushroom1', 'temperatura', 15, 30, datetime('now'))
        ''')
        print("Parametros ideales para 'temperatura' insertados.")

    c.execute('SELECT COUNT(*) FROM ideal_params WHERE param_type = "humedad" AND client_id = "mushroom1"')
    if c.fetchone()[0] == 0:
        c.execute('''
            INSERT INTO ideal_params (client_id, param_type, min_value, max_value, timestamp)
            VALUES ('mushroom1', 'humedad', 30, 100, datetime('now'))
        ''')
        print("Parametros ideales para 'humedad' insertados.")

    # Verificar si los actuadores predeterminados ya existen para el cliente mushroom1
    c.execute('SELECT COUNT(*) FROM actuators WHERE name = "Iluminacion" AND client_id = "mushroom1"')
    if c.fetchone()[0] == 0:
        c.execute('''
            INSERT INTO actuators (client_id, name, state, timestamp)
            VALUES ('mushroom1', 'Iluminacion', 0, datetime('now'))
        ''')
        print("Actuador 'Iluminacion' insertado.")

    c.execute('SELECT COUNT(*) FROM actuators WHERE name = "Ventilacion" AND client_id = "mushroom1"')
    if c.fetchone()[0] == 0:
        c.execute('''
            INSERT INTO actuators (client_id, name, state, timestamp)
            VALUES ('mushroom1', 'Ventilacion', 0, datetime('now'))
        ''')
        print("Actuador 'Ventilacion' insertado.")

    c.execute('SELECT COUNT(*) FROM actuators WHERE name = "Humidificador" AND client_id = "mushroom1"')
    if c.fetchone()[0] == 0:
        c.execute('''
            INSERT INTO actuators (client_id, name, state, timestamp)
            VALUES ('mushroom1', 'Humidificador', 0, datetime('now'))
        ''')
        print("Actuador 'Humidificador' insertado.")

    c.execute('SELECT COUNT(*) FROM actuators WHERE name = "Motor" AND client_id = "mushroom1"')
    if c.fetchone()[0] == 0:
        c.execute('''
            INSERT INTO actuators (client_id, name, state, timestamp)
            VALUES ('mushroom1', 'Motor', 0, datetime('now'))
        ''')
        print("Actuador 'Motor' insertado.")

    # Insertar estado inicial de la aplicacion si no existe para el cliente mushroom1
    c.execute('SELECT COUNT(*) FROM app_state WHERE client_id = "mushroom1"')
    if c.fetchone()[0] == 0:
        c.execute('''
            INSERT INTO app_state (client_id, mode, timestamp)
            VALUES ('mushroom1', 'automatico', datetime('now'))
        ''')
        print("Estado inicial de la aplicacion insertado.")

    conn.commit()
    conn.close()
    print("Base de datos creada y tablas inicializadas.")

# Ejecutar la funcion para crear las tablas si el archivo se ejecuta directamente
if __name__ == '__main__':
    create_tables()
