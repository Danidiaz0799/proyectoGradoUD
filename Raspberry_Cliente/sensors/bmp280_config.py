import board
import busio
import adafruit_bmp280

print("Iniciando configuracion del sensor BMP280")

# Configuracion del sensor BMP280
try:
    print("Configurando I2C")
    i2c = busio.I2C(board.SCL, board.SDA)
    print("I2C configurado correctamente")
    
    print("Inicializando BMP280")
    bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x76)  # Especificar la direccion I2C correcta
    print("BMP280 inicializado correctamente")
    
    # Configurar la presión a nivel del mar
    bmp280.sea_level_pressure = 1013.25
except Exception as e:
    bmp280 = None
    print(f"Error al inicializar el sensor BMP280: {e}")

def read_bmp280():
    if bmp280 is None:
        print("El sensor BMP280 no esta inicializado")
        return None
    try:
        temperature = bmp280.temperature
        pressure = bmp280.pressure
        return {'temperature': temperature, 'pressure': pressure}
    except Exception as e:
        print(f"Error al leer los datos del sensor BMP280: {e}")
        return None

def publish_bmp280_data(client, topic):
    sensor_data = read_bmp280()
    if sensor_data:
        temp = sensor_data['temperature']
        pres = sensor_data['pressure']
        message = '{0},{1}'.format(temp, pres).encode('utf-8')  # Formato del mensaje y conversion a bytes
        client.publish(topic, message)  # Publicar los datos al topico
        print("Datos publicados:", message)
    else:
        print("Error al leer los datos del sensor BMP280")
