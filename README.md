# proyectoGradoUD
![image](https://github.com/user-attachments/assets/6a5322b3-7d50-4350-ae90-57fdf479fd64)

Código del proyecto de grado de tecnología de la universidad Distrital

## Descripción

Este proyecto tiene como objetivo desarrollar una aplicación innovadora que resuelva problemas específicos en el ámbito de la tecnología. Utiliza diversas tecnologías modernas y sigue las mejores prácticas de desarrollo de software para garantizar un producto final robusto y eficiente.

## Tecnologías Utilizadas
- Lenguaje de programación: [Python, Angular, Flask]

## Código de la Raspberry Cliente

El código de la Raspberry Cliente está diseñado para leer datos de un sensor sht3x y publicarlos en un broker MQTT. A continuación se describen los archivos principales:

- `boot.py`: Contiene la función principal que gestiona la conexión Wi-Fi, la conexión al broker MQTT y la publicación de datos del sensor.
- `config/wifi_config.py`: Configura y maneja la conexión Wi-Fi.
- `config/mqtt_config.py`: Configura y maneja la conexión al broker MQTT.
- `sensors/sensor_config.py`: Configura el sensor sht3x y define la función para publicar los datos del sensor.
- `config/config.py`: Contiene las configuraciones generales como las credenciales Wi-Fi y los detalles del broker MQTT.

## Código de la Raspberry Pi

El código de la Raspberry Pi está diseñado para recibir los datos publicados por la Raspberry Cliente, almacenarlos en una base de datos y proporcionar una API para acceder a estos datos. A continuación se describen los archivos principales:

- `app.py`: Configura y ejecuta la aplicación Flask, incluyendo la conexión al broker MQTT y el manejo de rutas para servir la aplicación Angular.
- `mqtt_client.py`: Configura el cliente MQTT para recibir datos de la Raspberry Cliente y guardarlos en la base de datos.
- `database.py`: Crea las tablas necesarias en la base de datos SQLite.
- `models/sensor_data.py`: Define las funciones para interactuar con la tabla de datos del sensor.
- `models/event.py`: Define las funciones para interactuar con la tabla de eventos.
- `models/actuator.py`: Define las funciones para interactuar con la tabla de actuadores.
- `routes/sensor_routes.py`: Define las rutas API para obtener y agregar datos del sensor.
- `routes/event_routes.py`: Define las rutas API para obtener y agregar eventos.
- `routes/actuator_routes.py`: Define las rutas API para obtener y agregar estados de actuadores.

