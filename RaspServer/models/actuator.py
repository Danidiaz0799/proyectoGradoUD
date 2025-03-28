import aiosqlite
from datetime import datetime
from .sensor_data import get_db_connection

# Guardar estado de actuadores en la base de datos
async def save_actuator_state(name, state):
    conn = await get_db_connection()
    await conn.execute('INSERT INTO actuators (timestamp, name, state) VALUES (?, ?, ?)',
                       (datetime.now().isoformat(), name, state))
    await conn.commit()
    await conn.close()

# Editar estado de actuadores en la base de datos
async def update_actuator_state(id, state):
    conn = await get_db_connection()
    await conn.execute('UPDATE actuators SET state = ?, timestamp = ? WHERE id = ?',
                       (state, datetime.now().isoformat(), id))
    await conn.commit()
    await conn.close()

# Obtener todos los actuadores desde la base de datos
async def get_all_actuators():
    conn = await get_db_connection()
    async with conn.execute('SELECT * FROM actuators') as cursor:
        data = await cursor.fetchall()
    await conn.close()
    return data

# Obtener el estado de un actuador específico desde la base de datos
async def get_actuator_state(id):
    conn = await get_db_connection()
    async with conn.execute('SELECT state FROM actuators WHERE id = ?', (id,)) as cursor:
        state = await cursor.fetchone()
    await conn.close()
    return state['state'] if state else None
