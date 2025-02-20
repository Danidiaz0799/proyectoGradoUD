import dht
from machine import Pin

# Configuracion del sensor DHT11
sensor_pin = Pin(13, Pin.IN, Pin.PULL_UP)  # Pin al que esta conectado el sensor DHT11
sensor = dht.DHT11(sensor_pin)  # Inicializacion del sensor

# Funcion para publicar datos del sensor (temperatura y humedad) al topico MQTT
def publish_sensor_data(client, topic):
    try:
        sensor.measure()  # Medir los valores de temperatura y humedad
        temp = sensor.temperature()  # Obtener temperatura
        hum = sensor.humidity()  # Obtener humedad
        message = b'{0},{1}'.format(temp, hum)  # Formato del mensaje
        client.publish(topic, message)  # Publicar los datos al topico
        print("Datos publicados:", message)
    except OSError as e:
        print("Error al leer el sensor:", str(e))  # Error de lectura del sensor
    except Exception as e:
        print("Error al publicar datos:", str(e))  # Error al publicar los datos
