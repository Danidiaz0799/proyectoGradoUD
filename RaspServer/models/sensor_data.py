import aiosqlite
from datetime import datetime
import time

# Conectar a la base de datos
async def get_db_connection():
    conn = await aiosqlite.connect('/home/stevpi/Desktop/raspServer/sensor_data.db')
    conn.row_factory = aiosqlite.Row
    return conn

async def execute_query_with_retry(query, params=(), retries=5, delay=1):
    for attempt in range(retries):
        try:
            conn = await get_db_connection()
            async with conn.execute(query, params) as cursor:
                result = await cursor.fetchall()
            await conn.commit()
            await conn.close()
            return result
        except aiosqlite.OperationalError as e:
            if "database is locked" in str(e) and attempt < retries - 1:
                await asyncio.sleep(delay)
            else:
                raise

async def execute_write_query_with_retry(query, params=(), retries=5, delay=1):
    for attempt in range(retries):
        try:
            conn = await get_db_connection()
            await conn.execute(query, params)
            await conn.commit()
            await conn.close()
            return
        except aiosqlite.OperationalError as e:
            if "database is locked" in str(e) and attempt < retries - 1:
                await asyncio.sleep(delay)
            else:
                raise

# Guardar datos del sht3x en la base de datos
async def save_sht3x_data(temperature, humidity):
    query = 'INSERT INTO sht3x_data (timestamp, temperature, humidity) VALUES (?, ?, ?)'
    params = (datetime.now().isoformat(), temperature, humidity)
    await execute_write_query_with_retry(query, params)

# Obtener todos los datos de sht3x desde la base de datos
async def get_all_sht3x_data(page, page_size):
    conn = await get_db_connection()
    async with conn.execute('SELECT * FROM sht3x_data ORDER BY timestamp DESC LIMIT ? OFFSET ?',
                            (page_size, (page - 1) * page_size)) as cursor:
        data = await cursor.fetchall()
    await conn.close()
    return data

# Guardar datos del gy302 en la base de datos
async def save_gy302_data(light_level):
    query = 'INSERT INTO gy302_data (timestamp, light_level) VALUES (?, ?)'
    params = (datetime.now().isoformat(), light_level)
    await execute_write_query_with_retry(query, params)

# Obtener todos los datos de gy302 desde la base de datos
async def get_all_gy302_data(page, page_size):
    conn = await get_db_connection()
    async with conn.execute('SELECT * FROM gy302_data ORDER BY timestamp DESC LIMIT ? OFFSET ?',
                            (page_size, (page - 1) * page_size)) as cursor:
        data = await cursor.fetchall()
    await conn.close()
    return data

# Obtener parametros ideales desde la base de datos
async def get_ideal_params(param_type):
    query = 'SELECT * FROM ideal_params WHERE param_type = ? ORDER BY timestamp DESC LIMIT 1'
    params = (param_type,)
    result = await execute_query_with_retry(query, params)
    return result[0] if result else None

# Actualizar parametros ideales en la base de datos
async def update_ideal_params(param_type, min_value, max_value):
    query = '''
        UPDATE ideal_params
        SET min_value = ?, max_value = ?, timestamp = ?
        WHERE param_type = ?
    '''
    params = (min_value, max_value, datetime.now().isoformat(), param_type)
    await execute_write_query_with_retry(query, params)
