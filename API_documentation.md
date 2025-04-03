# Documentación de API - Sistema de Monitoreo Ambiental Multi-Cliente

Esta documentación describe todos los endpoints disponibles en la API del sistema de monitoreo ambiental para cultivos de setas, con soporte para múltiples dispositivos cliente.

## Tabla de Contenidos
- [Gestión de Clientes](#gestión-de-clientes)
- [Sensores](#sensores)
- [Eventos y Alertas](#eventos-y-alertas)
- [Control de Actuadores](#control-de-actuadores)
- [Estado del Sistema](#estado-del-sistema)
- [Estadísticas](#estadísticas)

## Gestión de Clientes

### Listar todos los clientes
- **URL**: `/api/clients`
- **Método**: `GET`
- **Descripción**: Obtiene una lista de todos los clientes registrados.
- **Respuesta**: Array de objetos cliente con su estado, última conexión y descripción
- **Ejemplo respuesta**:
  ```json
  [
    {
      "id": 1,
      "client_id": "mushroom1",
      "name": "Orellana Rosada",
      "description": "Cultivo principal de setas Orellana Rosada",
      "last_seen": "2023-11-22T15:30:25",
      "status": "online",
      "created_at": "2023-11-01T10:00:00",
      "manually_disabled": 0
    }
  ]
  ```

### Obtener cliente por ID
- **URL**: `/api/clients/{client_id}`
- **Método**: `GET`
- **Descripción**: Obtiene información detallada de un cliente específico.
- **Parámetros URL**: `client_id` - ID único del cliente
- **Respuesta**: Objeto con detalles del cliente
- **Ejemplo respuesta**:
  ```json
  {
    "id": 1,
    "client_id": "mushroom1",
    "name": "Orellana Rosada",
    "description": "Cultivo principal de setas Orellana Rosada",
    "last_seen": "2023-11-22T15:30:25",
    "status": "online",
    "created_at": "2023-11-01T10:00:00",
    "manually_disabled": 0
  }
  ```

### Registrar nuevo cliente
- **URL**: `/api/clients`
- **Método**: `POST`
- **Descripción**: Registra un nuevo cliente en el sistema.
- **Cuerpo**:
  ```json
  {
    "client_id": "mushroom2",
    "name": "Shiitake",
    "description": "Cultivo de setas Shiitake"
  }
  ```
- **Respuesta**: Confirmación de registro exitoso

### Actualizar estado de cliente
- **URL**: `/api/clients/{client_id}/status`
- **Método**: `PUT`
- **Descripción**: Actualiza el estado (online/offline) de un cliente. Cuando se establece a 'offline', el cliente se marca como manualmente desactivado y no se reactivará automáticamente con mensajes MQTT.
- **Parámetros URL**: `client_id` - ID único del cliente
- **Cuerpo**:
  ```json
  {
    "status": "offline"
  }
  ```
- **Respuesta**: Confirmación de actualización exitosa
- **Notas especiales**: 
  - Al marcar un cliente como 'offline', permanecerá en ese estado incluso si sigue enviando datos.
  - Para reactivar un cliente manualmente desactivado, envíe el estado "online".

## Sensores

### Obtener datos de temperatura y humedad
- **URL**: `/api/clients/{client_id}/Sht3xSensor`
- **Método**: `GET`
- **Descripción**: Obtiene lecturas históricas de temperatura y humedad.
- **Parámetros URL**: `client_id` - ID único del cliente
- **Parámetros Query**: 
  - `page` (opcional, default=1): Número de página
  - `pageSize` (opcional, default=10): Tamaño de página
- **Respuesta**: Array de lecturas de temperatura y humedad
- **Ejemplo respuesta**:
  ```json
  [
    {
      "id": 100,
      "client_id": "mushroom1",
      "timestamp": "2023-11-22T15:30:25",
      "temperature": 23.5,
      "humidity": 65.3
    }
  ]
  ```

### Obtener datos de temperatura y humedad (manual)
- **URL**: `/api/clients/{client_id}/Sht3xSensorManual`
- **Método**: `GET`
- **Descripción**: Similar a Sht3xSensor pero para modo manual.
- **Parámetros**: Igual que el anterior

### Obtener parámetros ideales
- **URL**: `/api/clients/{client_id}/IdealParams/{param_type}`
- **Método**: `GET`
- **Descripción**: Obtiene los parámetros ideales para un tipo específico.
- **Parámetros URL**: 
  - `client_id` - ID único del cliente
  - `param_type` - Tipo de parámetro (temperatura, humedad)
- **Respuesta**: Objeto con rangos mínimo y máximo
- **Ejemplo respuesta**:
  ```json
  {
    "id": 1,
    "client_id": "mushroom1",
    "param_type": "temperatura",
    "min_value": 15.0,
    "max_value": 30.0,
    "timestamp": "2023-11-22T15:30:25"
  }
  ```

### Actualizar parámetros ideales
- **URL**: `/api/clients/{client_id}/IdealParams/{param_type}`
- **Método**: `PUT`
- **Descripción**: Actualiza los parámetros ideales para un tipo específico.
- **Parámetros URL**:
  - `client_id` - ID único del cliente
  - `param_type` - Tipo de parámetro (temperatura, humedad)
- **Cuerpo**:
  ```json
  {
    "min_value": 18.0,
    "max_value": 28.0
  }
  ```
- **Respuesta**: Confirmación de actualización exitosa

## Eventos y Alertas

### Listar eventos
- **URL**: `/api/clients/{client_id}/Event`
- **Método**: `GET`
- **Descripción**: Obtiene el historial de eventos y alertas.
- **Parámetros URL**: `client_id` - ID único del cliente
- **Parámetros Query**: 
  - `page` (opcional, default=1): Número de página
  - `pageSize` (opcional, default=10): Tamaño de página
- **Respuesta**: Array de eventos
- **Ejemplo respuesta**:
  ```json
  [
    {
      "id": 1,
      "client_id": "mushroom1",
      "message": "Advertencia! Temperatura fuera de rango: 32.5 C (Ideal: 15-30 C)",
      "timestamp": "2023-11-22T15:30:25",
      "topic": "temperatura"
    }
  ]
  ```

### Crear evento
- **URL**: `/api/clients/{client_id}/Event`
- **Método**: `POST`
- **Descripción**: Crea un nuevo evento en el sistema.
- **Parámetros URL**: `client_id` - ID único del cliente
- **Cuerpo**:
  ```json
  {
    "message": "Nuevo evento personalizado",
    "topic": "personalizado"
  }
  ```
- **Respuesta**: Confirmación de creación exitosa

### Filtrar eventos por tema
- **URL**: `/api/clients/{client_id}/Event/FilterByTopic`
- **Método**: `GET`
- **Descripción**: Filtra eventos por un tema específico.
- **Parámetros URL**: `client_id` - ID único del cliente
- **Parámetros Query**: 
  - `topic`: Tema por el que filtrar (temperatura, humedad)
  - `page` (opcional, default=1): Número de página
  - `pageSize` (opcional, default=10): Tamaño de página
- **Respuesta**: Array de eventos filtrados por tema

### Eliminar evento
- **URL**: `/api/clients/{client_id}/Event/{id}`
- **Método**: `DELETE`
- **Descripción**: Elimina un evento específico.
- **Parámetros URL**: 
  - `client_id` - ID único del cliente
  - `id` - ID del evento a eliminar
- **Respuesta**: Confirmación de eliminación exitosa

## Control de Actuadores

### Obtener todos los actuadores
- **URL**: `/api/clients/{client_id}/Actuator`
- **Método**: `GET`
- **Descripción**: Lista todos los actuadores y sus estados.
- **Parámetros URL**: `client_id` - ID único del cliente
- **Respuesta**: Array de actuadores con sus estados
- **Ejemplo respuesta**:
  ```json
  [
    {
      "id": 1,
      "client_id": "mushroom1",
      "name": "Iluminacion",
      "state": true,
      "timestamp": "2023-11-22T15:30:25"
    }
  ]
  ```

### Control de iluminación
- **URL**: `/api/clients/{client_id}/Actuator/toggle_light`
- **Método**: `POST`
- **Descripción**: Controla el estado de la iluminación.
- **Parámetros URL**: `client_id` - ID único del cliente
- **Cuerpo**:
  ```json
  {
    "state": true
  }
  ```
- **Respuesta**: Confirmación de señal enviada

### Control de ventilación
- **URL**: `/api/clients/{client_id}/Actuator/toggle_fan`
- **Método**: `POST`
- **Descripción**: Controla el estado del ventilador.
- **Parámetros URL**: `client_id` - ID único del cliente
- **Cuerpo**:
  ```json
  {
    "state": true
  }
  ```
- **Respuesta**: Confirmación de señal enviada

### Control de humidificador
- **URL**: `/api/clients/{client_id}/Actuator/toggle_humidifier`
- **Método**: `POST`
- **Descripción**: Controla el estado del humidificador.
- **Parámetros URL**: `client_id` - ID único del cliente
- **Cuerpo**:
  ```json
  {
    "state": true
  }
  ```
- **Respuesta**: Confirmación de señal enviada

### Control de motor
- **URL**: `/api/clients/{client_id}/Actuator/toggle_motor`
- **Método**: `POST`
- **Descripción**: Controla el estado del motor.
- **Parámetros URL**: `client_id` - ID único del cliente
- **Cuerpo**:
  ```json
  {
    "state": true
  }
  ```
- **Respuesta**: Confirmación de señal enviada

### Agregar nuevo actuador
- **URL**: `/api/clients/{client_id}/Actuator`
- **Método**: `POST`
- **Descripción**: Agrega un nuevo actuador al sistema.
- **Parámetros URL**: `client_id` - ID único del cliente
- **Cuerpo**:
  ```json
  {
    "name": "NuevoActuador",
    "state": false
  }
  ```
- **Respuesta**: Confirmación de creación exitosa

### Actualizar estado de actuador
- **URL**: `/api/clients/{client_id}/Actuator/{id}`
- **Método**: `PUT`
- **Descripción**: Actualiza el estado de un actuador específico.
- **Parámetros URL**: 
  - `client_id` - ID único del cliente
  - `id` - ID del actuador
- **Cuerpo**:
  ```json
  {
    "state": true
  }
  ```
- **Respuesta**: Confirmación de actualización exitosa

## Estado del Sistema

### Obtener modo de operación
- **URL**: `/api/clients/{client_id}/getState`
- **Método**: `GET`
- **Descripción**: Obtiene el modo actual (automático/manual).
- **Parámetros URL**: `client_id` - ID único del cliente
- **Respuesta**: Objeto con el modo actual
- **Ejemplo respuesta**:
  ```json
  {
    "mode": "automatico"
  }
  ```

### Actualizar modo de operación
- **URL**: `/api/clients/{client_id}/updateState`
- **Método**: `PUT`
- **Descripción**: Cambia el modo de operación.
- **Parámetros URL**: `client_id` - ID único del cliente
- **Cuerpo**:
  ```json
  {
    "mode": "manual"
  }
  ```
- **Respuesta**: Confirmación de actualización exitosa

## Estadísticas

### Obtener estadísticas del dashboard
- **URL**: `/api/clients/{client_id}/statistics/dashboard`
- **Método**: `GET`
- **Descripción**: Obtiene estadísticas agregadas para el dashboard.
- **Parámetros URL**: `client_id` - ID único del cliente
- **Parámetros Query**: 
  - `days` (opcional, default=7): Cantidad de días para el análisis
- **Respuesta**: Métricas estadísticas de temperatura y humedad
- **Ejemplo respuesta**:
  ```json
  {
    "sht3x_stats": {
      "temperature": {
        "count": 1250,
        "mean": 24.3,
        "median": 23.8,
        "mode": 23.5,
        "min": 19.2,
        "max": 32.5,
        "std_dev": 2.1
      },
      "humidity": {
        "count": 1250,
        "mean": 65.7,
        "median": 64.3,
        "mode": 62.5,
        "min": 45.0,
        "max": 89.6,
        "std_dev": 8.3
      }
    }
  }
  ```
