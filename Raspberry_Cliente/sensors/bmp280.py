import board
import busio
import adafruit_bmp280

# Configuración del sensor BMP280
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x76)

def read_bmp280():
    temperature = sensor.temperature
    pressure = sensor.pressure
    return {'temperature': temperature, 'pressure': pressure}

def publish_bmp280_data(client, topic):
    sensor_data = read_bmp280()
    if sensor_data:
        temp = sensor_data['temperature']
        pressure = sensor_data['pressure']
        message = '{0},{1}'.format(temp, pressure).encode('utf-8')
        client.publish(topic, message)
        print("Datos BMP280 publicados:", message, "en el topico:", topic)
    else:
        print("Error al leer los datos del sensor BMP280")
