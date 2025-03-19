import time
import board
import busio
import adafruit_sht31d
from actuators.oled import display_data  # Importar la funcion para mostrar datos en la pantalla OLED

# Configuracion del sensor SHT3x
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_sht31d.SHT31D(i2c, address=0x44)  # Especificar la direccion I2C

def read_sht3x():
    temperature = sensor.temperature
    humidity = sensor.relative_humidity
    return {'temperature': temperature, 'humidity': humidity}

def publish_sht3x_data(client, topic):
    sensor_data = read_sht3x()
    if sensor_data:
        temperature = sensor_data['temperature']
        humidity = sensor_data['humidity']
        message = '{0},{1}'.format(temperature, humidity).encode('utf-8')
        client.publish(topic, message)
        print("Datos SHT3x publicados:", message, "en el topico:", topic)
        display_data(temperature, humidity)  # Mostrar datos en la pantalla OLED
    else:
        print("Error al leer los datos del sensor SHT3x")
