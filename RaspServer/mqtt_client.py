import paho.mqtt.client as mqtt
from models.sensor_data import save_sht3x_data, get_ideal_params
from models.event import save_event
from models.client import update_client_status, register_client, client_exists
import time
from models.actuator import update_actuator_state, get_actuator_state, get_actuator_by_name
from models.app_state import get_app_state
import asyncio
import re

client = None
client_last_events = {}  # Diccionario para rastrear el ultimo evento por cliente y tipo

# Funcion para extraer el client_id de un topico MQTT
def extract_client_id(topic):
    # El formato esperado es 'clients/{client_id}/...'
    match = re.match(r'clients/([^/]+)/', topic)
    if match:
        return match.group(1)
    return None

# Funcion de callback cuando se recibe un mensaje MQTT
def on_message(client, userdata, msg):
    try:
        # Extraer el client_id del topico
        client_id = extract_client_id(msg.topic)
        if not client_id:
            print(f"No se pudo extraer client_id del topico: {msg.topic}")
            return
        
        # Actualizar estado del cliente
        asyncio.run(update_client_status(client_id))
        
        # Procesar el mensaje segun el topico
        if msg.topic == f'clients/{client_id}/sensor/sht3x':
            data = msg.payload.decode('utf-8', errors='ignore').split(',')
            if len(data) == 2:
                asyncio.run(handle_sht3x_message(client_id, data))

        elif msg.topic == f'clients/{client_id}/register':
            data = msg.payload.decode('utf-8', errors='ignore').split(',')
            if len(data) >= 2:
                name = data[0]
                description = data[1] if len(data) > 1 else ""
                asyncio.run(register_client(client_id, name, description))
                print(f"Cliente {client_id} registrado: {name}")
        else:
            print(f"Topico no reconocido: {msg.topic}")
    except Exception as e:
        print(f'Error al procesar el mensaje: {e}')

async def handle_sht3x_message(client_id, data):
    global client_last_events
    temperatura, humedad = float(data[0]), float(data[1])
    print(f'Cliente {client_id} - Temperatura: {temperatura}C, Humedad: {humedad}')
    await save_sht3x_data(client_id, temperatura, humedad)
    current_time = time.time()

    # Inicializar entradas para este cliente si no existen
    if client_id not in client_last_events:
        client_last_events[client_id] = {'temp': 0, 'hum': 0}

    # Obtener parametros ideales para este cliente
    ideal_temp_params = await get_ideal_params(client_id, 'temperatura')
    ideal_humidity_params = await get_ideal_params(client_id, 'humedad')

    if not ideal_temp_params or not ideal_humidity_params:
        print(f"No se encontraron parametros ideales para cliente {client_id}")
        return

    min_temp = ideal_temp_params['min_value']
    max_temp = ideal_temp_params['max_value']
    min_humidity = ideal_humidity_params['min_value']
    max_humidity = ideal_humidity_params['max_value']

    # Verificar si la temperatura o la humedad estan fuera de los parametros
    if not (min_temp <= temperatura <= max_temp):
        if current_time - client_last_events[client_id]['temp'] > 60:
            await save_event(client_id, f"Advertencia! Temperatura fuera de rango: {temperatura} C (Ideal: {min_temp}-{max_temp} C)", "temperatura")
            client_last_events[client_id]['temp'] = current_time
    
    if not (min_humidity <= humedad <= max_humidity):
        if current_time - client_last_events[client_id]['hum'] > 60:
            await save_event(client_id, f"Advertencia! Humedad fuera de rango: {humedad} % (Ideal: {min_humidity}-{max_humidity} %)", "humedad")
            client_last_events[client_id]['hum'] = current_time

    # Verificar el estado de la aplicacion para este cliente
    app_state = await get_app_state(client_id)
    if app_state == 'automatico':
        await update_actuators(client_id, temperatura, humedad)

async def update_actuators(client_id, temperature, humidity):
    # Obtener parametros ideales para este cliente
    ideal_temp_params = await get_ideal_params(client_id, 'temperatura')
    ideal_humidity_params = await get_ideal_params(client_id, 'humedad')

    if not ideal_temp_params or not ideal_humidity_params:
        print(f"No se encontraron parametros ideales para cliente {client_id}")
        return

    min_temp = ideal_temp_params['min_value']
    max_temp = ideal_temp_params['max_value']
    min_humidity = ideal_humidity_params['min_value']
    max_humidity = ideal_humidity_params['max_value']

    # Obtener actuadores por nombre para este cliente
    light_actuator = await get_actuator_by_name(client_id, "Iluminacion")
    fan_actuator = await get_actuator_by_name(client_id, "Ventilacion")
    humidifier_actuator = await get_actuator_by_name(client_id, "Humidificador")
    motor_actuator = await get_actuator_by_name(client_id, "Motor")
    
    if not all([light_actuator, fan_actuator, humidifier_actuator, motor_actuator]):
        print(f"No se encontraron todos los actuadores para cliente {client_id}")
        return

    # Validar temperatura
    if temperature < min_temp:
        await update_actuator_and_log(client_id, light_actuator['id'], 'true', "Temperatura baja", f'clients/{client_id}/light')
        await update_actuator_and_log(client_id, fan_actuator['id'], 'false', "Ventilador apagado", f'clients/{client_id}/fan')
    elif temperature > max_temp:
        await update_actuator_and_log(client_id, light_actuator['id'], 'false', "Temperatura alta", f'clients/{client_id}/light')
        await update_actuator_and_log(client_id, fan_actuator['id'], 'true', "Ventilador encendido", f'clients/{client_id}/fan')
    else:
        await update_actuator_and_log(client_id, light_actuator['id'], 'false', "Temperatura normal", f'clients/{client_id}/light')
        await update_actuator_and_log(client_id, fan_actuator['id'], 'false', "Ventilador apagado", f'clients/{client_id}/fan')

    # Validar humedad
    if humidity < min_humidity:
        await update_actuator_and_log(client_id, humidifier_actuator['id'], 'true', "Humedad baja", f'clients/{client_id}/humidifier')
        await update_actuator_and_log(client_id, motor_actuator['id'], 'false', "Motor apagado", f'clients/{client_id}/motor')
    elif humidity > max_humidity:
        await update_actuator_and_log(client_id, humidifier_actuator['id'], 'false', "Humedad alta", f'clients/{client_id}/humidifier')
        await update_actuator_and_log(client_id, motor_actuator['id'], 'true', "Motor encendido", f'clients/{client_id}/motor')
    else:
        await update_actuator_and_log(client_id, humidifier_actuator['id'], 'false', "Humedad normal", f'clients/{client_id}/humidifier')
        await update_actuator_and_log(client_id, motor_actuator['id'], 'false', "Motor apagado", f'clients/{client_id}/motor')

async def update_actuator_and_log(client_id, actuator_id, state, description, topic):
    current_state = await get_actuator_state(client_id, actuator_id)
    if current_state != state:
        await update_actuator_state(client_id, actuator_id, state)
        await publish_message(topic, str(state).lower())
        print(f'Cliente {client_id} - {description}: {state}')

# Funcion para publicar mensajes MQTT
async def publish_message(topic, message):
    global client
    if client:
        client.publish(topic, message)
    else:
        print("Cliente MQTT no esta conectado")

# Configuracion del cliente MQTT
def connect_mqtt():
    global client
    client = mqtt.Client()
    client.on_message = on_message
    client.connect('localhost', 1883, 60)
    
    # Suscribirse a todos los topicos de clientes
    client.subscribe('clients/+/sensor/sht3x')
    client.subscribe('clients/+/register')
    
    client.loop_start()
    print("Cliente MQTT inicializado y suscrito a topicos de multiples clientes")
