# -*- coding: utf-8 -*-
import smbus
import time

# Direccion I2C del sensor GY-302
DEVICE = 0x23

# Modos de medicion
POWER_DOWN = 0x00
POWER_ON = 0x01
RESET = 0x07
CONTINUOUS_HIGH_RES_MODE_1 = 0x10

bus = smbus.SMBus(1)  # Para Raspberry Pi 1, Model B rev 1, usa bus = smbus.SMBus(0)

def read_light(addr=DEVICE):
    try:
        data = bus.read_i2c_block_data(addr, CONTINUOUS_HIGH_RES_MODE_1)
        return convert_to_number(data)
    except OSError as e:
        print(f"Error de entrada/salida: {e}")
        return None

def convert_to_number(data):
    result = (data[1] + (256 * data[0])) / 1.2
    return result

try:
    while True:
        light_level = read_light()
        if light_level is not None:
            print(f"Nivel de luz: {light_level} lx")
        else:
            print("Error al leer el nivel de luz")
        time.sleep(5)  # Leer cada 5 segundos

except KeyboardInterrupt:
    print("Medicion detenida por el usuario")
