import sqlite3

def clean_tables():
    conn = sqlite3.connect('/home/stevpi/Desktop/raspServer/sensor_data.db')
    c = conn.cursor()

    # Limpiar datos de la tabla dht_data
    c.execute('DELETE FROM dht_data')
    print("Datos de la tabla dht_data limpiados.")

    # Limpiar datos de la tabla events
    c.execute('DELETE FROM events')
    print("Datos de la tabla events limpiados.")

    conn.commit()
    conn.close()
    print("Base de datos limpiada.")

# Ejecutar la funcion para limpiar las tablas si el archivo se ejecuta directamente
if __name__ == '__main__':
    clean_tables()
