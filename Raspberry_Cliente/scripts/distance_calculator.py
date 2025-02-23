# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time

# Configuracion de los pines GPIO
GPIO.setmode(GPIO.BCM)
TRIG = 23
ECHO = 24

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def calcular_distancia():
    # Asegurarse de que el TRIG este bajo al principio
    GPIO.output(TRIG, False)
    time.sleep(0.5)  # Reducir el tiempo de espera inicial

    # Enviar una senal de 10us para activar el sensor
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    # Medir el tiempo de ida y vuelta de la senal
    pulso_inicio = time.time()
    while GPIO.input(ECHO) == 0:
        pulso_inicio = time.time()

    pulso_fin = time.time()
    while GPIO.input(ECHO) == 1:
        pulso_fin = time.time()

    duracion_pulso = pulso_fin - pulso_inicio

    # Calcular la distancia (34300 cm/s es la velocidad del sonido)
    distancia = duracion_pulso * 17150

    # Limitar la distancia a un rango razonable
    if distancia > 400 or distancia < 2:
        distancia = -1  # Valor fuera de rango

    distancia = round(distancia, 2)

    return distancia

try:
    while True:
        distancias = []
        for _ in range(5):  # Tomar 5 mediciones y promediarlas
            dist = calcular_distancia()
            if dist != -1:
                distancias.append(dist)
            time.sleep(0.1)  # Pequeña pausa entre mediciones

        if distancias:
            distancia_promedio = sum(distancias) / len(distancias)
            print(f"Distancia promedio: {distancia_promedio} cm")
        else:
            print("Distancia fuera de rango")
        
        time.sleep(5)  # Cambiar el tiempo de espera a 5 segundos

except KeyboardInterrupt:
    print("Medicion detenida por el usuario")
    GPIO.cleanup()
