import sqlite3

def show_tables():
    conn = sqlite3.connect('/home/stevpi/Desktop/raspServer/sensor_data.db')
    c = conn.cursor()

    # Mostrar datos de la tabla dht_data
    c.execute('SELECT * FROM dht_data')
    dht_data = c.fetchall()
    print("Datos de la tabla dht_data:")
    for row in dht_data:
        print(row)

    # Mostrar datos de la tabla events
    c.execute('SELECT * FROM events')
    events = c.fetchall()
    print("\nDatos de la tabla events:")
    for row in events:
        print(row)

    # Mostrar datos de la tabla actuators
    c.execute('SELECT * FROM actuators')
    actuators = c.fetchall()
    print("\nDatos de la tabla actuators:")
    for row in actuators:
        print(row)

    conn.close()

# Ejecutar la funcion para mostrar las tablas si el archivo se ejecuta directamente
if __name__ == '__main__':
    show_tables()
