# -*- coding: utf-8 -*-
import time
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

    while True:
        temperature = bmp280.temperature
        pressure = bmp280.pressure
        print(f"Temperatura: {temperature:.2f} C")
        print(f"Presion: {pressure:.2f} hPa")
        time.sleep(2)
except Exception as e:
    print(f"Error al inicializar o leer el sensor BMP280: {e}")
