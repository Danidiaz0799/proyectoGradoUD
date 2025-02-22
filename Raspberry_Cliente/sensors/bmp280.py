import time
import board
import busio
import adafruit_bmp280

# Configuracion del sensor BMP280
i2c = busio.I2C(board.SCL, board.SDA)
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x76)
bmp280.sea_level_pressure = 1013.25

def read_sensor():
    temperature = bmp280.temperature
    pressure = bmp280.pressure
    return {'temperature': temperature, 'pressure': pressure}

def publish_sensor_data(client, topic):
    sensor_data = read_sensor()
    if sensor_data:
        temp = sensor_data['temperature']
        pressure = sensor_data['pressure']
        message = '{0},{1}'.format(temp, pressure).encode('utf-8')
        client.publish(topic, message)
        print("Datos publicados:", message)
    else:
        print("Error al leer los datos del sensor BMP280")
