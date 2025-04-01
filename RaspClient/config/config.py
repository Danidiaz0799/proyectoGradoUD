# Configuracion de la red Wi-Fi
SSID = 'Stev7'  # Nombre de la red Wi-Fi
PASSWORD = 'hola12345'  # Contrasena de la red Wi-Fi

TOPIC_URL = 'mushroom1/'

# Configuracion del cliente MQTT
SERVER = '192.168.137.214'  # IP del servidor MQTT (Raspberry Pi)
TOPIC_FAN = TOPIC_URL + 'fan'  # Topico para controlar el ventilador
TOPIC_LIGHT = TOPIC_URL + 'light'  # Topico para controlar la luz
TOPIC_HUMIDIFIER = 'humidifier'  # Topico para controlar el humidificador
TOPIC_MOTOR = TOPIC_URL + 'motor'  # Topico para controlar el motor
TOPIC_GY302 = TOPIC_URL + 'sensor/gy302'
TOPIC_SHT3X = TOPIC_URL + 'sensor/sht3x'  # Topico donde se publicaran los datos del sensor SHT3x
