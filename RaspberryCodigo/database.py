import sqlite3

def create_tables():
    conn = sqlite3.connect('sensor_data.db')
    c = conn.cursor()

    # Crear tabla para datos de sensores
    c.execute('''
        CREATE TABLE IF NOT EXISTS dht_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            temperature REAL NOT NULL,
            humidity REAL NOT NULL
        )
    ''')
    print("Tabla dht_data creada o ya existe.")

    # Crear tabla para eventos
    c.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT NOT NULL,
            timestamp TEXT NOT NULL
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

    conn.commit()
    conn.close()
    print("Base de datos creada y tablas inicializadas.")

if __name__ == '__main__':
    create_tables()
