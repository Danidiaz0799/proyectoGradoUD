from config.wifi_config import connect_wifi
from config.mqtt_config import connect_mqtt
from sensors.sensor_config import publish_sensor_data
from config import config
import time
from machine import Pin
import _thread

# Configuracion del pin de la luz del ESP32
light_pin = Pin(2, Pin.OUT)  # Pin al que esta conectada la luz del ESP32

# Funcion de callback para manejar mensajes MQTT
def on_message(topic, msg):
    if topic == b'esp32/light':
        state = msg.decode('utf-8')
        light_pin.value(1 if state == 'true' else 0)  # Encender o apagar la luz

# Funcion para manejar la conexion MQTT y recibir mensajes
def mqtt_loop(client):
    while True:
        try:
            client.check_msg()  # Verificar si hay nuevos mensajes
        except OSError as e:
            print("Error en el loop MQTT:", str(e))
            client = connect_mqtt()  # Intentar reconectar si falla la conexion MQTT
        time.sleep(1)  # Esperar 1 segundo antes de verificar nuevamente

# Funcion para publicar datos del sensor
def sensor_loop(client):
    while True:
        try:
            publish_sensor_data(client, config.TOPIC)  # Publicar datos del sensor
        except OSError as e:
            print("Error en el loop de sensores:", str(e))
        time.sleep(5)  # Esperar 5 segundos entre publicaciones

# Funcion principal del programa
def main():
    # Intentar conectarse al Wi-Fi
    if connect_wifi():
        client = connect_mqtt()  # Intentar conectar al broker MQTT
        if client:  # Si se conecta correctamente al broker
            client.set_callback(on_message)  # Configurar callback de mensajes
            client.subscribe(b'esp32/light')  # Suscribirse al topico para controlar la luz
            # Iniciar hilos para manejar MQTT y sensores
            _thread.start_new_thread(mqtt_loop, (client,))
            _thread.start_new_thread(sensor_loop, (client,))
            while True:
                time.sleep(1)  # Mantener el programa principal en ejecucion
        else:
            print("No se pudo conectar al broker MQTT.")
    else:
        print("No se pudo conectar a la red Wi-Fi.")

# Ejecutar el programa principal
main()
