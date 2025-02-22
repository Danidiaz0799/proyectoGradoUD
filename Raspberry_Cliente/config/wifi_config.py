import subprocess
from config import config

def connect_wifi():
    ssid = config.SSID
    password = config.PASSWORD
    
    try:
        # Escanear redes Wi-Fi disponibles
        result = subprocess.run(['nmcli', 'dev', 'wifi'], capture_output=True, text=True, check=True)
        print("Redes Wi-Fi disponibles:")
        print(result.stdout)
        
        # Conectar a la red Wi-Fi
        subprocess.run(['sudo', 'nmcli', 'd', 'wifi', 'connect', ssid, 'password', password], check=True)
        print("Conexion Wi-Fi establecida")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error al conectar a la red Wi-Fi: {e}")
        return False
