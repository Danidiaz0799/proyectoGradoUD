# Configuracion de la red Wi-Fi
SSID = 'Claro_00BF1E'  # Nombre de la red Wi-Fi
PASSWORD = 'Z2N2R2C4D9H3'  # Contrasena de la red Wi-Fi

# Configuracion del cliente MQTT
SERVER = '192.168.20.44'  # IP del servidor MQTT (Raspberry Pi)
CLIENT_ID = 'ESP32_DHT11_Sensor'  # ID del cliente MQTT
TOPIC_SENSOR = 'temperatura_humedad'  # Topico donde se publicaran los datos del sensor DHT11
TOPIC_LIGHT = 'raspberry/light'  # Topico para controlar la luz
