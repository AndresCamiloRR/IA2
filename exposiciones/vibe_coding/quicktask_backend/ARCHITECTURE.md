# Arquitectura del Backend QuickTask

## Diagrama general

```
┌─────────────────────────────────────────────────────────────┐
│                        Cliente (Browser)                     │
│              (Realiza peticiones HTTP/REST)                  │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP Request/Response
┌────────────────────────▼────────────────────────────────────┐
│                    FastAPI App (main.py)                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Rutas (Routes) - Endpoints CRUD                    │   │
│  │  • GET /tasks                                        │   │
│  │  • POST /tasks                                       │   │
│  │  • GET /tasks/{id}                                   │   │
│  │  • PUT/PATCH /tasks/{id}                             │   │
│  │  • DELETE /tasks/{id}                                │   │
│  │  • POST /tasks/{id}/restore                          │   │
│  └──────────────────────────────────────────────────────┘   │
│                         │                                    │
│  ┌──────────────────────▼──────────────────────────────┐   │
│  │  Validación (Pydantic - schemas.py)                 │   │
│  │  • TaskCreate                                        │   │
│  │  • TaskUpdate                                        │   │
│  │  • TaskResponse                                      │   │
│  └──────────────────────────────────────────────────────┘   │
│                         │                                    │
│  ┌──────────────────────▼──────────────────────────────┐   │
│  │  Lógica de Negocio (crud.py)                        │   │
│  │  • create_task()                                     │   │
│  │  • read_task()                                       │   │
│  │  • update_task()                                     │   │
│  │  • delete_task()                                     │   │
│  │  • restore_task()                                    │   │
│  │  • get_tasks() con filtros                           │   │
│  └──────────────────────────────────────────────────────┘   │
│                         │                                    │
│  ┌──────────────────────▼──────────────────────────────┐   │
│  │  Acceso a datos (SQLAlchemy ORM - models.py)        │   │
│  │  • Task Model                                        │   │
│  │  • Session Management (database.py)                 │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │ SQL Queries
┌────────────────────────▼────────────────────────────────────┐
│                  SQLite Database                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Tabla: tasks                                        │   │
│  │  ├── id (INTEGER, PRIMARY KEY)                       │   │
│  │  ├── title (VARCHAR, NOT NULL)                       │   │
│  │  ├── description (TEXT)                              │   │
│  │  ├── status (VARCHAR) - 'pending'/'completed'        │   │
│  │  ├── priority (VARCHAR) - 'low'/'medium'/'high'      │   │
│  │  ├── due_date (VARCHAR) - YYYY-MM-DD                 │   │
│  │  ├── is_deleted (BOOLEAN)                            │   │
│  │  ├── created_at (DATETIME)                           │   │
│  │  └── updated_at (DATETIME)                           │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  Archivo: tasks.db (SQLite)                                 │
└──────────────────────────────────────────────────────────────┘
```

## Flujo de una solicitud (Request Flow)

### Ejemplo: Crear una nueva tarea

```
1. Cliente envía:
   POST /tasks
   Content-Type: application/json
   {
     "title": "Comprar leche",
     "priority": "high",
     "due_date": "2025-10-30"
   }

2. FastAPI recibe la solicitud
   ↓ (main.py - ruta /tasks)

3. Pydantic valida los datos
   ↓ (schemas.py - TaskCreate)
   ✓ Título válido (no vacío)
   ✓ Prioridad válida (high/medium/low)
   ✓ Fecha válida (formato YYYY-MM-DD)

4. Se inyecta la sesión de BD
   ↓ (database.py - get_db)

5. Se ejecuta la lógica CRUD
   ↓ (crud.py - create_task)
   • Crea objeto Task
   • Lo añade a la sesión
   • Hace commit a la BD

6. SQLAlchemy genera SQL
   ↓ (models.py - Task ORM)
   INSERT INTO tasks (title, priority, due_date, status, created_at, updated_at)
   VALUES ('Comprar leche', 'high', '2025-10-30', 'pending', NOW(), NOW())

7. SQLite ejecuta la query
   ↓
   ✓ Tarea insertada con ID 1

8. FastAPI retorna respuesta
   ↓ (schemas.py - TaskResponse)
   201 Created
   {
     "id": 1,
     "title": "Comprar leche",
     "description": null,
     "status": "pending",
     "priority": "high",
     "due_date": "2025-10-30",
     "created_at": "2025-10-26T10:30:00",
     "updated_at": "2025-10-26T10:30:00"
   }
```

## Estructura de módulos

### 1. **main.py** - Aplicación principal
```python
# Crear app FastAPI
app = FastAPI(...)

# Definir rutas (endpoints)
@app.get("/tasks")
def list_tasks(...): ...

@app.post("/tasks")
def create_task(...): ...

# Iniciar servidor
if __name__ == "__main__":
    uvicorn.run(app, ...)
```

**Responsabilidades:**
- Definir todas las rutas HTTP
- Inyectar dependencias
- Manejar códigos de estado
- Generar documentación OpenAPI

---

### 2. **database.py** - Configuración de BD
```python
# Configurar SQLAlchemy
DATABASE_URL = "sqlite:///./tasks.db"
engine = create_engine(DATABASE_URL, ...)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Dependencia para inyección
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**Responsabilidades:**
- Configurar conexión a BD
- Crear sesiones
- Proporcionar dependencia para FastAPI

---

### 3. **models.py** - Modelos ORM
```python
class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    # ... más columnas
```

**Responsabilidades:**
- Mapear tablas de BD a clases Python
- Definir tipos y restricciones
- Generar esquema SQL

---

### 4. **schemas.py** - Esquemas Pydantic
```python
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str = "medium"
    # ...

class TaskResponse(BaseModel):
    id: int
    title: str
    # ...
```

**Responsabilidades:**
- Validar datos de entrada (CREATE)
- Serializar datos de salida (RESPONSE)
- Documentar contratos API

---

### 5. **crud.py** - Operaciones CRUD
```python
def create_task(db: Session, task: TaskCreate):
    db_task = Task(**task.dict())
    db.add(db_task)
    db.commit()
    return db_task

def get_tasks(db: Session, ...):
    return db.query(Task).filter(...).all()

def update_task(db: Session, task_id: int, ...):
    db_task = db.query(Task).get(task_id)
    # actualizar...
    db.commit()
    return db_task
```

**Responsabilidades:**
- Encapsular lógica de base de datos
- Reutilizar código CRUD
- Separar BD de rutas HTTP

---

## Patrones de diseño utilizados

### 1. **Dependency Injection (DI)**
```python
# En main.py
@app.get("/tasks")
def list_tasks(db: Session = Depends(get_db)):
    # FastAPI automáticamente inyecta la sesión
    return crud.get_tasks(db)
```

**Ventajas:** Testeable, desacoplado, reutilizable.

---

### 2. **Separation of Concerns (SoC)**
- **main.py** → Rutas HTTP
- **schemas.py** → Validación
- **models.py** → Persistencia
- **crud.py** → Lógica de negocio

**Ventajas:** Código mantenible, fácil de testear, claro.

---

### 3. **Soft-Delete**
```python
# En lugar de DELETE físico
db_task.is_deleted = True  # Marca como eliminado
db.commit()

# En las queries, se filtra automáticamente
query = db.query(Task).filter(Task.is_deleted == False)
```

**Ventajas:** Recuperabilidad, auditoría, integridad referencial.

---

### 4. **Repository Pattern**
```python
# crud.py actúa como repositorio
# Encapsula todas las queries a la BD
# main.py solo llama a crud.*, no directamente a la BD
```

---

## Ciclo de vida de una solicitud

```
1. Cliente hace solicitud HTTP
   ↓
2. FastAPI router encuentra la ruta
   ↓
3. Se resuelven dependencias (ej: get_db)
   ↓
4. Se valida el body con Pydantic
   ↓
5. Se ejecuta la función (handler)
   ↓
6. La función llama a crud.*
   ↓
7. crud.* usa la sesión ORM
   ↓
8. SQLAlchemy traduce a SQL
   ↓
9. SQLite ejecuta la query
   ↓
10. Se devuelve el resultado
    ↓
11. Pydantic serializa la respuesta
    ↓
12. FastAPI envía respuesta HTTP al cliente
```

---

## Mejoras futuras en arquitectura

### 1. **Agregar autenticación**
```python
# auth.py
from fastapi.security import HTTPBearer, HTTPAuthCredentials

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthCredentials = Depends(security)):
    # Validar token JWT
    return decode_jwt(credentials.credentials)

# En las rutas
@app.get("/tasks")
def list_tasks(current_user = Depends(get_current_user), db = Depends(get_db)):
    # Solo tareas del usuario actual
    return crud.get_tasks(db, user_id=current_user.id)
```

---

### 2. **Agregar logging y monitoreo**
```python
import logging

logger = logging.getLogger(__name__)

@app.post("/tasks")
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    logger.info(f"Creating task: {task.title}")
    result = crud.create_task(db, task)
    logger.info(f"Task created with ID: {result.id}")
    return result
```

---

### 3. **Agregar caché**
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_task_cached(task_id: int, db: Session):
    return crud.get_task(db, task_id)
```

---

### 4. **Agregar tests**
```python
# test_api.py (como ya existe)
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_task():
    response = client.post("/tasks", json={"title": "Test"})
    assert response.status_code == 201
```

---

## Resumen de tecnologías

| Capa | Tecnología | Propósito |
|------|-----------|----------|
| **Web Framework** | FastAPI | Rutas HTTP, documentación automática |
| **Servidor** | Uvicorn | Servidor ASGI de alto rendimiento |
| **Validación** | Pydantic | Esquemas y validación de datos |
| **ORM** | SQLAlchemy | Mapeo de objetos a BD |
| **Base de datos** | SQLite | Persistencia de datos |
| **Testing** | requests, pytest | Pruebas (futuro) |

---

## Performance considerations

1. **Índices en BD** - Acelera búsquedas
2. **Paginación** - Reduce transferencia de datos
3. **Caché** - Evita queries repetidas
4. **Connection pooling** - Reutiliza conexiones
5. **Async/await** - FastAPI es nativo asincrónico

---

## Seguridad

1. **Validación de entrada** - Pydantic previene inyección SQL
2. **Soft-delete** - No pierde datos
3. **CORS (futuro)** - Controlar acceso desde otros dominios
4. **HTTPS (futuro)** - Encriptación en tránsito
5. **Autenticación (futuro)** - JWT o sesiones
