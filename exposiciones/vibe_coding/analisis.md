## Resumen funcional

QuickTask es una aplicación de gestión de tareas personales cuyo propósito es permitir a un usuario capturar, organizar y completar tareas con mínima fricción. La aplicación soporta:

- Captura rápida de tareas (título obligatorio, campos opcionales: descripción, vencimiento, hora, prioridad, etiquetas, subtareas, adjuntos).
- Editar y eliminar tareas (con confirmación y papelera/undo opcional).
- Marcar/desmarcar tareas como completadas y mantener historial básico de estado.
- Listados y vistas filtradas (Todas, Activas, Completadas, Hoy, Próximas, por etiqueta), búsqueda y filtros avanzados.
- Subtareas/checklists, recordatorios y recurrencia básica (MVP: reglas comunes como diaria/semanal/mensual).
- Modo local offline con sincronización opcional entre dispositivos y backup/export (CSV/JSON).

Componentes de interacción principales:

- Interfaz de usuario (cliente web/PWA o móvil): captura y presenta listas, formularios y notificaciones locales.
- API backend: persiste tareas, aplica reglas de negocio (recurrencia, generación de instancias), gestiona sincronización y notificaciones.
- Almacenamiento local: cache/IndexedDB (cliente) para uso offline.
- Persistencia en servidor: base de datos relacional (principal) y cache/cola para notificaciones/ops de sincronización.

## Análisis de módulos y componentes

1) Frontend
- Responsabilidad: UI/UX, validaciones básicas, local state, offline-first mediante cache (IndexedDB/Service Worker), sincronización incremental.
- Componentes: lista principal, editor/crear tarea, vista tarea, gestor de etiquetas, panel de filtros, gestor de adjuntos.
- Requisitos no funcionales relevantes: rendimiento (render <300ms para 500 tareas), accesibilidad (WCAG AA), PWA para notificaciones y offline.

2) Backend / API
- Responsabilidad: autenticación (opcional), CRUD completo de tareas, reglas de negocio (recurrencia, subtareas, historial), endpoints de búsqueda/filtrado, endpoints de sincronización/mutación y webhooks/notificaciones.
- API contract: REST (JSON) o GraphQL. Recomendado: REST con endpoints bien versionados y documentación OpenAPI.

3) Persistencia / Base de datos
- Responsabilidad: almacenar tareas, subtareas, etiquetas, usuario, historial y metadatos de sincronización.
- Recomendado: base relacional (PostgreSQL) por modelado claro de relaciones (tareas-subtareas-etiquetas, historial) y soporte para consultas complejas y concurrencia.

4) Cache / Mensajería
- Redis (cache y pub/sub) para: colas de trabajos (recordatorios/cron jobs), locks de sincronización y sesiones rápidas.

5) Servicios externos opcionales
- Servicio de notificaciones (FCM/APNs) para push en móviles.
- Servicio de autenticación tercerizado (Auth0 / Firebase Auth) si se decide externalizar login.
- Almacenamiento de adjuntos: S3-compatible (AWS S3 / Azure Blob / MinIO).

6) Sincronización y offline
- Mecanismo: cliente mantiene un log de cambios local con IDs temporales y timestamps; sincroniza con el servidor usando endpoints /sync que aceptan batches y devuelven resoluciones de conflicto.
- Resolución por defecto: último escritor gana (LWW) con opción de conflicto manual en UI para cambios críticos.

## Tecnologías recomendadas

- Frontend: React + TypeScript (alternativas: Svelte, Vue). PWA enabled, Service Worker, Workbox para offline. UI: TailwindCSS o Material UI.
- Backend: FastAPI (Python) + Uvicorn/Gunicorn para ASGI. Alternativa: Node.js (NestJS/Express + TypeScript) si el equipo prefiere JS full-stack.
- ORM / DB access: SQLAlchemy + Alembic (migrations) si FastAPI; en Node usar TypeORM/Prisma.
- Base de datos: PostgreSQL (producción). Para MVP/local: SQLite con migraciones.
- Cache/cola: Redis (celery/fastapi-background-tasks o RQ para workers). Para Python: Celery/RQ según complejidad.
- Notificaciones: Firebase Cloud Messaging (FCM) para Android/web push; APNs para iOS (si se hace nativo). Opcional: usar un service como OneSignal para simplificar.
- Almacenamiento de archivos: AWS S3 o servicio compatible.
- CI/CD: GitHub Actions o Azure DevOps con pipelines para lint, tests y despliegue.
- Observabilidad: Prometheus + Grafana para métricas; Sentry para errores.

## Riesgos técnicos y mitigaciones

- Riesgo: Conflictos de sincronización entre dispositivos.
	- Mitigación: diseñar esquema con versionado/timestamps por entidad, usar LWW como política por defecto y UI para resolver manualmente. Implementar pruebas e2e para escenarios concurrentes.

- Riesgo: rendimiento en cliente al renderizar muchas tareas.
	- Mitigación: virtualized list rendering (react-window/react-virtualized), paginación/lazy-loading y pruebas de carga con ~500-1000 ítems.

- Riesgo: complejidad de la recurrencia avanzada.
	- Mitigación: comenzar con reglas básicas (diaria/semanal/mensual) en MVP; usar bibliotecas maduras (rrule) si se requiere soporte avanzado más tarde.

- Riesgo: notificaciones push (gestion de tokens y permisos) y divergencias entre plataformas.
	- Mitigación: encapsular integración de push en un servicio modular; usar FCM para web/Android y un flow diferenciado para iOS; pruebas end-to-end en dispositivos reales/emuladores.

- Riesgo: seguridad y privacidad (almacenamiento de credenciales y datos personales).
	- Mitigación: TLS obligatorio, hashing seguro (bcrypt/Argon2) para contraseñas, principios de least-privilege para almacenamiento de adjuntos, y políticas de eliminación de datos.

## Mapa general de dependencias

- Frontend
	- react, react-dom, typescript, react-router, workbox, idb/LocalForage (IndexedDB wrapper), react-window, tailwindcss / MUI

- Backend
	- python 3.11+, fastapi, uvicorn, sqlalchemy, alembic, pydantic, redis, celery (o RQ), boto3 (S3), python-dotenv

- Base de datos
	- postgresql server, pgvector (si más adelante se usan búsquedas semánticas), pg-bouncer (conn pooling)

- Infra / infra-as-code
	- docker, docker-compose (dev), terraform / bicep (prod infra opcional), github-actions

## Justificación técnica de las elecciones

1) Frontend: React + TypeScript
- Razonamiento: React tiene amplio ecosistema, madurez para PWAs y muchas bibliotecas (virtualized lists, componentes accesibles). TypeScript añade seguridad de tipos para mantener calidad a medida que la base crece. Alternativas como Svelte ofrecen bundles más pequeños y mejor perf, pero la curva de adopción del equipo y el ecosistema (módulos, infra) suelen favorecer React.

2) Backend: FastAPI (por qué no Flask)
- Elegí FastAPI como primera opción por:
	- Soporte nativo para asincronía (async/await) y buen rendimiento comparado con Flask tradicional.
	- Validación y parsing declarativo con Pydantic simplifica modelos de entrada/salida y reduce errores.
	- Documentación automática OpenAPI/Swagger, útil para iterar rápido con frontend.

- ¿Y Flask? Flask es más minimalista y tiene menor curva inicial; sin embargo, para una aplicación que puede necesitar concurrencia (notificaciones, sincronización, websockets) y contratos tipados, FastAPI ofrece ventajas a medio plazo. Si el equipo ya domina Flask y proyecto es muy pequeño, Flask puede ser aceptable con extensiones (Flask-RESTful, Marshmallow), pero implicaría más trabajo para añadir async y validación tipada.

3) Base de datos: PostgreSQL vs SQLite
- PostgreSQL es la opción de producción por su robustez, ACID, concurrencia y capacidades avanzadas (JSONB, índices, transacciones). SQLite es útil para prototipos/MVP local, pero no para sincronización multiusuario ni cargas concurrentes.

4) Redis + Celery (o RQ)
- Para tareas en background (envío de notificaciones, generación de instancias recurrentes, limpieza de papelera) se recomienda usar una cola. Celery es más madura y rica en features; RQ es más simple si los requisitos son modestos.

5) Notificaciones: FCM/OneSignal
- FCM cubre web y Android; iOS requiere APNs. OneSignal o servicios similares simplifican integración a costa de vendor lock-in y costes.

## Contrato mínimo y criterios de éxito (pequeño checklist técnico)

- Endpoints CRUD documentados en OpenAPI.
- Frontend capaz de crear/editar/borrar/mostrar tareas y trabajar offline (guardar en IndexedDB y sincronizar).
- Persistencia en PostgreSQL con migraciones y tests unitarios para lógica de recurrencia y sincronización.

## Próximos pasos recomendados

1. Definir alcance MVP (priorizar RF-02, RF-03, RF-05, RF-06, RF-07 como sugerido en `requerimientos.md`).
2. Especificar un esquema de datos inicial (entidades: User, Task, Subtask, Tag, Attachment, TaskHistory, SyncMetadata). Puedo generar el ERD y los modelos si quieres.
3. Prototipo rápido: crear una PWA mínima (React+TS) con IndexedDB y un backend FastAPI con endpoints CRUD básicos y tests unitarios.

---

Si quieres, procedo a cualquiera de estas tareas: (A) generar el ERD y DDL inicial para PostgreSQL, (B) bosquejar el API OpenAPI (endpoints y modelos), o (C) crear el esqueleto de proyecto (repositorio, estructura de carpetas y archivos iniciales). Indica la opción y la priorizo en el todo-list.

