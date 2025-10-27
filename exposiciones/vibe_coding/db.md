# Diseño de Base de Datos y Arquitectura del Sistema — QuickTask

## 1. Modelo Entidad-Relación (E/R)

### 1.1 Descripción textual del modelo

El modelo de datos de QuickTask se estructura alrededor de la entidad principal `User` y su relación con `Task`. A continuación se describen las entidades y sus relaciones:

#### Entidades principales

1. **User** — Representa al usuario del sistema.
   - Atributos: id (PK), email (UNIQUE), password_hash, display_name, created_at, updated_at, is_deleted
   - Relaciones: usuario propietario de múltiples tareas (1:N con Task)
   - Nota: Un usuario puede existir en modo local (sin email/password) o con autenticación completa.

2. **Task** — Representa una tarea creada por un usuario.
   - Atributos: id (PK), user_id (FK), title, description, priority (ENUM), status (ENUM), due_date, due_time, order_index (para ordenación manual), is_deleted, created_at, updated_at, version (para sincronización)
   - Relaciones:
     - Pertenece a un usuario (N:1 con User)
     - Contiene múltiples subtareas (1:N con Subtask)
     - Asociado con múltiples etiquetas (N:M con Tag, vía TaskTag)
     - Tiene múltiples adjuntos (1:N con Attachment)
     - Tiene historial de cambios (1:N con TaskHistory)
     - Tiene metadatos de sincronización (1:1 con SyncMetadata)
     - Puede tener una regla de recurrencia (1:1 con RecurrenceRule)
     - Puede estar relacionado con recordatorios (1:N con Reminder)

3. **Subtask** — Representa un elemento de checklist dentro de una tarea.
   - Atributos: id (PK), task_id (FK), title, is_completed, order_index, created_at, updated_at
   - Relaciones: pertenece a una tarea (N:1 con Task)

4. **Tag** — Representa una etiqueta para categorizar tareas.
   - Atributos: id (PK), user_id (FK), name (UNIQUE por usuario), color (opcional), created_at
   - Relaciones:
     - Pertenece a un usuario (N:1 con User)
     - Asociado con múltiples tareas (N:M con Task, vía TaskTag)

5. **TaskTag** — Tabla de unión para la relación N:M entre Task y Tag.
   - Atributos: id (PK), task_id (FK), tag_id (FK), created_at
   - Relaciones: vincula tareas con etiquetas (N:M)

6. **Attachment** — Representa un archivo adjunto a una tarea.
   - Atributos: id (PK), task_id (FK), filename, file_url (ruta o URL), file_size_bytes, mime_type, created_at
   - Relaciones: pertenece a una tarea (N:1 con Task)

7. **TaskHistory** — Registra cambios históricos en una tarea (auditoría).
   - Atributos: id (PK), task_id (FK), action (ENUM: 'created', 'updated', 'completed', 'deleted', 'restored'), changes_json (cambios en formato JSON), actor_id, timestamp
   - Relaciones: asociado con una tarea (N:1 con Task)

8. **Reminder** — Representa un recordatorio para una tarea.
   - Atributos: id (PK), task_id (FK), reminder_time, reminder_type (ENUM: 'absolute', 'relative'), is_triggered, created_at, updated_at
   - Relaciones: asociado con una tarea (N:1 con Task)

9. **RecurrenceRule** — Define la regla de recurrencia para una tarea.
   - Atributos: id (PK), task_id (FK), recurrence_type (ENUM: 'daily', 'weekly', 'monthly', 'custom'), recurrence_data (JSON con detalles: días de semana, intervalo, etc.), next_occurrence, last_generated_at, is_active, created_at
   - Relaciones: asociado con una tarea (1:1 con Task)

10. **SyncMetadata** — Metadatos para sincronización entre dispositivos.
    - Atributos: id (PK), task_id (FK), client_id (identificador del cliente/dispositivo), version (entero de versionado), last_modified, sync_status (ENUM: 'pending', 'synced', 'conflict')
    - Relaciones: asociado con una tarea (1:1 con Task)

11. **UserSettings** — Preferencias del usuario.
    - Atributos: id (PK), user_id (FK), theme ('light' / 'dark'), default_sort_order (ENUM), language, notifications_enabled, created_at, updated_at
    - Relaciones: pertenece a un usuario (1:1 con User)

#### Cardinalidades resumidas

```
User (1) ─────→ (*) Task
User (1) ─────→ (*) Tag
User (1) ─────→ (1) UserSettings

Task (1) ─────→ (*) Subtask
Task (1) ─────→ (*) Attachment
Task (1) ─────→ (*) TaskHistory
Task (1) ─────→ (1) SyncMetadata
Task (1) ─────→ (1) RecurrenceRule
Task (1) ─────→ (*) Reminder
Task (*) ←─────→ (*) Tag  [vía TaskTag]
```

---

## 2. Esquema SQL (SQLite)

### 2.1 Creación de tablas

```sql
-- ============================================================================
-- TABLA: user
-- Descripción: Almacena información de usuarios del sistema
-- ============================================================================
CREATE TABLE user (
    id TEXT PRIMARY KEY,
    email TEXT UNIQUE,
    password_hash TEXT,
    display_name TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_deleted BOOLEAN DEFAULT 0
);

-- ============================================================================
-- TABLA: user_settings
-- Descripción: Preferencias de visualización y configuración del usuario
-- ============================================================================
CREATE TABLE user_settings (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL UNIQUE,
    theme TEXT DEFAULT 'light' CHECK (theme IN ('light', 'dark')),
    default_sort_order TEXT DEFAULT 'due_date' CHECK (default_sort_order IN ('due_date', 'priority', 'manual')),
    language TEXT DEFAULT 'es' CHECK (language IN ('es', 'en')),
    notifications_enabled BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
);

-- ============================================================================
-- TABLA: tag
-- Descripción: Etiquetas para categorizar tareas (específicas por usuario)
-- ============================================================================
CREATE TABLE tag (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    name TEXT NOT NULL,
    color TEXT DEFAULT '#808080',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
    UNIQUE(user_id, name)
);

-- ============================================================================
-- TABLA: task
-- Descripción: Tareas principales del sistema
-- ============================================================================
CREATE TABLE task (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    priority TEXT DEFAULT 'normal' CHECK (priority IN ('low', 'normal', 'high')),
    status TEXT DEFAULT 'active' CHECK (status IN ('active', 'completed', 'on_hold')),
    due_date DATE,
    due_time TIME,
    order_index INTEGER DEFAULT 0,
    is_deleted BOOLEAN DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    version INTEGER DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
);

-- ============================================================================
-- TABLA: task_tag
-- Descripción: Relación N:M entre tareas y etiquetas
-- ============================================================================
CREATE TABLE task_tag (
    id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    tag_id TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (task_id) REFERENCES task(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tag(id) ON DELETE CASCADE,
    UNIQUE(task_id, tag_id)
);

-- ============================================================================
-- TABLA: subtask
-- Descripción: Elementos de checklist dentro de una tarea
-- ============================================================================
CREATE TABLE subtask (
    id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    title TEXT NOT NULL,
    is_completed BOOLEAN DEFAULT 0,
    order_index INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (task_id) REFERENCES task(id) ON DELETE CASCADE
);

-- ============================================================================
-- TABLA: attachment
-- Descripción: Archivos adjuntos a tareas
-- ============================================================================
CREATE TABLE attachment (
    id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    filename TEXT NOT NULL,
    file_url TEXT NOT NULL,
    file_size_bytes INTEGER,
    mime_type TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (task_id) REFERENCES task(id) ON DELETE CASCADE
);

-- ============================================================================
-- TABLA: reminder
-- Descripción: Recordatorios asociados a tareas
-- ============================================================================
CREATE TABLE reminder (
    id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    reminder_time DATETIME,
    reminder_type TEXT CHECK (reminder_type IN ('absolute', 'relative')),
    relative_days INTEGER,
    is_triggered BOOLEAN DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (task_id) REFERENCES task(id) ON DELETE CASCADE
);

-- ============================================================================
-- TABLA: recurrence_rule
-- Descripción: Reglas de recurrencia para tareas repetitivas
-- ============================================================================
CREATE TABLE recurrence_rule (
    id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL UNIQUE,
    recurrence_type TEXT NOT NULL CHECK (recurrence_type IN ('daily', 'weekly', 'monthly', 'custom')),
    recurrence_data TEXT,
    next_occurrence DATE,
    last_generated_at DATETIME,
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (task_id) REFERENCES task(id) ON DELETE CASCADE
);

-- ============================================================================
-- TABLA: task_history
-- Descripción: Auditoría de cambios en tareas
-- ============================================================================
CREATE TABLE task_history (
    id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    action TEXT NOT NULL CHECK (action IN ('created', 'updated', 'completed', 'deleted', 'restored')),
    changes_json TEXT,
    actor_id TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (task_id) REFERENCES task(id) ON DELETE CASCADE
);

-- ============================================================================
-- TABLA: sync_metadata
-- Descripción: Metadatos para sincronización entre dispositivos
-- ============================================================================
CREATE TABLE sync_metadata (
    id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL UNIQUE,
    client_id TEXT NOT NULL,
    version INTEGER DEFAULT 1,
    last_modified DATETIME DEFAULT CURRENT_TIMESTAMP,
    sync_status TEXT DEFAULT 'synced' CHECK (sync_status IN ('pending', 'synced', 'conflict')),
    FOREIGN KEY (task_id) REFERENCES task(id) ON DELETE CASCADE
);
```

### 2.2 Índices para optimización

```sql
-- ============================================================================
-- ÍNDICES
-- Descripción: Optimización de consultas frecuentes
-- ============================================================================

-- Índices en task para búsquedas por usuario y estado
CREATE INDEX idx_task_user_id ON task(user_id);
CREATE INDEX idx_task_user_status ON task(user_id, status) WHERE is_deleted = 0;
CREATE INDEX idx_task_due_date ON task(due_date) WHERE is_deleted = 0;
CREATE INDEX idx_task_priority ON task(priority) WHERE is_deleted = 0;

-- Índices para sincronización
CREATE INDEX idx_sync_metadata_client_id ON sync_metadata(client_id);
CREATE INDEX idx_sync_metadata_sync_status ON sync_metadata(sync_status);

-- Índices para búsqueda de recordatorios sin disparar
CREATE INDEX idx_reminder_triggered ON reminder(is_triggered, reminder_time);

-- Índices para tareas relacionadas con etiquetas
CREATE INDEX idx_task_tag_tag_id ON task_tag(tag_id);

-- Índices para subtareas
CREATE INDEX idx_subtask_task_id ON subtask(task_id);

-- Índices para historial
CREATE INDEX idx_task_history_task_id ON task_history(task_id);
CREATE INDEX idx_task_history_timestamp ON task_history(timestamp);

-- Índices para adjuntos
CREATE INDEX idx_attachment_task_id ON attachment(task_id);
```

---

## 3. Consideraciones de diseño

### 3.1 Estrategia de identificadores (IDs)

- **Tipo**: TEXT (UUID v4 o ULID)
- **Ventajas**: Compatible con sincronización offline, evita problemas de auto-increment distribuido
- **Implementación**: Generar UUIDs en el cliente/backend antes de persistir

### 3.2 Versionado y sincronización

- Campo `version` en `task` para detectar conflictos
- Tabla `sync_metadata` con:
  - `client_id`: identifica el dispositivo/cliente
  - `version`: número de versión para resolución de conflictos (Last-Writer-Wins por defecto)
  - `sync_status`: estado del registro (pending, synced, conflict)
  - `last_modified`: timestamp para política LWW

### 3.3 Papelera y soft-delete

- Campo `is_deleted` en `user` y `task` para eliminación lógica
- Los índices usan `WHERE is_deleted = 0` para excluir registros eliminados de búsquedas normales
- Permite restauración sin perder historial

### 3.4 Auditoría

- Tabla `task_history` registra todas las acciones importantes
- Campo `changes_json` almacena un diff de cambios (serializado como JSON)
- Permite tracking completo de quién cambió qué y cuándo

### 3.5 Campos de tiempo

- **created_at**, **updated_at**: DATETIME con defaults
- **due_date**, **due_time**: separados para flexibilidad
- **last_modified** en sync_metadata: para resolución de conflictos LWW

### 3.6 Recurrencia

- `recurrence_data` es TEXT/JSON para permitir reglas complejas:
  ```json
  {
    "type": "weekly",
    "interval": 1,
    "days_of_week": ["MON", "WED", "FRI"],
    "until": "2025-12-31",
    "count": null
  }
  ```
- `next_occurrence` se calcula y almacena para queries eficientes

---

## 4. Arquitectura del Sistema

### 4.1 Diagrama de capas (N-Tier Architecture)

```
┌─────────────────────────────────────────────────┐
│            PRESENTATION LAYER (UI)              │
│  ┌──────────────────────────────────────────┐   │
│  │  React SPA (Web) / React Native (Mobile)│   │
│  │  - Task List View                       │   │
│  │  - Task Editor/Creator                  │   │
│  │  - Filters & Search Panel               │   │
│  │  - Settings & Preferences               │   │
│  │  - Sync Status Indicator                │   │
│  └──────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
           ↓ HTTP/REST (JSON) ↓
┌─────────────────────────────────────────────────┐
│            API GATEWAY / ROUTING                │
│  - Authentication middleware                   │
│  - Rate limiting                               │
│  - Request validation & logging                │
└─────────────────────────────────────────────────┘
           ↓ HTTP/JSON ↓
┌─────────────────────────────────────────────────┐
│          BUSINESS LOGIC LAYER (Backend)         │
│  ┌──────────────────────────────────────────┐   │
│  │  Task Service                            │   │
│  │    - CRUD operations (create, read, etc) │   │
│  │    - Search & filtering logic            │   │
│  │    - Recurrence generation               │   │
│  │  Sync Service                            │   │
│  │    - Conflict resolution (LWW policy)    │   │
│  │    - Batch sync processing               │   │
│  │  Reminder Service                        │   │
│  │    - Schedule management                 │   │
│  │    - Notification dispatching            │   │
│  │  User Service                            │   │
│  │    - Authentication & Authorization      │   │
│  │    - Settings management                 │   │
│  │  Tag Service                             │   │
│  │    - Tag CRUD & categorization           │   │
│  └──────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
           ↓ SQL/Transactions ↓
┌─────────────────────────────────────────────────┐
│             DATA ACCESS LAYER (DAL)             │
│  ┌──────────────────────────────────────────┐   │
│  │  Task Repository                         │   │
│  │  User Repository                         │   │
│  │  Tag Repository                          │   │
│  │  Reminder Repository                     │   │
│  │  - Query building & execution            │   │
│  │  - Transaction management                │   │
│  │  - Connection pooling                    │   │
│  └──────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
           ↓ SQL (SQLite/PostgreSQL) ↓
┌─────────────────────────────────────────────────┐
│            DATABASE LAYER                       │
│  - SQLite (local/MVP)                          │
│  - PostgreSQL (production)                     │
│  - Indexes & query optimization               │
└─────────────────────────────────────────────────┘
```

### 4.2 Componentes y responsabilidades

#### Capa de Presentación (Frontend)

**Responsabilidades:**
- Renderizar UI de tareas
- Capturar entrada del usuario
- Validaciones básicas en cliente
- Gestionar estado local (Redux/Zustand/Context API)
- Sincronización local con IndexedDB/LocalForage para offline

**Componentes principales:**
- `TaskListView`: Muestra lista filtrada de tareas
- `TaskEditor`: Formulario para crear/editar tareas
- `FilterPanel`: Filtros (estado, prioridad, etiqueta, fecha)
- `SearchBox`: Búsqueda por título/descripción
- `SyncIndicator`: Estado de sincronización
- `SettingsPanel`: Preferencias de usuario

**Tecnología recomendada:**
- React + TypeScript
- Redux Toolkit / Zustand para state management
- Workbox / Service Worker para offline
- IndexedDB / LocalForage para cache local

---

#### API Gateway / Middleware

**Responsabilidades:**
- Enrutamiento de requests
- Autenticación (JWT tokens)
- Autorización (RBAC/ABAC)
- Validación de entrada (schemas)
- Rate limiting
- Logging y monitoreo
- CORS management

**Endpoints principales:**
```
POST   /api/v1/auth/register
POST   /api/v1/auth/login
POST   /api/v1/auth/refresh

GET    /api/v1/tasks
POST   /api/v1/tasks
GET    /api/v1/tasks/:id
PUT    /api/v1/tasks/:id
DELETE /api/v1/tasks/:id

POST   /api/v1/tasks/:id/complete
POST   /api/v1/tasks/:id/restore

GET    /api/v1/tasks/search?q=...
GET    /api/v1/tasks/filter?status=...&priority=...&tag=...

POST   /api/v1/sync
GET    /api/v1/sync/status

POST   /api/v1/reminders/:id/trigger
GET    /api/v1/reminders

POST   /api/v1/tags
GET    /api/v1/tags
PUT    /api/v1/tags/:id
DELETE /api/v1/tags/:id

GET    /api/v1/export?format=json|csv
POST   /api/v1/import

GET    /api/v1/settings
PUT    /api/v1/settings
```

---

#### Capa de Lógica de Negocio (Backend Services)

**1. Task Service**

```
TaskService:
  ├─ createTask(userId, dto) → Task
  │   └─ Validar entrada
  │   └─ Generar UUID
  │   └─ Guardar en repositorio
  │   └─ Registrar en historial
  │   └─ Retornar task creada
  │
  ├─ updateTask(userId, taskId, dto) → Task
  │   └─ Verificar pertenencia (authorization)
  │   └─ Actualizar campos
  │   └─ Incrementar version
  │   └─ Registrar cambios en historial
  │   └─ Retornar task actualizada
  │
  ├─ deleteTask(userId, taskId) → void
  │   └─ Soft-delete (is_deleted = 1)
  │   └─ Registrar acción en historial
  │
  ├─ restoreTask(userId, taskId) → Task
  │   └─ Recuperar de papelera (is_deleted = 0)
  │   └─ Registrar restauración
  │
  ├─ markComplete(userId, taskId) → Task
  │   └─ status = 'completed'
  │   └─ completed_at = now()
  │   └─ Generar próxima instancia si recurrente
  │
  ├─ markIncomplete(userId, taskId) → Task
  │   └─ status = 'active'
  │   └─ Registrar reversión
  │
  ├─ searchTasks(userId, query, filters) → List<Task>
  │   └─ Ejecutar búsqueda full-text o LIKE
  │   └─ Aplicar filtros (status, priority, tag, fecha)
  │   └─ Ordenar según preferencia
  │   └─ Retornar resultados paginados
  │
  └─ getTasksByView(userId, view: 'today'|'upcoming'|'completed'|'all') → List<Task>
      └─ Filtrar según vista solicitada
      └─ Aplicar ordenación
```

**2. Sync Service**

```
SyncService:
  ├─ pushChanges(userId, clientId, changes: Batch) → SyncResponse
  │   └─ Para cada cambio en el batch:
  │   │   ├─ Verificar versión y timestamp
  │   │   ├─ Aplicar política LWW si conflicto
  │   │   ├─ Persistir cambio
  │   │   └─ Registrar en sync_metadata
  │   └─ Retornar resoluciones y conflictos
  │
  ├─ pullChanges(userId, clientId, lastSync: timestamp) → Batch
  │   └─ Obtener cambios desde lastSync
  │   └─ Construir batch con cambios
  │   └─ Retornar batch al cliente
  │
  └─ resolveConflict(taskId, localVersion, remoteVersion) → Task
      └─ Comparar timestamps (last_modified)
      └─ Aplicar "última versión gana"
      └─ O marcar para resolución manual en UI
```

**3. Reminder Service**

```
ReminderService:
  ├─ scheduleReminder(taskId, reminderTime, reminderType) → Reminder
  │   └─ Validar time/date
  │   └─ Calcular absolute/relative time
  │   └─ Guardar en base de datos
  │   └─ Programar en cron/scheduler
  │
  ├─ sendReminder(reminderId) → void
  │   └─ Obtener tarea asociada
  │   └─ Disparar notificación (local/push)
  │   └─ Marcar como triggered
  │
  └─ getPendingReminders() → List<Reminder>
      └─ Buscar reminders con is_triggered = 0
      └─ Filtrar por tiempo actual
```

**4. Recurrence Service**

```
RecurrenceService:
  ├─ createRecurrenceRule(taskId, rule: RecurrenceRule) → void
  │   └─ Validar regla (daily/weekly/monthly/custom)
  │   └─ Guardar en recurrence_rule
  │   └─ Calcular next_occurrence
  │
  ├─ generateNextOccurrence(taskId) → Task
  │   └─ Obtener regla recurrente
  │   └─ Calcular próxima fecha
  │   └─ Crear nueva instancia de tarea
  │   └─ Actualizar next_occurrence
  │   └─ Retornar nueva tarea
  │
  └─ isRecurrent(taskId) → bool
      └─ Verificar si tiene RecurrenceRule activa
```

**5. User Service**

```
UserService:
  ├─ register(email, password, displayName) → User
  │   └─ Validar email único
  │   └─ Hash contraseña (bcrypt/Argon2)
  │   └─ Crear usuario
  │   └─ Inicializar user_settings
  │
  ├─ authenticate(email, password) → AuthToken
  │   └─ Buscar usuario por email
  │   └─ Verificar contraseña
  │   └─ Generar JWT token
  │
  ├─ updateSettings(userId, settings) → UserSettings
  │   └─ Validar campos
  │   └─ Actualizar preferencias
  │
  └─ deleteUser(userId) → void
      └─ Soft-delete user (GDPR compliance)
      └─ Registrar en auditoría
```

---

#### Capa de Acceso a Datos (Data Access Layer)

**Repository Pattern:**

```
TaskRepository:
  ├─ findById(taskId) → Task
  ├─ findByUserId(userId, filters?) → List<Task>
  ├─ findByUserIdAndStatus(userId, status) → List<Task>
  ├─ findWithTags(taskId) → Task (with tag list)
  ├─ save(task) → Task
  ├─ update(task) → Task
  ├─ delete(taskId) → void
  └─ search(userId, query, filters) → List<Task>

UserRepository:
  ├─ findById(userId) → User
  ├─ findByEmail(email) → User
  ├─ save(user) → User
  └─ update(user) → User

TagRepository:
  ├─ findById(tagId) → Tag
  ├─ findByUserId(userId) → List<Tag>
  ├─ save(tag) → Tag
  └─ delete(tagId) → void

ReminderRepository:
  ├─ findById(reminderId) → Reminder
  ├─ findByTaskId(taskId) → List<Reminder>
  ├─ findPending() → List<Reminder>
  └─ save(reminder) → Reminder

SubtaskRepository:
  ├─ findByTaskId(taskId) → List<Subtask>
  ├─ save(subtask) → Subtask
  └─ update(subtask) → Subtask
```

---

### 4.3 Flujo de comunicación — Caso de uso: Crear tarea

```
1. Usuario abre formulario de nueva tarea (Frontend)
   ↓
2. Usuario ingresa título, descripción, prioridad, etc.
   ↓
3. Usuario presiona "Guardar"
   ↓
4. Frontend valida campos obligatorios localmente
   ↓
5. Frontend genera UUID local
   ↓
6. Frontend persiste en IndexedDB (offline-first)
   ↓
7. Frontend envía POST /api/v1/tasks con datos
   ↓
8. API Gateway valida token JWT
   ↓
9. Backend TaskService.createTask(userId, dto) ejecuta:
   ├─ Validar entrada (Pydantic schema)
   ├─ Generar UUID (server-side confirmación)
   ├─ Guardar en BD vía TaskRepository.save()
   ├─ Registrar en TaskHistory (action='created')
   ├─ Crear SyncMetadata entry
   └─ Retornar Task creada
   ↓
10. API responde con 201 + Task JSON
    ↓
11. Frontend actualiza IndexedDB con ID confirma del servidor
    ↓
12. Frontend actualiza TaskListView
    ↓
13. Usuario ve nueva tarea en lista
    ↓
14. [Opcional] Frontend marca como synced en sync_metadata
```

---

### 4.4 Flujo de comunicación — Caso de uso: Sincronización offline-first

```
ESCENARIO 1: Cambio local → Sync a servidor

1. Usuario en dispositivo A crea/edita tarea (sin conexión)
   ├─ Cambio persiste en IndexedDB local
   └─ Marcado como "pending" en sync_metadata local

2. Conexión se restablece
   ↓
3. Frontend detecta conectividad
   ↓
4. Frontend inicia POST /api/v1/sync con batch de cambios:
   {
     "clientId": "device-uuid",
     "changes": [
       {
         "taskId": "task-1",
         "action": "updated",
         "version": 2,
         "lastModified": "2025-01-15T10:30:00Z",
         "data": { "status": "completed", ... }
       }
     ]
   }
   ↓
5. Backend SyncService.pushChanges() ejecuta:
   ├─ Para cada cambio:
   │   ├─ Obtener task actual de BD
   │   ├─ Comparar versions/timestamps
   │   ├─ Si no hay conflicto → apply LWW logic
   │   └─ Si hay conflicto → marcar sync_status='conflict'
   └─ Retornar resoluciones

6. Frontend recibe respuesta:
   {
     "synced": [{ "taskId": "task-1", "version": 2 }],
     "conflicts": []
   }
   ↓
7. Frontend actualiza IndexedDB: sync_status='synced' para task-1
   ↓
8. SyncIndicator muestra "Todo sincronizado"

---

ESCENARIO 2: Cambio en dispositivo B → Pull a dispositivo A

1. Usuario en dispositivo B edita tarea (conectado)
   └─ Cambio guardado en servidor, sync_metadata.version = 3

2. Usuario en dispositivo A (conectado también)
   ├─ Frontend periodicamente (cada 30s) o manualmente:
   │   POST /api/v1/sync con { "lastSync": "2025-01-15T10:00:00Z" }
   ↓
3. Backend SyncService.pullChanges(userId, lastSync) retorna:
   {
     "changes": [
       {
         "taskId": "task-1",
         "action": "updated",
         "version": 3,
         "lastModified": "2025-01-15T10:45:00Z",
         "data": { "title": "Nueva descripción", ... }
       }
     ]
   }
   ↓
4. Frontend aplica cambios localmente a IndexedDB
   ↓
5. Frontend re-renderiza TaskListView con datos actualizados
   ↓
6. Usuario en dispositivo A ve cambio hecho en dispositivo B
```

---

### 4.5 Estrategia de persistencia local (Frontend)

**IndexedDB Schema:**

```javascript
// Almacenamiento local en el navegador/app
const localDB = {
  stores: {
    users: { keyPath: 'id' },
    tasks: { keyPath: 'id', indexes: ['userId', 'status', 'dueDate'] },
    tags: { keyPath: 'id', indexes: ['userId'] },
    subtasks: { keyPath: 'id', indexes: ['taskId'] },
    reminders: { keyPath: 'id', indexes: ['taskId'] },
    syncMetadata: { keyPath: 'taskId', indexes: ['syncStatus', 'clientId'] }
  }
}

// Cada registro en syncMetadata incluye:
{
  taskId: 'uuid',
  clientId: 'device-uuid',
  version: 2,
  lastModified: '2025-01-15T10:30:00Z',
  syncStatus: 'pending' | 'synced' | 'conflict'
}
```

---

### 4.6 Resolución de conflictos

**Política por defecto: Last-Writer-Wins (LWW)**

```
Cuando dos cambios compiten (e.g., editado en dos dispositivos):

task1 en Server:  version=3, lastModified='2025-01-15T10:45:00Z', title="A"
task1 en Device:  version=2, lastModified='2025-01-15T10:30:00Z', title="B"

Comparación de timestamps:
  10:45:00 (server) > 10:30:00 (device)
  → Servidor gana
  → task1 en Device se sobrescribe con title="A", version=3

Ventajas:
  ✓ Determinístico y sin complicaciones
  ✓ No se pierde información de quién cambió qué (guardado en history)

Desventajas:
  ✗ Puede sobrescribir cambios en conflicto
  ✗ Para tareas críticas, UI puede ofrecer resolución manual
```

**Resolución manual (opcional):**

```
Si syncStatus='conflict' en UI:
  → Mostrar dialog: "Conflicto detectado"
  → Mostrar lado a lado: versión local vs remota
  → Permitir usuario elegir qué aplicar
  → Actualizar version local con decisión
  → Re-sincronizar
```

---

### 4.7 Notificaciones y Reminders

**Flujo de ejecución:**

```
Backend Background Job (Celery/RQ):
  1. Cada minuto, ejecutar CheckPendingReminders
  2. Buscar reminders con:
     - is_triggered = 0
     - reminder_time <= NOW()
  3. Para cada reminder:
     ├─ Obtener tarea asociada
     ├─ Obtener usuario
     ├─ Decidir canal:
     │   ├─ Si user.notifications_enabled = true
     │   │   ├─ Enviar push vía FCM (web/android)
     │   │   └─ O notificación local (browser Notification API)
     │   └─ Registrar en log
     └─ Marcar reminder: is_triggered = 1
  4. Loguear ejecución para debugging

Frontend (PWA):
  1. Service Worker registra notificación
  2. Usuario ve popup con texto de tarea
  3. Click en notificación abre app y muestra tarea
```

---

### 4.8 Importar/Exportar

**Exportar a JSON:**

```json
{
  "exported_at": "2025-01-15T10:30:00Z",
  "format_version": "1.0",
  "user": {
    "email": "user@example.com",
    "display_name": "John Doe"
  },
  "tasks": [
    {
      "id": "uuid",
      "title": "...",
      "description": "...",
      "status": "active",
      "priority": "high",
      "due_date": "2025-01-20",
      "created_at": "2025-01-15T10:00:00Z",
      "subtasks": [...],
      "tags": [...]
    }
  ],
  "tags": [...]
}
```

**Exportar a CSV:**

```
title,description,status,priority,due_date,tags
"Comprar leche","Leche entera 1L",active,normal,2025-01-20,"grocery,weekly"
"Reunión Q1","Planning trimestral",completed,high,2025-01-15,"work,meeting"
```

**Importar:**

```
1. Usuario sube archivo (JSON o CSV)
2. Frontend parsea y valida schema
3. Para cada tarea:
   ├─ Generar UUID
   ├─ Validar campos obligatorios (title)
   ├─ Persistir en IndexedDB
   ├─ Marcar para sincronización
4. Mostrar progress bar
5. Al finalizar, re-sincronizar con servidor
```

---

### 4.9 Seguridad y autenticación

**Flujo de autenticación:**

```
1. Usuario ingresa email + password en login form
2. Frontend POST /api/v1/auth/login
3. Backend:
   ├─ Buscar usuario por email
   ├─ Comparar password hash con contraseña ingresada (bcrypt)
   ├─ Si válido:
   │   ├─ Generar JWT token (con exp: 24h)
   │   ├─ Retornar { accessToken, refreshToken }
   │   └─ [Opcional] refresh token se guarda en httpOnly cookie
   └─ Si inválido: retornar 401
4. Frontend almacena accessToken
5. Subsecuentes requests incluyen:
   Authorization: Bearer <accessToken>
6. API Gateway valida JWT en cada request
7. Si token vencido, frontend usa refreshToken para obtener nuevo accessToken
8. [Offline] Modo local sin autenticación si no se registra
```

**Seguridad en almacenamiento de contraseñas:**

- Usar **bcrypt** (Python: `bcrypt.hashpw()`) con salt rounds >= 12
- O **Argon2** para mayor resistencia contra ataques GPU
- NUNCA almacenar plain text

---

### 4.10 Escalabilidad y deployment

**Arquitectura escalable para producción:**

```
Frontend:
  ├─ CDN (Cloudflare/AWS CloudFront) para assets estáticos
  ├─ Single Page App (React build optimizado)
  └─ Service Worker para caching

Backend:
  ├─ Load Balancer (AWS ALB / Nginx)
  ├─ N× FastAPI instances (Uvicorn + Gunicorn)
  └─ Connection Pool a PostgreSQL

Datos:
  ├─ PostgreSQL cluster (Primary + Replicas)
  ├─ Backups automáticos
  └─ Connection pooling (PgBouncer)

Cache:
  ├─ Redis (session storage, rate limiting)
  └─ Opcional: Redis cluster para alta disponibilidad

Background Jobs:
  ├─ Celery workers (or RQ workers)
  ├─ Message broker: Redis/RabbitMQ
  └─ Periodic tasks: recordatorios, cleanup, etc.

Monitoreo:
  ├─ Prometheus (métricas)
  ├─ Grafana (dashboards)
  ├─ Sentry (error tracking)
  └─ ELK/Loki (log aggregation)

Deployment:
  ├─ Docker containers
  ├─ Kubernetes (EKS/AKS/GKE) para orquestación
  ├─ GitHub Actions para CI/CD
  └─ Infrastructure as Code (Terraform/Bicep)
```

---

## 5. Coherencia con requerimientos

### Mapeo: Requerimientos → Diseño

| RF | Descripción | Implementación en diseño |
|:--:|---|---|
| RF-01 | Registro/Inicio sesión opcional | User table + user_settings; JWT auth opcional |
| RF-02 | Crear tarea | Task table + TaskService.createTask() |
| RF-03 | Editar tarea | Task table + TaskService.updateTask() + TaskHistory |
| RF-04 | Eliminar tarea | is_deleted flag + papelera lógica + TaskHistory |
| RF-05 | Marcar completada | status enum + TaskService.markComplete() |
| RF-06 | Listados/vistas | TaskRepository.findByUserIdAndStatus() + indexes |
| RF-07 | Búsqueda/filtrado | TaskService.searchTasks() + índices en BD |
| RF-08 | Subtareas | Subtask table 1:N con Task |
| RF-09 | Recordatorios | Reminder table + ReminderService + background jobs |
| RF-10 | Recurrencia | RecurrenceRule table + RecurrenceService |
| RF-11 | Etiquetas | Tag + TaskTag (N:M) + TagService |
| RF-12 | Ordenación manual | order_index en Task |
| RF-13 | Importar/Exportar | Servicios en backend + parseo en frontend |
| RF-14 | Sincronización | sync_metadata table + SyncService + LWW policy |
| RF-15 | Backup/Restauración | Exportar JSON + re-importar |
| RF-16 | Auditoría | TaskHistory table |
| RF-17 | Preferencias | user_settings table |

### Validación de NFRs

| NFR | Criterio | Validación |
|:--:|---|---|
| NFR-01 | Rendimiento <300ms para 500 tareas | Indexes en task(user_id, status); IndexedDB local para caché |
| NFR-02 | 99.5% disponibilidad | PostgreSQL + replicas; loadbalancing; CI/CD automated |
| NFR-03 | Escalabilidad horizontal | Backend stateless + message queue; sync_metadata para resolución distribuida |
| NFR-04 | Seguridad/privacidad | bcrypt hashing; is_deleted para GDPR; TLS obligatorio |
| NFR-05 | Integridad/persistencia | Transacciones ACID; TaskHistory audit; LWW sync |
| NFR-06 | Usabilidad WCAG AA | Responsabilidad del frontend (accesibilidad semántica HTML) |
| NFR-07 | Localización i18n | user_settings.language; frontend i18n framework |
| NFR-08 | Resiliencia offline | IndexedDB + Service Worker + sync batch |
| NFR-09 | Límites almacenamiento | file_size_bytes + constraints en attachment table |
| NFR-10 | Pruebas/mantenibilidad | Test suite unitaria para services + integration tests |

---

## 6. Próximos pasos

1. **DDL SQL production-ready**: Adaptar SQLite DDL a PostgreSQL para producción (agregar SERIAL, CONSTRAINTS avanzadas).
2. **Migraciones**: Crear versión inicial con Alembic (Python) o Flyway/Liquibase si se usa Java.
3. **API OpenAPI spec**: Documentar endpoints CRUD con Swagger/OpenAPI.
4. **Modelos en código**: Generar modelos SQLAlchemy (Python) o TypeORM (Node.js) basados en este schema.
5. **Tests unitarios**: Escribir tests para cada Service (task, sync, reminder, user).
6. **Frontend integration**: Implementar Redux store + API client para consumir endpoints.
7. **E2E tests**: Validar flujos completos (crear → editar → completar → sincronizar).

