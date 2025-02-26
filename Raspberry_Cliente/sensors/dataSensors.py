# Importo los archivos individuales de cada Sensor
from config import config
from .dht11 import read_dht11

# Funcion para publicar los datos de los Sensores
def publish_sensor_data(client, topic):
    if topic == config.TOPIC_SENSOR_DHT11:  # Identificar el sensor DHT11 en el topic
        sensor_data = read_dht11()
    else:
        sensor_data = None

    if sensor_data:
        temp = sensor_data['temperature'] # Obtener la temperatura
        hum = sensor_data['humidity'] # Obtener la humedad
        message = '{0},{1}'.format(temp, hum).encode('utf-8')  # Formato del mensaje y conversion a bytes
        client.publish(topic, message)  # Publicar los datos al topico
        print("Datos publicados:", message) # Mensaje de depuración
    else:
        print("Error al leer los datos del sensor")