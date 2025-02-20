from config.wifi_config import connect_wifi
from config.mqtt_config import connect_mqtt
from sensors.sensor_config import publish_sensor_data
from config import config
import time

# Función principal del programa
def main():
    # Intentar conectarse al Wi-Fi
    if connect_wifi():
        client = connect_mqtt()  # Intentar conectar al broker MQTT
        if client:  # Si se conecta correctamente al broker
            while True:
                try:
                    publish_sensor_data(client, config.TOPIC)  # Publicar datos del sensor
                except OSError as e:
                    print("Error en el loop principal:", str(e))
                    client = connect_mqtt()  # Intentar reconectar si falla la conexión MQTT
                time.sleep(5)  # Esperar 5 segundos entre publicaciones
        else:
            print("No se pudo conectar al broker MQTT.")
    else:
        print("No se pudo conectar a la red Wi-Fi.")

# Ejecutar el programa principal
main()
