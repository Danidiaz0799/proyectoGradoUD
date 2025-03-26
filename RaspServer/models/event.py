import aiosqlite
from datetime import datetime
from .sensor_data import get_db_connection

# Guardar evento en la base de datos
async def save_event(message, topic):
    conn = await get_db_connection()
    await conn.execute('INSERT INTO events (timestamp, message, topic) VALUES (?, ?, ?)',
                       (datetime.now().isoformat(), message, topic))
    await conn.commit()
    await conn.close()

# Obtener todos los eventos desde la base de datos con paginacion
async def get_all_events(page, page_size):
    conn = await get_db_connection()
    async with conn.execute('SELECT * FROM events ORDER BY timestamp DESC LIMIT ? OFFSET ?',
                            (page_size, (page - 1) * page_size)) as cursor:
        data = await cursor.fetchall()
    await conn.close()
    return data

# Obtener eventos filtrados por tema
async def get_events_by_topic(topic, page, page_size):
    conn = await get_db_connection()
    async with conn.execute('SELECT * FROM events WHERE topic = ? ORDER BY timestamp DESC LIMIT ? OFFSET ?',
                            (topic, page_size, (page - 1) * page_size)) as cursor:
        data = await cursor.fetchall()
    await conn.close()
    return data

# Actualizar un evento en la base de datos
async def update_event(id, message, topic):
    conn = await get_db_connection()
    await conn.execute('UPDATE events SET message = ?, timestamp = ?, topic = ? WHERE id = ?',
                       (message, datetime.now().isoformat(), topic, id))
    await conn.commit()
    await conn.close()

# Eliminar un evento en la base de datos
async def delete_event(id):
    conn = await get_db_connection()
    await conn.execute('DELETE FROM events WHERE id = ?', (id,))
    await conn.commit()
    await conn.close()
