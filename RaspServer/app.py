# -*- coding: utf-8 -*-
from flask import Flask, send_from_directory
from flask_cors import CORS
from routes.client_routes import client_bp
from routes.sensor_routes import sensor_bp
from routes.event_routes import event_bp
from routes.actuator_routes import actuator_bp
from routes.app_state_routes import app_state_bp  # Corregido el nombre de la importación
from routes.statistics_routes import statistics_bp
from mqtt_client import connect_mqtt
import os

# Configuracion de la carpeta donde esta la app Angular
ANGULAR_BUILD_FOLDER = "/home/stevpi/Desktop/raspServer/angular_app/dist/mushroom-automation"

# Crear la aplicacion Flask
app = Flask(__name__, static_folder=ANGULAR_BUILD_FOLDER)
CORS(app, resources={r"/*": {"origins": "*"}})  # Permitir acceso desde cualquier origen

# Registrar Blueprints para modularizar las rutas - El orden es importante
# Primero registrar las rutas API específicas, luego las más genéricas
app.register_blueprint(client_bp, url_prefix='/api')
app.register_blueprint(sensor_bp, url_prefix='/api')
app.register_blueprint(event_bp, url_prefix='/api')
app.register_blueprint(actuator_bp, url_prefix='/api')
app.register_blueprint(app_state_bp, url_prefix='/api')  # Corregido el nombre del blueprint
app.register_blueprint(statistics_bp, url_prefix='/api')

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
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_index(path):
    # Evitar conflictos con rutas API
    if path.startswith('api/'):
        return {"error": "No encontrado"}, 404
    return send_from_directory(ANGULAR_BUILD_FOLDER, 'index.html')

# Iniciar la aplicacion
if __name__ == '__main__':
    connect_mqtt()  # Conectar al broker MQTT
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
