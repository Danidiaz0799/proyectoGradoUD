# 🌱 Sistema de Monitoreo Ambiental IoT - Universidad Distrital

[![Estado: En desarrollo](https://img.shields.io/badge/Estado-En%20Desarrollo-yellow)]()
[![Plataforma: Raspberry Pi](https://img.shields.io/badge/Plataforma-Raspberry%20Pi-C51A4A)]()
[![Lenguaje: Python](https://img.shields.io/badge/Lenguaje-Python-blue)]()

## 📋 Índice

- [Descripción General](#-descripción-general)
- [Arquitectura del Sistema](#-arquitectura-del-sistema)
- [Componentes Principales](#-componentes-principales)
  - [Raspberry Cliente](#-raspberry-cliente)
  - [Raspberry Servidor](#-raspberry-servidor)
- [Flujo de Datos](#-flujo-de-datos)
- [API REST](#-api-rest)
- [Instalación y Despliegue](#-instalación-y-despliegue)
- [Tecnologías Utilizadas](#-tecnologías-utilizadas)

## 🎯 Descripción General

Sistema IoT que monitorea y controla condiciones ambientales (temperatura, humedad e iluminación) en tiempo real. Ideal para cultivos, invernaderos y ambientes donde se requiere control preciso de condiciones.

**Características principales:**
- ✅ Monitoreo continuo de temperatura, humedad y luz
- ✅ Control automático de actuadores basado en parámetros configurables
- ✅ Interfaz web para visualización de datos históricos y en tiempo real
- ✅ Sistema de alertas para condiciones fuera de rango
- ✅ Modos automático y manual para control de actuadores

## 🏗️ Arquitectura del Sistema

```
┌─────────────────┐    MQTT    ┌─────────────────┐    HTTP    ┌─────────────────┐
│  Raspberry Pi   │  ───────►  │  Raspberry Pi   │  ◄─────►  │   Navegador     │
│    Cliente      │            │    Servidor     │            │     Web         │
│                 │  ◄───────  │                 │            │                 │
└────────┬────────┘            └────────┬────────┘            └─────────────────┘
         │                              │
    ┌────▼───┐                   ┌─────▼─────┐
    │Sensores│                   │ Base de   │
    │  &     │                   │  Datos    │
    │Actuad. │                   │  SQLite   │
    └────────┘                   └───────────┘
```

1. **Sensores → Cliente**: Captura de datos ambientales
2. **Cliente → Servidor**: Transmisión mediante protocolo MQTT
3. **Servidor → Base de Datos**: Almacenamiento para análisis e históricos
4. **Servidor → Cliente**: Comandos para actuadores basados en condiciones ambientales
5. **Servidor ↔ Web**: API REST para visualización y control desde interfaz Angular

## 🧩 Componentes Principales

### 📟 Raspberry Cliente

Dispositivo que captura datos de sensores y controla actuadores físicos.

#### Hardware
- Sensores SHT3x (temperatura/humedad)
- Pantalla OLED para visualización local
- Actuadores: bombilla 24V, ventiladores 5V, humidificador 24V, motor 5V

#### Software
- **boot.py**: Punto de entrada que inicializa todo el sistema
- **Sensores**: Módulos para lectura de datos ambientales
- **Actuadores**: Control de dispositivos físicos
- **Comunicación**: Cliente MQTT para envío/recepción de datos

#### Estructura de Archivos
```
RaspClient/
├── boot.py                 # Inicialización del sistema
├── projectClient.service   # Configuración systemd
├── config/                 # Configuraciones
│   ├── config.py           # Credenciales y endpoints
│   ├── mqtt_config.py      # Conexión MQTT
│   └── wifi_config.py      # Conexión Wi-Fi
├── sensors/                # Lectura de sensores
│   ├── sht3x.py            # Sensor temp/humedad
└── actuators/              # Control de actuadores
    ├── light.py            # Bombilla
    ├── fan.py              # Ventiladores
    ├── humidifier.py       # Humidificador
    ├── motor.py            # Motor
    └── oled.py             # Pantalla
```

### 🖥️ Raspberry Servidor

Dispositivo que procesa datos, ejecuta lógica de control y sirve la aplicación web.

#### Funcionalidades
- Recepción y almacenamiento de datos
- Análisis de condiciones ambientales
- Control automático basado en parámetros configurables
- Generación de alertas y eventos
- Servidor web con API REST

#### Estructura de Archivos
```
RaspServer/
├── app.py                  # Aplicación Flask principal
├── mqtt_client.py          # Cliente MQTT
├── database.py             # Gestión de base de datos
├── project.service         # Configuración systemd
├── models/                 # Modelos de datos
│   ├── sensor_data.py      # Datos de sensores
│   ├── event.py            # Eventos y alertas
│   ├── actuator.py         # Estado de actuadores
│   └── app_state.py        # Estado del sistema
└── routes/                 # API endpoints
    ├── sensor_routes.py    # Rutas para sensores
    ├── event_routes.py     # Rutas para eventos
    ├── actuator_routes.py  # Rutas para actuadores
    └── app_state_routes.py # Rutas para estado
```

## 🔄 Flujo de Datos

1. **Captura** 📊: Los sensores miden condiciones ambientales cada 5 segundos
   ```
   SHT3x → Temperatura (°C), Humedad (%)
   ```

2. **Transmisión** 📡: Cliente envía datos vía MQTT al servidor
   ```
   Tópico 'sensor/sht3x': "23.5,45.2" (temperatura,humedad)
   ```

3. **Procesamiento** ⚙️: Servidor evalúa datos contra parámetros ideales
   ```
   Ideal Temperatura: 15-30°C
   Ideal Humedad: 30-100%
   ```

4. **Acción** 🔌: Control automático de actuadores (modo automático)
   ```
   Temperatura baja → Luz ON, Ventilador OFF
   Temperatura alta → Luz OFF, Ventilador ON
   Humedad baja → Humidificador ON, Motor OFF
   Humedad alta → Humidificador OFF, Motor ON
   ```

5. **Retroalimentación** 🔁: Actuadores modifican el ambiente y el ciclo continúa

## 🌐 API REST

El servidor expone una API REST completa para interactuar con el sistema:

### Sensores
- `GET /api/Sht3xSensor` - Datos de temperatura/humedad (paginados)

### Actuadores
- `GET /api/Actuator` - Estado de todos los actuadores
- `POST /api/Actuator/toggle_light` - Control de iluminación
- `POST /api/Actuator/toggle_fan` - Control de ventilación
- `POST /api/Actuator/toggle_humidifier` - Control de humidificador
- `POST /api/Actuator/toggle_motor` - Control de motor

### Sistema
- `GET /api/AppState` - Modo actual (automático/manual)
- `POST /api/AppState` - Cambio de modo
- `GET /api/Event` - Registro de eventos/alertas
- `GET /api/IdealParams/{param}` - Parámetros ideales
- `PUT /api/IdealParams/{param}` - Actualización de parámetros

## 🚀 Instalación y Despliegue

### Raspberry Cliente
1. Clonar repositorio en la Raspberry Pi cliente
2. Configurar `config.py` con credenciales Wi-Fi y dirección del servidor
3. Instalar dependencias: `pip install paho-mqtt adafruit-circuitpython-sht31d`
4. Instalar como servicio: `sudo cp projectClient.service /etc/systemd/system/`
5. Activar servicio: `sudo systemctl enable projectClient && sudo systemctl start projectClient`

### Raspberry Servidor
1. Clonar repositorio en la Raspberry Pi servidor
2. Instalar dependencias: `pip install flask flask-cors paho-mqtt sqlite3 aiosqlite`
3. Instalar como servicio: `sudo cp project.service /etc/systemd/system/`
4. Activar servicio: `sudo systemctl enable project && sudo systemctl start project`
5. Acceder a la interfaz web: `http://<ip-raspberry-servidor>:5000`

## 🛠️ Tecnologías Utilizadas

- **Hardware**: Raspberry Pi, sensores SHT3x, actuadores varios
- **Backend**: Python, Flask, SQLite, MQTT (Mosquitto)
- **Frontend**: Angular
- **Comunicación**: Protocolo MQTT, API REST
- **Despliegue**: Servicios systemd

