import paho.mqtt.client as mqtt
from models.sensor_data import save_sht3x_data, save_gy302_data, get_ideal_params
from models.event import save_event
import time
from models.actuator import update_actuator_state, get_actuator_state
from models.app_state import get_app_state  # Importar la función para obtener el estado de la aplicación
import asyncio

client = None
last_temp_event_time = 0
last_hum_event_time = 0

# Funcion de callback cuando se recibe un mensaje MQTT
def on_message(client, userdata, msg):
    global last_temp_event_time, last_hum_event_time
    try:
        # Decodificar el mensaje en UTF-8 y manejar errores
        data = msg.payload.decode('utf-8', errors='ignore').split(',')
        if msg.topic == 'sensor/sht3x' and len(data) == 2:
            asyncio.run(handle_sht3x_message(data))
        elif msg.topic == 'sensor/gy302' and len(data) == 1:
            asyncio.run(handle_gy302_message(data))
        else:
            print("Datos recibidos en formato incorrecto")
    except Exception as e:
        print(f'Error al procesar el mensaje: {e}')

async def handle_sht3x_message(data):
    global last_temp_event_time, last_hum_event_time
    temperatura, humedad = float(data[0]), float(data[1])  # Separar y convertir temperatura y humedad a float
    print(f'Temperatura: {temperatura}C, Humedad: {humedad}')  # Imprimir datos en consola
    await save_sht3x_data(temperatura, humedad)  # Guardar datos en la base de datos
    current_time = time.time()

    # Obtener parametros ideales
    ideal_temp_params = await get_ideal_params('temperatura')
    ideal_humidity_params = await get_ideal_params('humedad')

    if not ideal_temp_params or not ideal_humidity_params:
        print("No se encontraron parametros ideales")
        return

    min_temp = ideal_temp_params['min_value']
    max_temp = ideal_temp_params['max_value']
    min_humidity = ideal_humidity_params['min_value']
    max_humidity = ideal_humidity_params['max_value']

    # Verificar si la temperatura o la humedad estan fuera de los parametros
    if not (min_temp <= temperatura <= max_temp):  # Rango de temperatura aceptable
        if current_time - last_temp_event_time > 60:
            await save_event(f"Advertencia! Temperatura fuera de rango: {temperatura} C (Ideal: {min_temp}-{max_temp} C)", "temperatura")
            last_temp_event_time = current_time
    if not (min_humidity <= humedad <= max_humidity):  # Rango de humedad aceptable
        if current_time - last_hum_event_time > 60:
            await save_event(f"Advertencia! Humedad fuera de rango: {humedad} % (Ideal: {min_humidity}-{max_humidity} %)", "humedad")
            last_hum_event_time = current_time

    # Verificar el estado de la aplicación
    app_state = await get_app_state()
    if app_state == 'automatico':
        await update_actuators(temperatura, humedad)

async def update_actuators(temperature, humidity):
    # Obtener parametros ideales
    ideal_temp_params = await get_ideal_params('temperatura')
    ideal_humidity_params = await get_ideal_params('humedad')

    if not ideal_temp_params or not ideal_humidity_params:
        print("No se encontraron parametros ideales")
        return

    min_temp = ideal_temp_params['min_value']
    max_temp = ideal_temp_params['max_value']
    min_humidity = ideal_humidity_params['min_value']
    max_humidity = ideal_humidity_params['max_value']

    # Validar temperatura
    if temperature < min_temp:
        await update_actuator_and_log(1, 'true', "Temperatura baja", 'raspberry/light')
        await update_actuator_and_log(2, 'false', "Ventilador apagado", 'raspberry/fan')
    elif temperature > max_temp:
        await update_actuator_and_log(1, 'false', "Temperatura alta", 'raspberry/light')
        await update_actuator_and_log(2, 'true', "Ventilador encendido", 'raspberry/fan')
    else:
        await update_actuator_and_log(1, 'false', "Temperatura normal", 'raspberry/light')
        await update_actuator_and_log(2, 'false', "Ventilador apagado", 'raspberry/fan')

    # Validar humedad
    if humidity < min_humidity:
        await update_actuator_and_log(3, 'true', "Humedad baja", 'raspberry/humidifier')
        await update_actuator_and_log(4, 'false', "Motor apagado", 'raspberry/motor')
    elif humidity > max_humidity:
        await update_actuator_and_log(3, 'false', "Humedad alta", 'raspberry/humidifier')
        await update_actuator_and_log(4, 'true', "Motor encendido", 'raspberry/motor')
    else:
        await update_actuator_and_log(3, 'false', "Humedad normal", 'raspberry/humidifier')
        await update_actuator_and_log(4, 'false', "Motor apagado", 'raspberry/motor')

async def update_actuator_and_log(actuator_id, state, description, topic):
    current_state = await get_actuator_state(actuator_id)
    if current_state != state:
        await update_actuator_state(actuator_id, state)
        await publish_message(topic, str(state).lower())
        print(f'{description}: {state}')

async def handle_gy302_message(data):
    nivel_luz = data[0]  # Nivel de luz
    print(f'Nivel de luz: {nivel_luz} lx')  # Imprimir datos en consola
    await save_gy302_data(nivel_luz)  # Guardar datos en la base de datos

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
    client.connect('localhost', 1883, 60)  # Conectarse al broker local de la Raspberry
    client.subscribe('sensor/sht3x')  # Suscribirse al topico donde la Raspberry publica
    client.subscribe('sensor/gy302')  # Suscribirse al topico donde se publican los datos del GY-302
    client.loop_start()  # Iniciar el loop en segundo plano para recibir mensajes
