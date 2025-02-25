import Adafruit_DHT

# Configuracion del sensor DHT11
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4  # Pin GPIO al que esta conectado el sensor DHT11

# Funcion para leer los datos del sensor DHT11
def read_dht11():
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        return {'temperature': temperature, 'humidity': humidity}
    else:
        return None
