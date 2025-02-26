import Adafruit_DHT
import time

# Configuracion del sensor DHT11
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4  # Pin GPIO al que esta conectado el sensor DHT11

def read_sensor():
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        return {'temperature': temperature, 'humidity': humidity}
    else:
        return None

def publish_sensor_data(client, topic):
    sensor_data = read_sensor()
    if sensor_data:
        temp = sensor_data['temperature']
        hum = sensor_data['humidity']
        message = '{0},{1}'.format(temp, hum).encode('utf-8')  # Formato del mensaje y conversion a bytes
        client.publish(topic, message)  # Publicar los datos al topico
        print("Datos publicados:", message)
    else:
        print("Error al leer los datos del sensor")
