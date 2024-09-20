import network
from umqtt.simple import MQTTClient
import dht
from machine import Pin
import time

# Configuración de la red Wi-Fi
ssid = 'PocoPro'  # Nombre de la red Wi-Fi
password = 'Hola1234567'  # Contraseña de la red Wi-Fi

# Configuración del cliente MQTT
server = '192.168.33.214'  # IP del servidor MQTT (Raspberry Pi)
client_id = 'ESP32_DHT11_Sensor'  # ID del cliente MQTT
topic = b'temperatura_humedad'  # Tópico donde se publicarán los datos

# Configuración del sensor DHT11
sensor_pin = Pin(13, Pin.IN, Pin.PULL_UP)  # Pin al que está conectado el sensor DHT11
sensor = dht.DHT11(sensor_pin)  # Inicialización del sensor

# Función para conectar al Wi-Fi con manejo de reconexión
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)  # Modo Wi-Fi como estación (STA_IF)
    wlan.active(True)  # Activar la interfaz Wi-Fi
    if not wlan.isconnected():
        print('Conectando a la red:', ssid)
        wlan.connect(ssid, password)  # Intentar conectarse a la red Wi-Fi
        timeout = 10  # Tiempo de espera máximo para la conexión
        start_time = time.time()
        while not wlan.isconnected():
            if time.time() - start_time > timeout:
                print('Tiempo de espera excedido. Verifique la red o la configuración.')
                return False
            time.sleep(1)
    print('Conectado a la red. IP:', wlan.ifconfig()[0])  # IP asignada al ESP32
    return True

# Función para conectar al broker MQTT con manejo de reconexión
def connect_mqtt():
    try:
        mqtt_client = MQTTClient(client_id, server)  # Crear cliente MQTT
        mqtt_client.connect()  # Conectar al broker MQTT
        print("Conectado al broker MQTT")
    except Exception as e:
        print("Error al conectar al broker MQTT:", str(e))
        return None  # Retornar None si no se puede conectar
    return mqtt_client

# Función para publicar datos del sensor (temperatura y humedad) al tópico MQTT
def publish_sensor_data(client):
    try:
        sensor.measure()  # Medir los valores de temperatura y humedad
        temp = sensor.temperature()  # Obtener temperatura
        hum = sensor.humidity()  # Obtener humedad
        message = b'{0},{1}'.format(temp, hum)  # Formato del mensaje
        client.publish(topic, message)  # Publicar los datos al tópico
        print("Datos publicados:", message)
    except OSError as e:
        print("Error al leer el sensor:", str(e))  # Error de lectura del sensor
    except Exception as e:
        print("Error al publicar datos:", str(e))  # Error al publicar los datos

# Función principal del programa
def main():
    # Intentar conectarse al Wi-Fi
    if connect_wifi():
        client = connect_mqtt()  # Intentar conectar al broker MQTT
        if client:  # Si se conecta correctamente al broker
            while True:
                try:
                    publish_sensor_data(client)  # Publicar datos del sensor
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
