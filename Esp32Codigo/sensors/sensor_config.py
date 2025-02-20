import dht
from machine import Pin

# Configuración del sensor DHT11
sensor_pin = Pin(13, Pin.IN, Pin.PULL_UP)  # Pin al que está conectado el sensor DHT11
sensor = dht.DHT11(sensor_pin)  # Inicialización del sensor

# Función para publicar datos del sensor (temperatura y humedad) al tópico MQTT
def publish_sensor_data(client, topic):
    try:
        sensor.measure()  # Medir los valores de temperatura y humedad
        temp = sensor.temperature()  # Obtener temperatura
        hum = sensor.humidity()  # Obtener humedad
        message = b'{0},{1}'.format(temp, hum)  # Formato del mensaje
        client.publish(topic, message)  # Publicar los datos al tópico
        print("Datos publicados:", message)
    except OSError as e:
        print("Error al leer el sensor:", str(e))  # Error de lectura del sensor
    except Exception as e:
        print("Error al publicar datos:", str(e))  # Error al publicar los datos
