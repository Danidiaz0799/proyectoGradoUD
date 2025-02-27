import paho.mqtt.client as mqtt
from models.sensor_data import save_sensor_data
from models.event import save_event  # Importar la funcion para guardar eventos
import time

client = None
last_temp_event_time = 0
last_hum_event_time = 0

# Funcion de callback cuando se recibe un mensaje MQTT
def on_message(client, userdata, msg):
    global last_temp_event_time, last_hum_event_time
    try:
        # Decodificar el mensaje en UTF-8 y manejar errores
        data = msg.payload.decode('utf-8', errors='ignore').split(',')
        if msg.topic == 'sensor/dht11' and len(data) == 2:
            temperatura, humedad = data[0], data[1]  # Separar temperatura y humedad
            print(f'Temperatura: {temperatura}C, Humedad: {humedad}')  # Imprimir datos en consola
            save_sensor_data(temperatura, humedad)  # Guardar datos en la base de datos
            current_time = time.time()
            # Verificar si la temperatura o la humedad estan fuera de los parametros
            if not (20 <= float(temperatura) <= 30):  # Rango de temperatura aceptable
                if current_time - last_temp_event_time > 60:
                    save_event(f"Advertencia: Temperatura fuera de rango - {temperatura}", "temperatura")
                    last_temp_event_time = current_time
            if not (60 <= float(humedad) <= 90):  # Rango de humedad aceptable
                if current_time - last_hum_event_time > 60:
                    save_event(f"Advertencia: Humedad fuera de rango - {humedad}", "humedad")
                    last_hum_event_time = current_time
        elif msg.topic == 'sensor/bmp280' and len(data) == 2:
            temperatura, presion = data[0], data[1]  # Separar temperatura y presión
            print(f'Temperatura: {temperatura}C, Presion: {presion}hPa')  # Imprimir datos en consola
        elif msg.topic == 'sensor/gy302' and len(data) == 1:
            nivel_luz = data[0]  # Nivel de luz
            print(f'Nivel de luz: {nivel_luz} lx')  # Imprimir datos en consola
        else:
            print("Datos recibidos en formato incorrecto")
    except Exception as e:
        print(f'Error al procesar el mensaje: {e}')

# Funcion para publicar mensajes MQTT
def publish_message(topic, message):
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
    client.subscribe('sensor/dht11')  # Suscribirse al topico donde el ESP32 publica
    client.subscribe('sensor/bmp280')  # Suscribirse al topico donde se publican los datos del BMP280
    client.subscribe('sensor/gy302')  # Suscribirse al topico donde se publican los datos del GY-302
    client.loop_start()  # Iniciar el loop en segundo plano para recibir mensajes
