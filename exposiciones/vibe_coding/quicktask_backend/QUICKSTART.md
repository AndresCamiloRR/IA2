# 🚀 Quick Start - QuickTask Backend

## En 5 pasos

### 1. Instalar dependencias
```bash
cd quicktask_backend
pip install -r requirements.txt
```

### 2. Iniciar servidor
```bash
python main.py
```

Verás:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 3. Abrir documentación interactiva
Abre en tu navegador:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### 4. Crear tu primera tarea
```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Mi primera tarea",
    "priority": "high"
  }'
```

### 5. Listar tareas
```bash
curl http://localhost:8000/tasks
```

---

## Comandos útiles

### Crear tarea completa
```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Comprar leche",
    "description": "Leche entera de 1L",
    "priority": "high",
    "due_date": "2025-10-30"
  }'
```

### Listar solo tareas pendientes
```bash
curl "http://localhost:8000/tasks?status=pending"
```

### Listar solo tareas completadas
```bash
curl "http://localhost:8000/tasks?status=completed"
```

### Obtener tarea específica (ID=1)
```bash
curl http://localhost:8000/tasks/1
```

### Marcar como completada
```bash
curl -X PATCH http://localhost:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "completed"}'
```

### Actualizar título y prioridad
```bash
curl -X PATCH http://localhost:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Comprar leche de soya",
    "priority": "low"
  }'
```

### Eliminar tarea
```bash
curl -X DELETE http://localhost:8000/tasks/1
```

### Restaurar tarea eliminada
```bash
curl -X POST http://localhost:8000/tasks/1/restore
```

### Paginación
```bash
curl "http://localhost:8000/tasks?skip=0&limit=10"
```

---

## Ejecutar pruebas

### Suite completa de pruebas
```bash
python test_api.py
```

### Demostración interactiva (con colores)
```bash
python run_demo.py
```

---

## Estructura rápida

```
main.py          ← Punto de entrada (rutas HTTP)
database.py      ← Configuración SQLite
models.py        ← Modelos ORM
schemas.py       ← Validación Pydantic
crud.py          ← Operaciones de BD
```

---

## Códigos de respuesta

| Código | Significado |
|--------|-------------|
| 200 | OK - Solicitud exitosa |
| 201 | Created - Recurso creado |
| 204 | No Content - Eliminado exitosamente |
| 400 | Bad Request - Datos inválidos |
| 404 | Not Found - Recurso no existe |
| 422 | Unprocessable Entity - Error validación |
| 500 | Server Error - Error interno |

---

## Validaciones

- **title**: Obligatorio, 1-255 caracteres
- **description**: Opcional, máx 2000 caracteres
- **priority**: 'low', 'medium', 'high' (default: 'medium')
- **status**: 'pending', 'completed' (default: 'pending')
- **due_date**: Formato YYYY-MM-DD (ej: 2025-10-30)

---

## Documentación completa

- **README.md** → Guía detallada con ejemplos
- **ARCHITECTURE.md** → Diseño técnico y patrones
- **SUMMARY.md** → Resumen ejecutivo del proyecto

---

## Necesitas ayuda?

1. Revisa la documentación en `/docs`
2. Lee el README.md
3. Ejecuta `python test_api.py` para ver ejemplos
4. Revisa el código en main.py

---

**¡Listo para empezar! 🎉**
