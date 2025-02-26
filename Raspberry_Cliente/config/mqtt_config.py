import paho.mqtt.client as mqtt
from config import config
import time

def connect_mqtt():
    client = mqtt.Client()
    while True:
        try:
            client.connect(config.SERVER, 1883, 60)
            print("Conexion al broker MQTT establecida")
            return client
        except OSError as e:
            print("No se pudo conectar al broker MQTT. Intentando de nuevo en 5 segundos...")
            time.sleep(5)
