# Proyecto de Grado - Universidad Distrital

## Descripción

Este proyecto tiene como objetivo desarrollar una aplicación innovadora basada en el Internet de las Cosas (IoT) para la captura, almacenamiento y visualización de datos provenientes de sensores. Se enfoca en proporcionar un sistema eficiente y escalable para el monitoreo remoto en tiempo real.

El sistema está compuesto por dos principales componentes:

- **Raspberry Cliente**: Se encarga de recopilar datos de sensores ambientales y enviarlos a un broker MQTT para su posterior procesamiento.
- **Raspberry Pi Servidor**: Recibe los datos de la Raspberry Cliente, los almacena en una base de datos y expone una API para su acceso y control de actuadores. Además, aloja el servidor web que permite la visualización y gestión de los datos en tiempo real.

## Tecnologías Utilizadas

- **Lenguajes de Programación**: Python, Angular, Flask.
- **Base de Datos**: SQLite.
- **Protocolos de Comunicación**: MQTT.
- **Hardware**: Raspberry Pi, sensores SHT3x, sensores GY302, actuadores (humidificador nebulizador de 24V, ventiladores de 5V, motor de 5V, bombilla de 24V).

## Código de la Raspberry Cliente

El código de la Raspberry Cliente está diseñado para leer datos de los sensores SHT3x (temperatura y humedad) y GY302 (luz), y publicarlos en un broker MQTT. A continuación, se describen los archivos principales:

- `boot.py`: Contiene la función principal que gestiona la conexión Wi-Fi, la conexión al broker MQTT y la publicación de datos de los sensores.
- `config/wifi_config.py`: Configura y maneja la conexión Wi-Fi.
- `config/mqtt_config.py`: Configura y maneja la conexión al broker MQTT.
- `sensors/sensor_config.py`: Configura los sensores SHT3x y GY302 y define las funciones para publicar los datos.
- `config/config.py`: Contiene las configuraciones generales como las credenciales Wi-Fi y los detalles del broker MQTT.

## Código de la Raspberry Server

El código de la Raspberry Pi está diseñado para recibir los datos publicados por la Raspberry Cliente, almacenarlos en una base de datos y proporcionar una API para acceder a estos datos. A continuación, se describen los archivos principales:

- `app.py`: Configura y ejecuta la aplicación Flask, incluyendo la conexión al broker MQTT y el manejo de rutas para servir la aplicación Angular. Este servidor web está alojado en la Raspberry Pi Servidor.
- `mqtt_client.py`: Configura el cliente MQTT para recibir datos de la Raspberry Cliente y guardarlos en la base de datos.
- `database.py`: Crea las tablas necesarias en la base de datos SQLite.
- `models/sensor_data.py`: Define las funciones para interactuar con la tabla de datos del sensor.
- `models/event.py`: Define las funciones para interactuar con la tabla de eventos.
- `models/actuator.py`: Define las funciones para interactuar con la tabla de actuadores.
- `routes/sensor_routes.py`: Define las rutas API para obtener y agregar datos de los sensores.
- `routes/event_routes.py`: Define las rutas API para obtener y agregar eventos.
- `routes/actuator_routes.py`: Define las rutas API para obtener y agregar estados de actuadores.
- `routes/ideal_params_routes.py`: Define las rutas API para obtener y actualizar los parámetros ideales.

## Endpoints de la API

La API proporciona los siguientes endpoints para interactuar con los datos:

### Sensores (routes/sensor_routes.py)

- `GET /api/Sht3xSensor` → Retorna los datos de temperatura y humedad.
- `GET /api/Gy302Sensor` → Retorna los datos del sensor de luz.
- `GET /api/SensorData?start=<fecha>&end=<fecha>` → Retorna los datos en un rango de fechas.
- `POST /api/SensorData` → Agrega nuevos datos de sensores. Recibe un JSON con los datos del sensor.

### Eventos (routes/event_routes.py)

- `GET /api/Event` → Retorna todos los eventos almacenados.
- `GET /api/Event/FilterByTopic?topic=<nombre>` → Filtra eventos por tema.
- `POST /api/Event` → Agrega un nuevo evento. Requiere un JSON con los detalles del evento.

### Actuadores (routes/actuator_routes.py)

- `GET /api/Actuator` → Retorna el estado de todos los actuadores.
- `POST /api/Actuator/toggle_light` → Controla la bombilla de 24V.
- `POST /api/Actuator/toggle_fan` → Controla los ventiladores de 5V.
- `POST /api/Actuator/toggle_humidifier` → Controla el humidificador nebulizador de 24V.
- `POST /api/Actuator/toggle_motor` → Controla el motor de 5V.

### Parámetros Ideales (routes/ideal_params_routes.py)

- `GET /api/IdealParams/{param}` → Obtiene los parámetros ideales.
- `PUT /api/IdealParams/{param}` → Actualiza los parámetros ideales.

## Arquitectura del Sistema

- **Captura de Datos**: La Raspberry Cliente recoge información de sensores y la transmite vía MQTT.
- **Procesamiento y Almacenamiento**: La Raspberry Pi Servidor recibe los datos, los almacena en una base de datos y los expone mediante una API.
- **Visualización y Control**: Un cliente web desarrollado en Angular permite visualizar los datos y controlar los actuadores en tiempo real.

Este proyecto sigue las mejores prácticas de desarrollo de software y está diseñado para ser fácilmente escalable y adaptable a diferentes entornos de monitoreo. Importante

