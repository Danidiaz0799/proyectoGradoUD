# Configuracion de la red Wi-Fi
SSID = 'Stev7'  # Nombre de la red Wi-Fi
PASSWORD = 'hola12345'  # Contrasena de la red Wi-Fi

# Identificación del cliente - Debe ser único para cada dispositivo
CLIENT_ID = 'mushroom1'  # Identificador único del cliente
CLIENT_NAME = 'Cultivo de Setas 1'  # Nombre descriptivo
CLIENT_DESCRIPTION = 'Cultivo principal de setas Orellana Rosada'  # Descripción

# Configuracion del cliente MQTT
SERVER = '192.168.137.214'  # IP del servidor MQTT (Raspberry Pi)

# Nuevos tópicos basados en el ID de cliente
TOPIC_PREFIX = f'clients/{CLIENT_ID}/'
TOPIC_REGISTER = f'{TOPIC_PREFIX}register'
TOPIC_FAN = f'{TOPIC_PREFIX}fan'
TOPIC_LIGHT = f'{TOPIC_PREFIX}light'
TOPIC_HUMIDIFIER = f'{TOPIC_PREFIX}humidifier'
TOPIC_MOTOR = f'{TOPIC_PREFIX}motor'
TOPIC_SHT3X = f'{TOPIC_PREFIX}sensor/sht3x'
