import Adafruit_DHT
import time
import board
import busio
import adafruit_bmp280

# Configuracion del sensor DHT11
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4  # Pin GPIO al que esta conectado el sensor DHT11

# Configuracion del sensor BMP280
i2c = busio.I2C(board.SCL, board.SDA)
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x76)
bmp280.sea_level_pressure = 1013.25

def read_dht11():
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        return {'temperature': temperature, 'humidity': humidity}
    else:
        return None

def read_bmp280():
    try:
        temperature = bmp280.temperature
        pressure = bmp280.pressure
        return {'temperature': temperature, 'pressure': pressure}
    except Exception as e:
        print(f"Error al leer el sensor BMP280: {e}")
        return None

def publish_sensor_data(client, topic, sensor_data):
    if sensor_data:
        message = ','.join(f"{key}:{value}" for key, value in sensor_data.items()).encode('utf-8')
        client.publish(topic, message)
        print("Datos publicados:", message)
    else:
        print("Error al leer los datos del sensor")
