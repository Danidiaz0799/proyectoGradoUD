import aiosqlite
from datetime import datetime
from .sensor_data import get_db_connection

async def get_app_state():
    conn = await get_db_connection()
    async with conn.execute('SELECT mode FROM app_state ORDER BY timestamp DESC LIMIT 1') as cursor:
        state = await cursor.fetchone()
    await conn.close()
    return state['mode'] if state else None

async def update_app_state(mode):
    conn = await get_db_connection()
    await conn.execute('INSERT INTO app_state (mode, timestamp) VALUES (?, ?)', (mode, datetime.now().isoformat()))
    await conn.commit()
    await conn.close()
