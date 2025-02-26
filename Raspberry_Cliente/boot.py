# -*- coding: utf-8 -*-
from config.wifi_config import connect_wifi
from config.mqtt_config import connect_mqtt
from sensors.dht11 import publish_sensor_data
from config import config
import time
import threading
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM) # Configuracion del pin de la luz de la Raspberry Pi
GPIO.setwarnings(False)  # Desactivar advertencias de GPIO
light_pin = 2  # Pin al que esta conectada la luz de la Raspberry Pi
GPIO.setup(light_pin, GPIO.OUT) # Se configura el pin como salida

# Funcion de callback para manejar mensajes MQTT
def on_message(client, userdata, message):
    print(f"Mensaje recibido en el topico {message.topic}: {message.payload.decode('utf-8')}") # Mensaje de depuración
    if message.topic == config.TOPIC_LIGHT:
        state = message.payload.decode('utf-8') # Obtener el estado de la luz
        GPIO.output(light_pin, GPIO.HIGH if state == 'true' else GPIO.LOW)  # Encender o apagar la luz

# Funcion para manejar la conexion MQTT y recibir mensajes
def mqtt_loop(client):
    while True:
        try:
            client.loop()  # Verificar si hay nuevos mensajes
        except OSError as e:
            print("Error en el loop MQTT:", str(e)) # Mensaje de error
            client = connect_mqtt()  # Intentar reconectar si falla la conexion MQTT
        time.sleep(1)  # Esperar 1 segundo antes de verificar nuevamente

# Funcion para publicar datos del sensor DHT11
def sensor_loop(client):
    while True:
        try:
            publish_sensor_data(client, config.TOPIC_SENSOR)  # Publicar datos del sensor DHT11
        except OSError as e:
            print("Error en el loop de sensores DHT11:", str(e)) # Mensaje de error
        time.sleep(5)  # Esperar 5 segundos entre publicaciones

# Funcion principal del programa
def main():
    # Intentar conectarse al Wi-Fi
    if connect_wifi(): # Si se conecta correctamente al Wi-Fi
        client = connect_mqtt()  # Intentar conectar al broker MQTT
        if client:  # Si se conecta correctamente al broker
            client.on_message = on_message  # Configurar callback de mensajes
            client.subscribe(config.TOPIC_LIGHT)  # Suscribirse al topico para controlar la luz
            print("Suscrito al topico de control de luz")
            # Iniciar hilos para manejar MQTT y sensores
            threading.Thread(target=mqtt_loop, args=(client,)).start()
            threading.Thread(target=sensor_loop, args=(client,)).start()
            while True:
                time.sleep(1)  # Mantener el programa principal en ejecucion
        else:
            print("No se pudo conectar al broker MQTT.")
    else:
        print("No se pudo conectar a la red Wi-Fi.")

# Ejecutar el programa principal
if __name__ == "__main__":
    main()
