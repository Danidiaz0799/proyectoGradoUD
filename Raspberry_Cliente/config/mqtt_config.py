import paho.mqtt.client as mqtt
from config import config

def connect_mqtt():
    client = mqtt.Client(client_id=config.CLIENT_ID, protocol=mqtt.MQTTv311)
    client.connect(config.SERVER, 1883, 60)
    return client
