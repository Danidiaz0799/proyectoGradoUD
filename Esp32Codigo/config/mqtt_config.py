from umqtt.simple import MQTTClient
from config import config

# Funcion para conectar al broker MQTT con manejo de reconexion
def connect_mqtt():
    try:
        mqtt_client = MQTTClient(config.CLIENT_ID, config.SERVER)  # Crear cliente MQTT
        mqtt_client.connect()  # Conectar al broker MQTT
        print("Conectado al broker MQTT")
    except Exception as e:
        print("Error al conectar al broker MQTT:", str(e))
        return None  # Retornar None si no se puede conectar
    return mqtt_client  # Retornar el cliente MQTT si la conexion es exitosa
