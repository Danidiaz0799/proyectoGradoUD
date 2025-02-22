import paho.mqtt.client as mqtt
from config import config

def connect_mqtt():
    client = mqtt.Client(client_id=config.CLIENT_ID, protocol=mqtt.MQTTv311)  # Especificar la version de la API de callbacks
    client.username_pw_set("Claro_00BF1E", "Z2N2R2C4D9H3")
    client.connect(config.SERVER, 1883, 60)
    
    return client
