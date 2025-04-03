from datetime import datetime
from .sensor_data import get_db_connection, execute_query_with_retry, execute_write_query_with_retry

# Registrar un nuevo cliente
async def register_client(client_id, name, description=""):
    # Verificar si el cliente ya existe
    conn = await get_db_connection()
    async with conn.execute('SELECT * FROM clients WHERE client_id = ?', (client_id,)) as cursor:
        existing = await cursor.fetchone()
    
    if existing:
        # Actualizar el cliente existente
        query = '''
            UPDATE clients 
            SET name = ?, description = ?, last_seen = ?, status = 'online'
            WHERE client_id = ?
        '''
        params = (name, description, datetime.now().isoformat(), client_id)
        await conn.execute(query, params)
    else:
        # Crear un nuevo cliente
        query = '''
            INSERT INTO clients (client_id, name, description, last_seen, status, created_at)
            VALUES (?, ?, ?, ?, 'online', ?)
        '''
        params = (client_id, name, description, datetime.now().isoformat(), datetime.now().isoformat())
        await conn.execute(query, params)
        
        # Crear configuración inicial para el nuevo cliente
        await initialize_client_config(conn, client_id)
    
    await conn.commit()
    await conn.close()
    return True

# Inicializar configuración para un nuevo cliente
async def initialize_client_config(conn, client_id):
    # Crear parámetros ideales para el cliente
    await conn.execute('''
        INSERT INTO ideal_params (client_id, param_type, min_value, max_value, timestamp)
        VALUES (?, 'temperatura', 15, 30, ?)
    ''', (client_id, datetime.now().isoformat()))
    
    await conn.execute('''
        INSERT INTO ideal_params (client_id, param_type, min_value, max_value, timestamp)
        VALUES (?, 'humedad', 30, 100, ?)
    ''', (client_id, datetime.now().isoformat()))
    
    # Crear actuadores predeterminados para el cliente
    actuadores = [
        ('Iluminacion', 0),
        ('Ventilacion', 0),
        ('Humidificador', 0),
        ('Motor', 0)
    ]
    
    for nombre, estado in actuadores:
        await conn.execute('''
            INSERT INTO actuators (client_id, name, state, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (client_id, nombre, estado, datetime.now().isoformat()))
    
    # Crear estado inicial de la aplicación
    await conn.execute('''
        INSERT INTO app_state (client_id, mode, timestamp)
        VALUES (?, 'automatico', ?)
    ''', (client_id, datetime.now().isoformat()))

# Actualizar el estado de un cliente
async def update_client_status(client_id, status='online'):
    query = '''
        UPDATE clients
        SET status = ?, last_seen = ?
        WHERE client_id = ?
    '''
    params = (status, datetime.now().isoformat(), client_id)
    await execute_write_query_with_retry(query, params)

# Obtener todos los clientes registrados
async def get_all_clients():
    query = 'SELECT * FROM clients ORDER BY last_seen DESC'
    result = await execute_query_with_retry(query)
    return result

# Obtener un cliente específico por ID
async def get_client_by_id(client_id):
    query = 'SELECT * FROM clients WHERE client_id = ?'
    params = (client_id,)
    result = await execute_query_with_retry(query, params)
    return result[0] if result else None

# Verificar si un cliente existe
async def client_exists(client_id):
    query = 'SELECT COUNT(*) as count FROM clients WHERE client_id = ?'
    params = (client_id,)
    result = await execute_query_with_retry(query, params)
    return result[0]['count'] > 0 if result else False
