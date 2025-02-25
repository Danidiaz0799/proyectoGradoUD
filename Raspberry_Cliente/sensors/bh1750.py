import smbus
import time

# Configuracion del sensor BH1750
DEVICE = 0x23  # Direccion I2C del sensor BH1750
POWER_DOWN = 0x00  # No se usa actualmente
POWER_ON = 0x01  # No se usa actualmente
RESET = 0x07  # No se usa actualmente
CONTINUOUS_LOW_RES_MODE = 0x13
CONTINUOUS_HIGH_RES_MODE_1 = 0x10
CONTINUOUS_HIGH_RES_MODE_2 = 0x11
ONE_TIME_HIGH_RES_MODE_1 = 0x20
ONE_TIME_HIGH_RES_MODE_2 = 0x21
ONE_TIME_LOW_RES_MODE = 0x23

bus = smbus.SMBus(1)  # Rev 2 Pi uses 1

def read_light(addr=DEVICE):
    data = bus.read_i2c_block_data(addr, ONE_TIME_HIGH_RES_MODE_1)
    return convert_to_number(data)

def convert_to_number(data):
    # Simplemente convierte 2 bytes de datos en un numero decimal
    return (data[1] + (256 * data[0])) / 1.2

def read_bh1750():
    try:
        light_level = read_light()
        return {'light': light_level}
    except Exception as e:
        print("Error al leer el sensor BH1750:", str(e))
        return None
