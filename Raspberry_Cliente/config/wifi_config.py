import network

def connect_wifi():
    ssid = "tu_ssid"
    password = "tu_password"
    
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(ssid, password)
    
    while not station.isconnected():
        pass
    
    print("Conexión Wi-Fi establecida")
    print(station.ifconfig())
    return True
