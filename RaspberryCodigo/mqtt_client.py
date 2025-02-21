import paho.mqtt.client as mqtt
from models.sensor_data import save_sensor_data
from models.event import save_event  # Importar la función para guardar eventos

client = None

# Funcion de callback cuando se recibe un mensaje MQTT
def on_message(client, userdata, msg):
    try:
        # Decodificar el mensaje en UTF-8 y manejar errores
        data = msg.payload.decode('utf-8', errors='ignore').split(',')
        if len(data) == 2:
            temperatura, humedad = data[0], data[1]  # Separar temperatura y humedad
            save_sensor_data(temperatura, humedad)  # Guardar datos en la base de datos
            # Verificar si la temperatura o la humedad están fuera de los parámetros
            if not (20 <= float(temperatura) <= 30):  # Rango de temperatura aceptable
                save_event(f"Advertencia: Temperatura fuera de rango - {temperatura}")
            if not (60 <= float(humedad) <= 90):  # Rango de humedad aceptable
                save_event(f"Advertencia: Humedad fuera de rango - {humedad}")
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
    client.subscribe('temperatura_humedad')  # Suscribirse al topico donde el ESP32 publica
    client.loop_start()  # Iniciar el loop en segundo plano para recibir mensajes

# Conectar al cliente MQTT al iniciar el módulo
connect_mqtt()
