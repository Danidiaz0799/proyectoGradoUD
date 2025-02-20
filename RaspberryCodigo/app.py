# -*- coding: utf-8 -*-
from flask import Flask, send_from_directory
from flask_cors import CORS
from routes.sensor_routes import sensor_bp
from routes.event_routes import event_bp
from routes.actuator_routes import actuator_bp
from mqtt_client import connect_mqtt
import os

# Configuracion de la carpeta donde esta la app Angular
ANGULAR_BUILD_FOLDER = "/home/stevpi/Desktop/proyectoGradoUD/angular_app/dist/mushroom-automation"

# Crear la aplicacion Flask
app = Flask(__name__, static_folder=ANGULAR_BUILD_FOLDER)
CORS(app, resources={r"/*": {"origins": "*"}})  # Permitir acceso desde cualquier origen

# Registrar Blueprints para modularizar las rutas
app.register_blueprint(sensor_bp)
app.register_blueprint(event_bp)
app.register_blueprint(actuator_bp)

# Ruta para servir archivos estaticos (JS, CSS, imagenes, etc.)
@app.route('/<path:filename>')
def serve_static_files(filename):
    file_path = os.path.join(ANGULAR_BUILD_FOLDER, filename)
    # Si el archivo existe, lo sirve normalmente
    if os.path.isfile(file_path):
        return send_from_directory(ANGULAR_BUILD_FOLDER, filename)
    # Si no existe, devolver el index.html (manejo de rutas SPA)
    return send_from_directory(ANGULAR_BUILD_FOLDER, 'index.html')

# Ruta para servir la pagina principal
@app.route('/')
def serve_index():
    return send_from_directory(ANGULAR_BUILD_FOLDER, 'index.html')

# Iniciar la aplicacion
if __name__ == '__main__':
    connect_mqtt()  # Conectar al broker MQTT
    app.run(host='0.0.0.0', port=5000)  # Modo produccion sin debug
