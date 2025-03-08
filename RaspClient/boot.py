# -*- coding: utf-8 -*-
from config.wifi_config import connect_wifi
from config.mqtt_config import connect_mqtt
from actuators.light import control_light
from actuators.fan import control_fan  # Importar la funcion para controlar el ventilador
from sensors.bmp280 import publish_bmp280_data
from sensors.gy302 import publish_gy302_data
from sensors.sht3x import publish_sht3x_data  # Importar la funcion para publicar datos del sensor SHT3x
from config import config
import time
import threading

# Funcion de callback para manejar mensajes MQTT
def on_message(client, userdata, message):  # Modificar para aceptar los argumentos adicionales
    print(f"Mensaje recibido en el topico {message.topic}: {message.payload.decode('utf-8')}")
    if message.topic == config.TOPIC_LIGHT:
        state = message.payload.decode('utf-8')
        control_light(state)
    elif message.topic == config.TOPIC_FAN:  # Manejar el topico del ventilador
        state = message.payload.decode('utf-8')
        control_fan(state)

# Funcion para manejar la conexion MQTT y recibir mensajes
def mqtt_loop(client):
    while True:
        try:
            client.loop()  # Verificar si hay nuevos mensajes
        except OSError as e:
            print("Error en el loop MQTT:", str(e)) # Mensaje de error
            client = connect_mqtt()  # Intentar reconectar si falla la conexion MQTT
        time.sleep(1)  # Esperar 1 segundo antes de verificar nuevamente

# Funcion para publicar datos del sensor BMP280
def bmp280_loop(client):
    while True:
        try:
            publish_bmp280_data(client, config.TOPIC_BMP280)  # Publicar datos del sensor BMP280
        except OSError as e:
            print("Error en el loop de sensores BMP280:", str(e)) # Mensaje de error
        time.sleep(5)  # Esperar 5 segundos entre publicaciones

# Funcion para publicar datos del sensor GY-302
def gy302_loop(client):
    while True:
        try:
            publish_gy302_data(client, config.TOPIC_GY302)  # Publicar datos del sensor GY-302
        except OSError as e:
            print("Error en el loop de sensores GY-302:", str(e)) # Mensaje de error
        time.sleep(5)  # Esperar 5 segundos entre publicaciones

# Funcion para publicar datos del sensor SHT3x
def sht3x_loop(client):
    while True:
        try:
            publish_sht3x_data(client, config.TOPIC_SHT3X)  # Publicar datos del sensor SHT3x
        except OSError as e:
            print("Error en el loop de sensores SHT3x:", str(e))  # Mensaje de error
        time.sleep(5)  # Esperar 5 segundos entre publicaciones

# Funcion principal del programa
def main():
    # Intentar conectarse al Wi-Fi
    if connect_wifi(): # Si se conecta correctamente al Wi-Fi
        client = connect_mqtt()  # Intentar conectar al broker MQTT
        if client:  # Si se conecta correctamente al broker
            client.on_message = on_message  # Configurar callback de mensajes
            client.subscribe(config.TOPIC_LIGHT)  # Suscribirse al topico para controlar la luz
            client.subscribe(config.TOPIC_FAN)  # Suscribirse al topico para controlar el ventilador
            # Iniciar hilos para manejar MQTT y sensores
            threading.Thread(target=mqtt_loop, args=(client,)).start()
            threading.Thread(target=bmp280_loop, args=(client,)).start()  # Iniciar hilo para BMP280
            threading.Thread(target=gy302_loop, args=(client,)).start()  # Iniciar hilo para GY-302
            threading.Thread(target=sht3x_loop, args=(client,)).start()  # Iniciar hilo para SHT3x
            while True:
                time.sleep(1)  # Mantener el programa principal en ejecucion
        else:
            print("No se pudo conectar al broker MQTT.")
    else:
        print("No se pudo conectar a la red Wi-Fi.")

# Ejecutar el programa principal
if __name__ == "__main__":
    main()
