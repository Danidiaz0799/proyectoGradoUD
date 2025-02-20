import network
import time
from config import config

# Función para conectar al Wi-Fi con manejo de reconexión
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)  # Modo Wi-Fi como estación (STA_IF)
    wlan.active(True)  # Activar la interfaz Wi-Fi
    if not wlan.isconnected():
        print('Conectando a la red:', config.SSID)
        wlan.connect(config.SSID, config.PASSWORD)  # Intentar conectarse a la red Wi-Fi
        timeout = 10  # Tiempo de espera máximo para la conexión
        start_time = time.time()
        while not wlan.isconnected():
            if time.time() - start_time > timeout:
                print('Tiempo de espera excedido. Verifique la red o la configuración.')
                return False
            time.sleep(1)
    print('Conectado a la red. IP:', wlan.ifconfig()[0])  # IP asignada al ESP32
    return True
