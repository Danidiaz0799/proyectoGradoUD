import paho.mqtt.client as mqtt
from models.sensor_data import save_sensor_data

# Función de callback cuando se recibe un mensaje MQTT
def on_message(client, userdata, msg):
    try:
        # Decodificar el mensaje en UTF-8 y manejar errores
        data = msg.payload.decode('utf-8', errors='ignore').split(',')
        if len(data) == 2:
            temperatura, humedad = data[0], data[1]  # Separar temperatura y humedad
            save_sensor_data(temperatura, humedad)  # Guardar datos en la base de datos
        print(f'Temperatura: {temperatura}, Humedad: {humedad}')
    except Exception as e:
        print(f'Error al procesar el mensaje: {e}')

# Configuración del cliente MQTT
def connect_mqtt():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect('localhost', 1883, 60)  # Conectarse al broker local de la Raspberry
    client.subscribe('temperatura_humedad')  # Suscribirse al tópico donde el ESP32 publica
    client.loop_start()  # Iniciar el loop en segundo plano para recibir mensajes
