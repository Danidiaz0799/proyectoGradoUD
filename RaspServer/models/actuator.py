import aiosqlite
from datetime import datetime
from .sensor_data import get_db_connection

# Guardar estado de actuadores en la base de datos
async def save_actuator_state(client_id, name, state):
    conn = await get_db_connection()
    await conn.execute('INSERT INTO actuators (client_id, name, state, timestamp) VALUES (?, ?, ?, ?)',
                       (client_id, name, state, datetime.now().isoformat()))
    await conn.commit()
    await conn.close()

# Editar estado de actuadores en la base de datos
async def update_actuator_state(client_id, id, state):
    conn = await get_db_connection()
    await conn.execute('UPDATE actuators SET state = ?, timestamp = ? WHERE id = ? AND client_id = ?',
                       (state, datetime.now().isoformat(), id, client_id))
    await conn.commit()
    await conn.close()

# Obtener todos los actuadores desde la base de datos para un cliente
async def get_all_actuators(client_id):
    conn = await get_db_connection()
    async with conn.execute('SELECT * FROM actuators WHERE client_id = ?', (client_id,)) as cursor:
        data = await cursor.fetchall()
    await conn.close()
    return data

# Obtener el estado de un actuador específico desde la base de datos
async def get_actuator_state(client_id, id):
    conn = await get_db_connection()
    async with conn.execute('SELECT state FROM actuators WHERE id = ? AND client_id = ?', (id, client_id)) as cursor:
        state = await cursor.fetchone()
    await conn.close()
    return state['state'] if state else None

# Obtener un actuador por nombre para un cliente específico
async def get_actuator_by_name(client_id, name):
    conn = await get_db_connection()
    async with conn.execute('SELECT * FROM actuators WHERE client_id = ? AND name = ?', (client_id, name)) as cursor:
        actuator = await cursor.fetchone()
    await conn.close()
    return actuator
