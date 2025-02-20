# -*- coding: utf-8 -*-

from flask import Flask
from flask_cors import CORS
from routes.sensor_routes import sensor_bp
from routes.event_routes import event_bp
from routes.actuator_routes import actuator_bp
from mqtt_client import connect_mqtt

# Crear la aplicación Flask
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}})

# Registrar Blueprints para modularizar las rutas
app.register_blueprint(sensor_bp)
app.register_blueprint(event_bp)
app.register_blueprint(actuator_bp)

# Iniciar la aplicación
if __name__ == '__main__':
    connect_mqtt()  # Conectar al broker MQTT
    app.run(host='0.0.0.0', port=5000, debug=True)  # Iniciar el servidor Flask
