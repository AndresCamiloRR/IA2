## Diagrama de Casos de Uso (PlantUML)

```plantuml
@startuml
left to right direction
actor User
actor "AuthService (optional)" as AuthService
actor "NotificationService (optional)" as NotificationService

rectangle "QuickTask System" {
	User -- (Usar en modo local)
	User -- (Registrar / Iniciar sesión)
	User -- (Crear tarea)
	User -- (Editar tarea)
	User -- (Eliminar tarea)
	User -- (Restaurar tarea desde papelera)
	User -- (Marcar/Desmarcar completada)
	User -- (Ver listados / Filtrar / Buscar)
	User -- (Gestionar subtareas / checklist)
	User -- (Gestionar etiquetas)
	User -- (Configurar recordatorio)
	User -- (Configurar recurrencia básica)
	User -- (Importar / Exportar CSV/JSON)
	User -- (Backup / Restauración)
	User -- (Ajustes de visualización)
	User -- (Sincronizar cambios)

	(Registrar / Iniciar sesión) .up.> AuthService : uses
	(Configurar recordatorio) .up.> NotificationService : uses
}

note right of User
	Actor principal: usuario final que crea y
	gestiona tareas. AuthService y Notification
	Service son actores externos opcionales.
end note

@enduml
```
![alt text](image.png)

## Diagrama de Clases (PlantUML)

```plantuml
@startuml
skinparam classAttributeIconSize 0

class User {
	+UUID id
	+String email
	+String displayName
	+DateTime createdAt
	+DateTime updatedAt
	+settings: Map
	+register(email,password)
	+authenticate(email,password)
}

class Task {
	+UUID id
	+String title
	+String description
	+DateTime dueDate
	+DateTime dueTime
	+Priority priority
	+Status status
	+List<Tag> tags
	+List<Attachment> attachments
	+RecurrenceRule recurrence
	+Bool deleted
	+DateTime createdAt
	+DateTime updatedAt
	+addSubtask(subtask)
	+markCompleted()
	+update(fields)
}

class Subtask {
	+UUID id
	+String title
	+Bool completed
	+Int order
	+toggle()
}

class Tag {
	+UUID id
	+String name
	+DateTime createdAt
}

class Attachment {
	+UUID id
	+String filename
	+String url
	+Int sizeBytes
}

class TaskHistory {
	+UUID id
	+UUID taskId
	+String action
	+String actorId
	+DateTime timestamp
}

class SyncMetadata {
	+UUID id
	+UUID taskId
	+String clientId
	+Int version
	+DateTime lastModified
}

class TaskService {
	+createTask(user, dto)
	+updateTask(user, taskId, dto)
	+deleteTask(user, taskId)
	+restoreTask(user, taskId)
	+markComplete(user, taskId)
	+search(user, query)
	+syncChanges(user, changes)
}

class TaskRepository {
	+findById(id)
	+findByUser(userId, filter)
	+save(task)
	+delete(taskId)
}

class NotificationService {
	+scheduleReminder(taskId, dateTime)
	+sendPush(userId, payload)
}

User "1" o-- "*" Task : owns
Task "1" o-- "*" Subtask : contains
Task "*" -- "*" Tag : tagged
Task "1" o-- "*" Attachment : has
Task "1" o-- "*" TaskHistory : history
Task "1" o-- "1" SyncMetadata : sync

TaskService ..> TaskRepository : uses
TaskService ..> NotificationService : uses

@enduml
```
![alt text](image-1.png)

## Explicación breve

- Diagrama de Casos de Uso: muestra actores y los casos de uso principales cubiertos por los requerimientos. El actor `User` puede operar en modo local o (opcionalmente) registrarse para sincronización; `AuthService` y `NotificationService` aparecen como actores externos opcionales para reflejar funciones de autenticación y envío de recordatorios/push.

- Diagrama de Clases: define el modelo de dominio esencial y los servicios que encapsulan la lógica (por ejemplo `TaskService` y `TaskRepository`). Incluye entidades persistentes (`Task`, `Subtask`, `Tag`, `Attachment`, `TaskHistory`, `SyncMetadata`) con atributos clave y métodos representativos. Las relaciones muestran propiedad y cardinalidades esperadas.

Estos diagramas usan PlantUML; puedes renderizarlos copiando los bloques `plantuml` en cualquier visor PlantUML (online o local) o usando extensiones de VS Code que soporten PlantUML.

