import smbus

# Configuración del sensor GY-302
I2C_PORT = 1
GY302_ADDRESS = 0x23

def read_gy302():
    bus = smbus.SMBus(I2C_PORT)
    data = bus.read_i2c_block_data(GY302_ADDRESS, 0x10, 2)
    light_level = (data[1] + (256 * data[0])) / 1.2
    return {'light_level': light_level}

def publish_gy302_data(client, topic):
    sensor_data = read_gy302()
    if sensor_data:
        light_level = sensor_data['light_level']
        message = '{0}'.format(light_level).encode('utf-8')
        client.publish(topic, message)
        print("Datos GY-302 publicados:", message)
    else:
        print("Error al leer los datos del sensor GY-302")
