# QuickTask Backend API - Documentación

## Descripción general

API REST minimalista para gestionar tareas personales. Implementada con **FastAPI**, **SQLAlchemy** y **SQLite**.

## Estructura del proyecto

```
quicktask_backend/
├── main.py              # Aplicación principal con rutas FastAPI
├── database.py          # Configuración de la base de datos
├── models.py            # Modelos ORM (SQLAlchemy)
├── schemas.py           # Esquemas de validación (Pydantic)
├── crud.py              # Funciones CRUD
├── requirements.txt     # Dependencias del proyecto
└── tasks.db            # Base de datos SQLite (creada automáticamente)
```

## Instalación y configuración

### 1. Crear un entorno virtual (recomendado)

```bash
python -m venv venv
```

**Activar el entorno virtual:**

- **Windows:**
  ```bash
  venv\Scripts\activate
  ```
- **macOS/Linux:**
  ```bash
  source venv/bin/activate
  ```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Ejecutar el servidor

```bash
python main.py
```

O alternativamente:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

El servidor estará disponible en `http://localhost:8000`.

## Documentación interactiva

FastAPI genera automáticamente documentación interactiva:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## Endpoints

### 1. Listar todas las tareas

**GET** `/tasks`

**Query Parameters:**
- `skip` (int, default=0): Número de tareas a saltar (para paginación).
- `limit` (int, default=100): Número máximo de tareas a retornar.
- `status` (str, opcional): Filtrar por estado ('pending' o 'completed').

**Ejemplos:**

```bash
# Listar todas las tareas
curl -X GET http://localhost:8000/tasks

# Listar solo tareas pendientes
curl -X GET "http://localhost:8000/tasks?status=pending"

# Paginación: saltar 10, traer 20
curl -X GET "http://localhost:8000/tasks?skip=10&limit=20"
```

**Respuesta (200 OK):**
```json
[
  {
    "id": 1,
    "title": "Comprar leche",
    "description": "Leche entera de 1L",
    "status": "pending",
    "priority": "medium",
    "due_date": "2025-10-30",
    "created_at": "2025-10-26T10:30:00",
    "updated_at": "2025-10-26T10:30:00"
  }
]
```

---

### 2. Obtener una tarea específica

**GET** `/tasks/{task_id}`

**Path Parameters:**
- `task_id` (int): ID de la tarea.

**Ejemplos:**

```bash
# Obtener tarea con ID 1
curl -X GET http://localhost:8000/tasks/1
```

**Respuesta (200 OK):**
```json
{
  "id": 1,
  "title": "Comprar leche",
  "description": "Leche entera de 1L",
  "status": "pending",
  "priority": "medium",
  "due_date": "2025-10-30",
  "created_at": "2025-10-26T10:30:00",
  "updated_at": "2025-10-26T10:30:00"
}
```

**Respuesta (404 Not Found):**
```json
{
  "detail": "Tarea no encontrada"
}
```

---

### 3. Crear una nueva tarea

**POST** `/tasks`

**Body (JSON):**
```json
{
  "title": "Comprar leche",
  "description": "Leche entera de 1L",
  "priority": "medium",
  "due_date": "2025-10-30"
}
```

**Campos:**
- `title` (string, requerido): Título de la tarea (1-255 caracteres).
- `description` (string, opcional): Descripción (máx. 2000 caracteres).
- `priority` (string, default="medium"): 'low', 'medium' o 'high'.
- `due_date` (string, opcional): Formato YYYY-MM-DD.

**Ejemplos:**

```bash
# Crear una tarea simple
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Comprar leche"
  }'

# Crear una tarea completa
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Comprar leche",
    "description": "Leche entera de 1L en el supermercado",
    "priority": "high",
    "due_date": "2025-10-30"
  }'
```

**Respuesta (201 Created):**
```json
{
  "id": 1,
  "title": "Comprar leche",
  "description": "Leche entera de 1L",
  "status": "pending",
  "priority": "high",
  "due_date": "2025-10-30",
  "created_at": "2025-10-26T10:30:00",
  "updated_at": "2025-10-26T10:30:00"
}
```

---

### 4. Actualizar una tarea (PUT/PATCH)

**PUT** `/tasks/{task_id}` o **PATCH** `/tasks/{task_id}`

**Path Parameters:**
- `task_id` (int): ID de la tarea.

**Body (JSON):** Todos los campos son opcionales.
```json
{
  "title": "Nuevo título",
  "status": "completed",
  "priority": "low",
  "due_date": "2025-11-01"
}
```

**Ejemplos:**

```bash
# Marcar tarea como completada
curl -X PATCH http://localhost:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{
    "status": "completed"
  }'

# Actualizar múltiples campos
curl -X PUT http://localhost:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Comprar leche de soya",
    "priority": "low",
    "due_date": "2025-11-05"
  }'
```

**Respuesta (200 OK):**
```json
{
  "id": 1,
  "title": "Comprar leche de soya",
  "description": "Leche entera de 1L",
  "status": "completed",
  "priority": "low",
  "due_date": "2025-11-05",
  "created_at": "2025-10-26T10:30:00",
  "updated_at": "2025-10-26T11:45:00"
}
```

---

### 5. Eliminar una tarea

**DELETE** `/tasks/{task_id}`

**Path Parameters:**
- `task_id` (int): ID de la tarea.

**Nota:** Se utiliza *soft-delete* (eliminación lógica), por lo que la tarea no desaparece físicamente de la BD sino que se marca como eliminada.

**Ejemplos:**

```bash
# Eliminar tarea con ID 1
curl -X DELETE http://localhost:8000/tasks/1
```

**Respuesta (204 No Content):** Sin body.

---

### 6. Restaurar una tarea eliminada

**POST** `/tasks/{task_id}/restore`

**Path Parameters:**
- `task_id` (int): ID de la tarea.

**Ejemplos:**

```bash
# Restaurar tarea con ID 1
curl -X POST http://localhost:8000/tasks/1/restore
```

**Respuesta (200 OK):**
```json
{
  "id": 1,
  "title": "Comprar leche de soya",
  "description": "Leche entera de 1L",
  "status": "completed",
  "priority": "low",
  "due_date": "2025-11-05",
  "created_at": "2025-10-26T10:30:00",
  "updated_at": "2025-10-26T11:45:00"
}
```

---

## Flujo de trabajo completo (script de prueba)

```bash
#!/bin/bash

API="http://localhost:8000"

echo "=== 1. Crear una tarea ==="
TASK_RESPONSE=$(curl -s -X POST $API/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Comprar leche",
    "description": "Leche entera de 1L",
    "priority": "high",
    "due_date": "2025-10-30"
  }')
echo $TASK_RESPONSE | python -m json.tool

echo -e "\n=== 2. Listar todas las tareas ==="
curl -s -X GET $API/tasks | python -m json.tool

echo -e "\n=== 3. Obtener tarea específica ==="
curl -s -X GET $API/tasks/1 | python -m json.tool

echo -e "\n=== 4. Actualizar tarea (marcar completada) ==="
curl -s -X PATCH $API/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "completed"}' | python -m json.tool

echo -e "\n=== 5. Listar solo tareas completadas ==="
curl -s -X GET "$API/tasks?status=completed" | python -m json.tool

echo -e "\n=== 6. Eliminar tarea ==="
curl -s -X DELETE $API/tasks/1
echo "Tarea eliminada"

echo -e "\n=== 7. Restaurar tarea ==="
curl -s -X POST $API/tasks/1/restore | python -m json.tool
```

Guardar como `test_api.sh` y ejecutar:
```bash
bash test_api.sh
```

---

## Códigos de estado HTTP

| Código | Significado | Ejemplo |
|--------|-------------|---------|
| 200 | OK | GET exitoso, PATCH exitoso |
| 201 | Created | POST exitoso (tarea creada) |
| 204 | No Content | DELETE exitoso |
| 400 | Bad Request | Datos inválidos |
| 404 | Not Found | Tarea no existe |
| 500 | Server Error | Error interno del servidor |

---

## Validaciones

### Título
- Requerido
- Mínimo 1 carácter
- Máximo 255 caracteres

### Descripción
- Opcional
- Máximo 2000 caracteres

### Prioridad
- Valores válidos: `low`, `medium`, `high`
- Default: `medium`

### Estado
- Valores válidos: `pending`, `completed`
- Default: `pending`

### Fecha de vencimiento
- Opcional
- Formato: `YYYY-MM-DD` (ISO 8601)
- Ejemplo: `2025-10-30`

---

## Notas técnicas

### Soft-delete
Las tareas no se eliminan físicamente de la BD; se marcan con `is_deleted = True`. Esto permite:
- Recuperar tareas eliminadas
- Mantener un historial completo
- Evitar problemas de integridad referencial

### Paginación
Los endpoints de listado soportan paginación mediante `skip` y `limit`:
- `skip=0&limit=10`: primeros 10 registros
- `skip=10&limit=10`: registros 11-20

### Timestamps automáticos
- `created_at`: Se asigna automáticamente al crear la tarea.
- `updated_at`: Se actualiza automáticamente cada vez que se modifica la tarea.

---

## Próximas mejoras

1. **Autenticación:** Añadir JWT para identificar usuarios.
2. **Subtareas:** Relación 1:N con una tabla `subtask`.
3. **Etiquetas:** Relación N:M con una tabla `tag`.
4. **Recordatorios:** Tabla `reminder` y worker de background jobs.
5. **Sincronización:** Endpoints de `/sync` para sincronizar entre dispositivos.
6. **Tests:** Suite de pruebas unitarias e integración con `pytest`.

---

## Licencia

MIT
