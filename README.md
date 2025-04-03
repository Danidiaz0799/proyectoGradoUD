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
- [Soporte Multi-Cliente](#-soporte-multi-cliente)
- [Instalación y Despliegue](#-instalación-y-despliegue)
- [Tecnologías Utilizadas](#-tecnologías-utilizadas)

## 🎯 Descripción General

Sistema IoT que monitorea y controla condiciones ambientales (temperatura, humedad) en tiempo real para múltiples dispositivos cliente. Ideal para cultivos, invernaderos y ambientes donde se requiere control preciso de condiciones.

**Características principales:**
- ✅ Monitoreo continuo de temperatura y humedad
- ✅ Control automático de actuadores basado en parámetros configurables
- ✅ Interfaz web para visualización de datos históricos y en tiempo real
- ✅ Sistema de alertas para condiciones fuera de rango
- ✅ Modos automático y manual para control de actuadores
- ✅ **Nuevo:** Soporte para múltiples dispositivos cliente
- ✅ **Nuevo:** Gestión avanzada de estado de clientes (activación/desactivación)

## 🏗️ Arquitectura del Sistema

```
┌───────────┐     MQTT      ┌────────────┐     HTTP     ┌─────────────────┐
│ Cliente 1 │ ────────────► │            │              │                 │
└───────────┘               │            │              │                 │
                            │  Servidor  │ ◄─────────►  │    Navegador    │
┌───────────┐               │  Central   │              │      Web        │
│ Cliente 2 │ ────────────► │            │              │                 │
└───────────┘     MQTT      └──────┬─────┘              └─────────────────┘
                                   │
                              ┌────▼────┐
                              │  Base   │
                              │   de    │
                              │  Datos  │
                              └─────────┘
```

1. **Sensores → Clientes**: Captura de datos ambientales en cada dispositivo
2. **Clientes → Servidor**: Transmisión mediante protocolo MQTT con identificación de cliente
3. **Servidor → Base de Datos**: Almacenamiento segmentado por cliente
4. **Servidor → Clientes**: Comandos para actuadores basados en condiciones ambientales
5. **Servidor ↔ Web**: API REST con selección de cliente para visualización y control

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
│   ├── config.py           # Credenciales, client_id y endpoints
│   ├── mqtt_config.py      # Conexión MQTT
│   └── wifi_config.py      # Conexión Wi-Fi
├── sensors/                # Lectura de sensores
│   └── sht3x.py            # Sensor temp/humedad
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
- Recepción y almacenamiento de datos de múltiples clientes
- Análisis de condiciones ambientales por cliente
- Control automático basado en parámetros configurables
- Generación de alertas y eventos
- Servidor web con API REST
- Gestión de clientes y su estado

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
│   ├── app_state.py        # Estado del sistema
│   ├── client.py           # Gestión de clientes
│   └── statistics.py       # Análisis estadísticos
└── routes/                 # API endpoints
    ├── sensor_routes.py    # Rutas para sensores
    ├── event_routes.py     # Rutas para eventos
    ├── actuator_routes.py  # Rutas para actuadores
    ├── app_state_routes.py # Rutas para estado
    ├── client_routes.py    # Rutas para gestión de clientes
    └── statistics_routes.py# Rutas para estadísticas
```

## 🔄 Flujo de Datos

1. **Identificación** 🆔: Cada cliente se registra con su ID único
   ```
   clients/{client_id}/register: "Orellana Rosada,Cultivo principal..."
   ```

2. **Captura** 📊: Los sensores miden condiciones ambientales cada 5 segundos
   ```
   clients/{client_id}/sensor/sht3x: "23.5,45.2" (temperatura,humedad)
   ```

3. **Procesamiento** ⚙️: Servidor evalúa datos contra parámetros ideales del cliente
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

El servidor expone una API REST completa para interactuar con el sistema. Todos los endpoints siguen el patrón `/api/clients/{client_id}/...` para permitir la selección de clientes específicos.

Para una documentación detallada de la API, consulte [API_documentation.md](API_documentation.md).

## 🔄 Soporte Multi-Cliente

El sistema permite gestionar múltiples dispositivos clientes de forma centralizada:

### Características del sistema multi-cliente

- **Identificación única**: Cada cliente tiene un identificador (`client_id`) único configurado
- **Tópicos MQTT separados**: Formato `clients/{client_id}/...` para aislar las comunicaciones
- **Datos segregados**: Registros de base de datos separados por `client_id`
- **Gestión independiente**: Cada cliente puede configurarse y controlarse por separado
- **Control de estado**: Los clientes pueden ser desactivados manualmente y no se reactivarán automáticamente

### Configuración de nuevo cliente

1. Configurar un nuevo dispositivo Raspberry Pi cliente:
   ```python
   # En config.py del cliente:
   CLIENT_ID = 'mushroom2'  # ID único del cliente
   CLIENT_NAME = 'Shiitake'  # Nombre descriptivo
   CLIENT_DESCRIPTION = 'Cultivo de setas Shiitake'
   ```

2. El cliente se registrará automáticamente al conectarse al servidor
3. El servidor creará la configuración inicial necesaria para el cliente
4. El cliente aparecerá en la interfaz web para su gestión

### Gestión de estado de clientes

- Los clientes pueden ser marcados como `offline` desde la API o interfaz
- Un cliente marcado como `offline` manualmente no se reactivará automáticamente al enviar datos
- Los datos del cliente seguirán almacenándose aunque esté marcado como `offline`

## 🚀 Instalación y Despliegue

### Raspberry Cliente
1. Clonar repositorio en la Raspberry Pi cliente
2. Configurar `config.py` con credenciales Wi-Fi, dirección del servidor y CLIENT_ID único
3. Instalar dependencias: `pip install paho-mqtt adafruit-circuitpython-sht31d`
4. Instalar como servicio: `sudo cp projectClient.service /etc/systemd/system/`
5. Activar servicio: `sudo systemctl enable projectClient && sudo systemctl start projectClient`

### Raspberry Servidor
1. Clonar repositorio en la Raspberry Pi servidor
2. Instalar dependencias: `pip install flask flask-cors paho-mqtt sqlite3 aiosqlite numpy`
3. Inicializar base de datos: `python database.py`
4. Instalar como servicio: `sudo cp project.service /etc/systemd/system/`
5. Activar servicio: `sudo systemctl enable project && sudo systemctl start project`
6. Acceder a la interfaz web: `http://<ip-raspberry-servidor>:5000`

## 🛠️ Tecnologías Utilizadas

- **Hardware**: Raspberry Pi, sensores SHT3x, actuadores varios
- **Backend**: Python, Flask, SQLite, MQTT (Mosquitto)
- **Frontend**: Angular
- **Comunicación**: Protocolo MQTT, API REST
- **Despliegue**: Servicios systemd

