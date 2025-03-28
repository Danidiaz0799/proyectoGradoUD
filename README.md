# Proyecto de Grado - Universidad Distrital

## Descripción

Este proyecto tiene como objetivo desarrollar una aplicación innovadora basada en el Internet de las Cosas (IoT) para la captura, almacenamiento y visualización de datos provenientes de sensores. Se enfoca en proporcionar un sistema eficiente y escalable para el monitoreo remoto en tiempo real.

El sistema está compuesto por dos principales componentes:

- **Raspberry Cliente**: Se encarga de recopilar datos de sensores ambientales y enviarlos a un broker MQTT para su posterior procesamiento. También recibe comandos para controlar actuadores.
- **Raspberry Pi Servidor**: Recibe los datos de la Raspberry Cliente, los almacena en una base de datos y expone una API para su acceso y control de actuadores. Además, aloja el servidor web que permite la visualización y gestión de los datos en tiempo real.

## Tecnologías Utilizadas

- **Lenguajes de Programación**: Python, Angular, Flask.
- **Base de Datos**: SQLite.
- **Protocolos de Comunicación**: MQTT.
- **Hardware**: Raspberry Pi, sensores SHT3x (temperatura/humedad), sensores GY302 (luz), pantalla OLED, actuadores (humidificador nebulizador de 24V, ventiladores de 5V, motor de 5V, bombilla de 24V).

## Código de la Raspberry Cliente

El código de la Raspberry Cliente está diseñado para leer datos de los sensores, publicarlos en un broker MQTT y controlar actuadores basado en los mensajes recibidos del servidor. A continuación, se describe la estructura y funcionalidad detallada:

### Estructura de Archivos

- **boot.py**: Archivo principal que contiene la función de inicio del sistema. Este archivo:
  - Inicializa las conexiones Wi-Fi y MQTT
  - Configura callbacks para recibir mensajes MQTT
  - Inicia hilos separados para publicar datos de sensores y escuchar comandos
  - Gestiona la suscripción a tópicos para controlar actuadores
  - Maneja la reconexión automática en caso de fallos

- **Carpeta config/**: Contiene los archivos de configuración:
  - **config.py**: Define constantes como credenciales Wi-Fi, dirección del servidor MQTT y nombres de tópicos
  - **wifi_config.py**: Implementa la funcionalidad para conectarse a la red Wi-Fi especificada
  - **mqtt_config.py**: Gestiona la conexión al broker MQTT

- **Carpeta sensors/**: Contiene los módulos para interactuar con los sensores:
  - **sht3x.py**: Funciones para leer y publicar datos de temperatura y humedad del sensor SHT3x
  - **gy302.py**: Funciones para leer y publicar datos de intensidad de luz del sensor GY302
  - **bmp280.py**: Funciones adicionales para sensores de presión atmosférica (no utilizados actualmente)

- **Carpeta actuators/**: Contiene los módulos para controlar los diferentes actuadores:
  - **light.py**: Controla el encendido/apagado de la bombilla de 24V
  - **fan.py**: Controla el encendido/apagado de los ventiladores de 5V
  - **humidifier.py**: Controla el encendido/apagado del humidificador nebulizador de 24V
  - **motor.py**: Controla el encendido/apagado del motor de 5V
  - **oled.py**: Gestiona la pantalla OLED para mostrar información en tiempo real

- **projectClient.service**: Archivo de configuración para systemd que permite que la aplicación cliente se ejecute como un servicio en la Raspberry Pi.

### Funcionalidad Principal

#### Lectura de Sensores
El cliente lee continuamente los valores de los sensores y los publica en el broker MQTT:
- Cada 5 segundos, lee los valores de temperatura y humedad del sensor SHT3x y los publica en el tópico 'sensor/sht3x'
- Cada 5 segundos, lee los valores de intensidad de luz del sensor GY302 y los publica en el tópico 'sensor/gy302'

#### Control de Actuadores
El cliente está suscrito a los siguientes tópicos MQTT para recibir comandos de control:
- 'raspberry/light': Para controlar la bombilla de 24V
- 'raspberry/fan': Para controlar los ventiladores de 5V
- 'raspberry/humidifier': Para controlar el humidificador nebulizador de 24V
- 'raspberry/motor': Para controlar el motor de 5V

Cuando recibe un mensaje en cualquiera de estos tópicos, ejecuta la función correspondiente para cambiar el estado del actuador.

#### Interfaz Visual con OLED
El cliente muestra información relevante en una pantalla OLED:
- Mensajes de estado durante la inicialización (conexión Wi-Fi, conexión MQTT)
- Valores actuales de temperatura y humedad en tiempo real
- Alertas y notificaciones cuando sea necesario

#### Operación Multihilo
El sistema utiliza hilos separados para:
- Escuchar mensajes MQTT entrantes
- Publicar datos del sensor SHT3x
- Publicar datos del sensor GY302
Esto permite que todas las operaciones se ejecuten simultáneamente sin bloquear el hilo principal.

## Código de la Raspberry Server

El código de la Raspberry Pi Servidor está diseñado para recibir los datos publicados por la Raspberry Cliente, almacenarlos en una base de datos y proporcionar una API para acceder a estos datos y controlar actuadores. A continuación, se describe la estructura y funcionalidad detallada:

### Estructura de Archivos

- **app.py**: Archivo principal que inicializa y configura la aplicación Flask, registra las rutas API y sirve la aplicación web Angular. Este archivo:
  - Inicializa el servidor Flask
  - Configura CORS para permitir peticiones desde cualquier origen
  - Registra los blueprints (rutas modulares) para diferentes funcionalidades
  - Establece rutas para servir archivos estáticos de la aplicación Angular
  - Conecta con el broker MQTT al iniciar la aplicación

- **mqtt_client.py**: Gestiona la comunicación MQTT con la Raspberry Cliente. Sus funciones principales son:
  - Establecer conexión con el broker MQTT
  - Suscribirse a los tópicos 'sensor/sht3x' y 'sensor/gy302'
  - Procesar los mensajes entrantes separando los datos de temperatura, humedad y luz
  - Almacenar los datos recibidos en la base de datos mediante las funciones correspondientes
  - Verificar si los valores recibidos están dentro de los parámetros ideales definidos
  - Generar eventos cuando los valores están fuera de rango
  - Controlar automáticamente los actuadores en base a los valores recibidos cuando el modo automático está activado

- **database.py**: Se encarga de crear y configurar la estructura de la base de datos SQLite. Este archivo:
  - Crea las tablas necesarias si no existen (gy302_data, sht3x_data, events, actuators, ideal_params, app_state)
  - Inicializa los datos por defecto para los parámetros ideales de temperatura (15-30°C) y humedad (30-100%)
  - Configura los actuadores predeterminados (Iluminación, Ventilación, Humidificador, Motor)
  - Establece el modo inicial de la aplicación como 'automático'

- **Carpeta models/**: Contiene los modelos de datos que interactúan con la base de datos:
  - **sensor_data.py**: Define funciones para guardar y recuperar datos de los sensores SHT3x y GY302, y gestionar los parámetros ideales.
  - **event.py**: Gestiona la creación y recuperación de eventos del sistema.
  - **actuator.py**: Maneja el estado de los actuadores y proporciona funciones para actualizarlos.
  - **app_state.py**: Controla el estado de la aplicación (modo manual o automático).

- **Carpeta routes/**: Contiene los blueprints que definen las rutas API:
  - **sensor_routes.py**: Proporciona endpoints para acceder a los datos de los sensores.
  - **event_routes.py**: Define rutas para gestionar eventos del sistema.
  - **actuator_routes.py**: Ofrece endpoints para controlar los actuadores.
  - **app_state_routes.py**: Permite cambiar entre modo automático y manual.

- **project.service**: Archivo de configuración para systemd que permite que la aplicación se ejecute como un servicio en la Raspberry Pi, asegurando que se inicie automáticamente después de un reinicio.

### Funcionalidad Principal

#### Sistema de Control Automatizado
El servidor implementa un sistema de control automático para mantener los parámetros ambientales (temperatura y humedad) dentro de los rangos ideales definidos:

- Si la temperatura es baja, enciende la iluminación y apaga el ventilador.
- Si la temperatura es alta, apaga la iluminación y enciende el ventilador.
- Si la humedad es baja, enciende el humidificador y apaga el motor.
- Si la humedad es alta, apaga el humidificador y enciende el motor.

#### Gestión de Modos de Operación
El sistema puede funcionar en dos modos:

- **Modo Automático**: Los actuadores se controlan automáticamente según los parámetros ambientales.
- **Modo Manual**: El usuario tiene control total sobre cada actuador a través de la API.

#### Sistema de Registro de Eventos
Cuando los valores de temperatura o humedad están fuera de los rangos ideales, el sistema genera eventos que se almacenan en la base de datos y pueden consultarse a través de la API.

#### Comunicación MQTT
La comunicación entre el cliente y el servidor se realiza mediante el protocolo MQTT:

- El cliente publica en los tópicos 'sensor/sht3x' (temperatura y humedad) y 'sensor/gy302' (luz).
- El servidor se suscribe a estos tópicos y procesa los mensajes recibidos.
- El servidor publica comandos en los tópicos 'raspberry/light', 'raspberry/fan', 'raspberry/humidifier' y 'raspberry/motor' para controlar los actuadores.

## Flujo de Comunicación del Sistema

1. **Captura de Datos**: Los sensores conectados a la Raspberry Cliente (SHT3x, GY302) capturan datos ambientales periódicamente.

2. **Publicación MQTT**: La Raspberry Cliente publica estos datos en los tópicos MQTT correspondientes:
   - Temperatura y humedad en 'sensor/sht3x' en formato "temperatura,humedad"
   - Nivel de luz en 'sensor/gy302'

3. **Recepción y Procesamiento**: La Raspberry Servidor recibe estos datos, los procesa y:
   - Almacena la información en la base de datos SQLite
   - Verifica si los valores están dentro de los rangos ideales configurados
   - Genera eventos si los valores están fuera de rango
   - Toma decisiones automáticas sobre los actuadores (en modo automático)

4. **Control de Actuadores**: Si es necesario, la Raspberry Servidor publica comandos en los tópicos:
   - 'raspberry/light' para controlar la iluminación
   - 'raspberry/fan' para controlar la ventilación
   - 'raspberry/humidifier' para controlar la humidificación
   - 'raspberry/motor' para controlar el motor de circulación

5. **Acción del Cliente**: La Raspberry Cliente recibe estos comandos y activa/desactiva los actuadores físicos correspondientes.

6. **Visualización Web**: Paralelamente, la aplicación web desarrollada en Angular consulta los datos a través de la API REST proporcionada por el servidor Flask, permitiendo al usuario:
   - Visualizar datos históricos y en tiempo real
   - Controlar manualmente los actuadores
   - Configurar parámetros ideales
   - Ver registro de eventos del sistema

## Endpoints de la API

La API proporciona los siguientes endpoints para interactuar con los datos:

### Sensores (routes/sensor_routes.py)

- `GET /api/Sht3xSensor` → Retorna los datos de temperatura y humedad con soporte de paginación.
- `GET /api/Gy302Sensor` → Retorna los datos del sensor de luz con soporte de paginación.
- `GET /api/SensorData?start=<fecha>&end=<fecha>` → Retorna los datos en un rango de fechas.
- `POST /api/SensorData` → Agrega nuevos datos de sensores. Recibe un JSON con los datos del sensor.

### Eventos (routes/event_routes.py)

- `GET /api/Event` → Retorna todos los eventos almacenados.
- `GET /api/Event/FilterByTopic?topic=<nombre>` → Filtra eventos por tema (temperatura o humedad).
- `POST /api/Event` → Agrega un nuevo evento. Requiere un JSON con los detalles del evento.

### Actuadores (routes/actuator_routes.py)

- `GET /api/Actuator` → Retorna el estado de todos los actuadores.
- `POST /api/Actuator/toggle_light` → Controla la bombilla de 24V.
- `POST /api/Actuator/toggle_fan` → Controla los ventiladores de 5V.
- `POST /api/Actuator/toggle_humidifier` → Controla el humidificador nebulizador de 24V.
- `POST /api/Actuator/toggle_motor` → Controla el motor de 5V.

### Estado de la Aplicación (routes/app_state_routes.py)

- `GET /api/AppState` → Obtiene el modo actual de la aplicación (manual o automático).
- `POST /api/AppState` → Cambia el modo de la aplicación. Recibe un JSON con el nuevo modo.

### Parámetros Ideales (routes/sensor_routes.py)

- `GET /api/IdealParams/{param}` → Obtiene los parámetros ideales para temperatura o humedad.
- `PUT /api/IdealParams/{param}` → Actualiza los parámetros ideales. Recibe un JSON con los nuevos valores mínimo y máximo.

## Arquitectura del Sistema

- **Captura de Datos**: La Raspberry Cliente recoge información de sensores y la transmite vía MQTT.
- **Procesamiento y Almacenamiento**: La Raspberry Pi Servidor recibe los datos, los almacena en una base de datos SQLite y los expone mediante una API RESTful.
- **Automatización**: El servidor analiza los datos recibidos y controla automáticamente los actuadores para mantener las condiciones ambientales óptimas.
- **Visualización y Control**: Un cliente web desarrollado en Angular permite visualizar los datos, controlar los actuadores manualmente y ajustar los parámetros ideales.

## Despliegue del Sistema

### Despliegue del Servidor
El servidor se despliega como un servicio systemd en la Raspberry Pi, lo que garantiza que se inicie automáticamente tras reiniciar el dispositivo. El archivo `project.service` define esta configuración y debe instalarse en el directorio `/etc/systemd/system/` para registrarlo como un servicio del sistema.

### Despliegue del Cliente
De manera similar, el cliente se despliega como un servicio systemd utilizando el archivo `projectClient.service`. Esto asegura que la captura de datos y el control de actuadores se inicie automáticamente cuando la Raspberry Cliente se encienda.

Este proyecto sigue las mejores prácticas de desarrollo de software y está diseñado para ser fácilmente escalable y adaptable a diferentes entornos de monitoreo.

