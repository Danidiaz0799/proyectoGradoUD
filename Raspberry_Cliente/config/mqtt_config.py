import paho.mqtt.client as mqtt

def connect_mqtt():
    client = mqtt.Client()
    client.username_pw_set("StevPro", "tu_contraseña")
    client.connect("tu_broker_mqtt", 1883, 60)
    
    return client
