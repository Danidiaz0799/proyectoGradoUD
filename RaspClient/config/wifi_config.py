import subprocess
from config import config

def connect_wifi():
    try:
        print("Intentando conectar a la red Wi-Fi...")
        result = subprocess.run(['sudo', 'nmcli', 'd', 'wifi', 'connect', config.SSID, 'password', config.PASSWORD], capture_output=True, text=True)
        if result.returncode == 0:
            print("Conexion Wi-Fi establecida")
            return True
        else:
            print(f"Error al conectar a la red Wi-Fi: {result.stderr}")
            return False
    except Exception as e:
        print(f"Excepcion al intentar conectar a la red Wi-Fi: {e}")
        return False
