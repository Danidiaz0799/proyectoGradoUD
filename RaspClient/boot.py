# -*- coding: utf-8 -*-
from config.wifi_config import connect_wifi
from config.mqtt_config import connect_mqtt
from actuators.light import control_light
from actuators.fan import control_fan
from actuators.humidifier import control_humidifier
from actuators.motor import control_motor
from sensors.sht3x import publish_sht3x_data
from config import config
from actuators.oled import display_message
import time
import threading

# Función para registrar el cliente en el servidor
def register_client(client):
    registration_message = f"{config.CLIENT_NAME},{config.CLIENT_DESCRIPTION}"
    client.publish(config.TOPIC_REGISTER, registration_message)
    print(f"Cliente registrado: ID={config.CLIENT_ID}, Nombre={config.CLIENT_NAME}")

# Funcion de callback para manejar mensajes MQTT
def on_message(client, userdata, message):
    print(f"Mensaje recibido en el topico {message.topic}: {message.payload.decode('utf-8')}")
    if message.topic == config.TOPIC_LIGHT:
        state = message.payload.decode('utf-8')
        control_light(state)
    elif message.topic == config.TOPIC_FAN:
        state = message.payload.decode('utf-8')
        control_fan(state)
    elif message.topic == config.TOPIC_HUMIDIFIER:
        state = message.payload.decode('utf-8')
        control_humidifier(state)
    elif message.topic == config.TOPIC_MOTOR:
        state = message.payload.decode('utf-8')
        control_motor(state)

# Funcion para manejar la conexion MQTT y recibir mensajes
def mqtt_loop(client):
    while True:
        try:
            client.loop()  # Verificar si hay nuevos mensajes
        except OSError as e:
            print("Error en el loop MQTT:", str(e))
            client = connect_mqtt()  # Intentar reconectar si falla la conexion MQTT
            setup_mqtt_client(client)  # Reconfigurar el cliente
        time.sleep(1)  # Esperar 1 segundo antes de verificar nuevamente

# Configurar cliente MQTT con suscripciones y callbacks
def setup_mqtt_client(client):
    client.on_message = on_message
    client.subscribe(config.TOPIC_LIGHT)
    client.subscribe(config.TOPIC_FAN)
    client.subscribe(config.TOPIC_HUMIDIFIER)
    client.subscribe(config.TOPIC_MOTOR)
    register_client(client)  # Registrar el cliente al iniciar y reconectar

# Funcion para publicar datos del sensor SHT3x
def sht3x_loop(client):
    while True:
        try:
            publish_sht3x_data(client, config.TOPIC_SHT3X)
        except OSError as e:
            print("Error en el loop de sensores SHT3x:", str(e))
        time.sleep(5)

# Funcion principal del programa
def main():
    # Intentar conectarse al Wi-Fi
    display_message("Conectando a Wi-Fi...")
    if connect_wifi():
        display_message("Wi-Fi Conectado")
        client = connect_mqtt()
        if client:
            display_message(f"Conectado como {config.CLIENT_ID}")
            setup_mqtt_client(client)
            
            # Iniciar hilos para manejar MQTT y sensores
            threading.Thread(target=mqtt_loop, args=(client,)).start()
            threading.Thread(target=sht3x_loop, args=(client,)).start()
            
            # Periódicamente re-registrar el cliente para mantener el estado 'online'
            while True:
                register_client(client)
                time.sleep(60)  # Re-registrar cada minuto
        else:
            display_message("No se conecto a MQTT")
            print("No se pudo conectar al broker MQTT.")
    else:
        display_message("No se conecto a Wi-Fi")
        print("No se pudo conectar a la red Wi-Fi.")

# Ejecutar el programa principal
if __name__ == "__main__":
    main()
