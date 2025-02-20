# proyectoGradoUD

Código del proyecto de grado de tecnología de la universidad Distrital

## Descripción

Este proyecto tiene como objetivo desarrollar una aplicación innovadora que resuelva problemas específicos en el ámbito de la tecnología. Utiliza diversas tecnologías modernas y sigue las mejores prácticas de desarrollo de software para garantizar un producto final robusto y eficiente.

## Tecnologías Utilizadas

- Lenguaje de programación: [Especificar lenguaje]
- Framework: [Especificar framework]
- Base de datos: [Especificar base de datos]
- Herramientas adicionales: [Especificar herramientas]

## Código del ESP32

El código del ESP32 está diseñado para leer datos de un sensor DHT11 y publicarlos en un broker MQTT. A continuación se describen los archivos principales:

- `esp32_code.py`: Contiene la función principal que gestiona la conexión Wi-Fi, la conexión al broker MQTT y la publicación de datos del sensor.
- `config/wifi_config.py`: Configura y maneja la conexión Wi-Fi.
- `config/mqtt_config.py`: Configura y maneja la conexión al broker MQTT.
- `sensors/sensor_config.py`: Configura el sensor DHT11 y define la función para publicar los datos del sensor.
- `config/config.py`: Contiene las configuraciones generales como las credenciales Wi-Fi y los detalles del broker MQTT.

## Código de la Raspberry Pi

El código de la Raspberry Pi está diseñado para recibir los datos publicados por el ESP32, almacenarlos en una base de datos y proporcionar una API para acceder a estos datos. A continuación se describen los archivos principales:

- `app.py`: Configura y ejecuta la aplicación Flask, incluyendo la conexión al broker MQTT y el manejo de rutas para servir la aplicación Angular.
- `mqtt_client.py`: Configura el cliente MQTT para recibir datos del ESP32 y guardarlos en la base de datos.
- `database.py`: Crea las tablas necesarias en la base de datos SQLite.
- `models/sensor_data.py`: Define las funciones para interactuar con la tabla de datos del sensor.
- `models/event.py`: Define las funciones para interactuar con la tabla de eventos.
- `models/actuator.py`: Define las funciones para interactuar con la tabla de actuadores.
- `routes/sensor_routes.py`: Define las rutas API para obtener y agregar datos del sensor.
- `routes/event_routes.py`: Define las rutas API para obtener y agregar eventos.
- `routes/actuator_routes.py`: Define las rutas API para obtener y agregar estados de actuadores.

## Instalación

1. Clonar el repositorio:
   ```bash
   git clone [URL del repositorio]
   ```
2. Navegar al directorio del proyecto:
   ```bash
   cd proyectoGradoUD
   ```
3. Instalar las dependencias:
   ```bash
   [Comando de instalación de dependencias]
   ```

## Uso

[Instrucciones sobre cómo usar la aplicación]

## Contribuciones

Las contribuciones son bienvenidas. Por favor, sigue los pasos a continuación para contribuir:

1. Haz un fork del repositorio.
2. Crea una nueva rama (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza tus cambios y haz commit (`git commit -am 'Añadir nueva funcionalidad'`).
4. Haz push a la rama (`git push origin feature/nueva-funcionalidad`).
5. Abre un Pull Request.

## Licencia

Este proyecto está licenciado bajo la Licencia [Nombre de la licencia].
