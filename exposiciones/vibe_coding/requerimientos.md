# QuickTask — Requerimientos

## 1. Descripción general del sistema

QuickTask es una aplicación de gestión de tareas personales que permite a los usuarios crear, editar, organizar y marcar tareas como completadas. Está diseñada para uso individual, con sincronización opcional entre dispositivos, recordatorios y filtros para priorizar el trabajo diario. El objetivo principal es proporcionar un flujo simple y rápido para capturar tareas y gestionarlas hasta su finalización.

## 2. Actores principales
- Usuario (Usuario final): Persona que crea y gestiona tareas.
- Sistema (QuickTask): La aplicación que almacena, procesa y presenta las tareas.
- Servicio de notificaciones (opcional): Servicio responsable de enviar recordatorios/push/alertas.
- Servicio de autenticación (si aplica): Gestiona cuentas y sesiones del usuario.
- Servicio de sincronización/almacenamiento remoto (opcional): Sincroniza datos entre dispositivos y realiza copias de seguridad.

## 3. Requerimientos funcionales (RF)
Cada requisito incluye una frase verificable (criterio de prueba breve).

**RF-01 — Registro / Inicio de sesión opcional**
- Descripción: El sistema debe permitir al usuario crear una cuenta (email + contraseña) e iniciar sesión. También debe existir la opción de usar la app en modo local sin cuenta.
- Verificación: Se puede crear una cuenta válida y autenticar con credenciales; en modo local, la app funciona sin autenticación.
- Prioridad: Media

**RF-02 — Crear tarea**
- Descripción: El usuario debe poder crear una tarea nueva proporcionando título obligatorio y campos opcionales: descripción, fecha de vencimiento, hora, prioridad (baja/normal/alta), etiquetas, subtareas y adjuntos.
- Verificación: Al guardar, la tarea aparece en la lista con los campos ingresados.
- Prioridad: Alta

**RF-03 — Editar tarea**
- Descripción: El usuario debe poder editar cualquier campo de una tarea existente y guardar los cambios.
- Verificación: Los cambios se persisten y se muestran inmediatamente.
- Prioridad: Alta

**RF-04 — Eliminar tarea**
- Descripción: El usuario debe poder eliminar una tarea; el sistema pedirá confirmación. Debe existir papelera/undo (opcional) para restaurar en un plazo determinado.
- Verificación: La tarea desaparece tras confirmar y puede restaurarse si la función papelera está activada.
- Prioridad: Media

**RF-05 — Marcar como completada / desmarcar**
- Descripción: El usuario puede marcar una tarea como completada y revertir esa acción (desmarcar).
- Verificación: El estado de la tarea cambia y se muestra visualmente; el historial del estado se guarda.
- Prioridad: Alta

**RF-06 — Listado y vista de tareas**
- Descripción: El sistema debe listar las tareas del usuario en una vista principal con orden por fecha, prioridad o manual. Deberá soportar vistas: Todas, Activas, Completadas, Hoy, Próximas, por Etiqueta.
- Verificación: Filtros y vistas muestran el subconjunto correcto de tareas.
- Prioridad: Alta

**RF-07 — Búsqueda y filtrado avanzado**
- Descripción: El usuario debe poder buscar tareas por texto (título/descripcion), filtrar por fecha, prioridad, etiqueta y estado.
- Verificación: Los resultados de búsqueda/filtrado coinciden con los criterios ingresados.
- Prioridad: Media

**RF-08 — Subtareas / checklist**
- Descripción: Una tarea puede contener subtareas o elementos de checklist que también puedan marcarse como completados individualmente.
- Verificación: Subtareas pueden añadirse, editarse y marcarse; el progreso se refleja en la tarea padre.
- Prioridad: Media

**RF-09 — Recordatorios y notificaciones**
- Descripción: El usuario puede definir recordatorios basados en fecha/hora o en intervalos relativos (por ejemplo, 1 día antes). El sistema enviará notificaciones locales o push según plataforma.
- Verificación: Notificación se dispara en el tiempo configurado (simulable en pruebas).
- Prioridad: Media

**RF-10 — Recurrencia de tareas**
- Descripción: Permitir programar tareas recurrentes (diarias, semanales, mensuales, personalizadas).
- Verificación: Se genera la próxima instancia recurrente tras completar la actual (según la regla).
- Prioridad: Baja-Media

**RF-11 — Etiquetas y categorización**
- Descripción: El usuario puede crear y asignar etiquetas a tareas. El sistema muestra la lista de etiquetas y permite filtrar por ellas.
- Verificación: Búsqueda/filtrado por etiqueta funciona; etiquetas se pueden crear y eliminar.
- Prioridad: Media

**RF-12 — Ordenación manual y prioridad**
- Descripción: Permitir reordenar tareas manualmente (drag & drop) en listas y ajustar prioridad.
- Verificación: El orden manual se mantiene y persiste entre sesiones.
- Prioridad: Media

**RF-13 — Importar/Exportar**
- Descripción: Permitir exportar tareas a formato estándar (CSV/JSON) e importar desde esos formatos (con validación básica).
- Verificación: Un archivo exportado contiene las tareas; importación crea tareas equivalentes.
- Prioridad: Baja

**RF-14 — Sincronización entre dispositivos (opcional)**
- Descripción: Si el usuario inicia sesión, sus tareas se sincronizan en la nube y se reflejan en otros dispositivos del mismo usuario.
- Verificación: Cambio en dispositivo A aparece en dispositivo B en un plazo máximo definido (p.ej. 5s-30s).
- Prioridad: Opcional/Alta si multidevice

**RF-15 — Backup y restauración**
- Descripción: Permitir al usuario crear y restaurar backups de sus tareas (local o nube).
- Verificación: Un backup descargado puede restaurarse y recuperar las tareas.
- Prioridad: Baja

**RF-16 — Auditoría básica / historial de cambios**
- Descripción: Registrar cambios clave (creación, edición importante, estado) para poder mostrar un historial simple.
- Verificación: Historial muestra entradas con timestamp y acción.
- Prioridad: Baja

**RF-17 — Preferencias de visualización**
- Descripción: Usuario puede elegir tema (claro/oscuro), tamaño de fuente y forma de orden por defecto.
- Verificación: Preferencias aplicadas inmediatamente y persistidas.
- Prioridad: Baja

## 4. Requerimientos no funcionales (NFR)
Cada NFR debe ser medible cuando aplique.

**NFR-01 — Rendimiento**
- La lista principal de tareas debe cargar y ser interactiva en < 300 ms para hasta 500 tareas locales.
- Las operaciones CRUD básicas (crear/editar/marcar) deben completarse en < 200 ms en condiciones normales (red local).

**NFR-02 — Disponibilidad**
- Si hay sincronización en la nube, el servicio debe garantizar 99.5% de disponibilidad mensual (si se contrata un servicio externo, documentar SLA).

**NFR-03 — Escalabilidad**
- La arquitectura debe soportar crecimiento de usuarios; la solución debe escalar horizontalmente para el servicio de sincronización.

**NFR-04 — Seguridad y privacidad**
- Datos sensibles (credenciales) deben almacenarse con hashing seguro (PBKDF2/ bcrypt/Argon2) y transmisión con TLS 1.2+.
- Usuarios deben poder eliminar su cuenta y datos (GDPR/LPD compliance si aplica).
- Acceso a adjuntos debe estar autenticado.

**NFR-05 — Integridad y persistencia**
- No debe perderse una tarea tras confirmación de guardado. Sincronización eventual puede aplicarse, pero se deben resolver conflictos con la última modificación del usuario o con políticas claras (p.ej. último escritor gana o mergeable).

**NFR-06 — Usabilidad**
- Tiempo de aprendizaje < 5 minutos para funciones básicas.
- El UI debe seguir principios de accesibilidad (WCAG AA): contraste, navegación con teclado y soporte lector de pantalla.

**NFR-07 — Localización**
- Soportar i18n; inicialmente Español (es-CO/ es-ES) e Inglés, con posibilidad de añadir otros idiomas.

**NFR-08 — Resiliencia / Offline**
- La app debe permitir uso offline para crear/editar/ marcar tareas; los cambios se sincronizan cuando la conexión se restablece.
- En caso de conflicto de sincronización, mostrar UI para resolver o aplicar política automática predefinida.

**NFR-09 — Tamaño de almacenamiento y adjuntos**
- Tamaño máximo por adjunto: 10 MB (configurable).
- Límite por usuario: configurable; documentar cuota.

**NFR-10 — Mantenibilidad y pruebas**
- Código debe tener cobertura unitaria mínima (p.ej. 60%) y CI automatizado para builds y tests.

## 5. Criterios de aceptación (al menos 3 funciones clave)
Usar formato Given / When / Then.

**Función clave A — Crear tarea (RF-02)**
- Given: El usuario ha abierto la vista "Nueva tarea".
- When: El usuario introduce "Título" válido y presiona "Guardar".
- Then: La nueva tarea aparece en la lista principal con el mismo título; los campos opcionales aparecen vacíos por defecto; la tarea persiste después de recargar la aplicación o cerrar y abrir la sesión.

**Función clave B — Editar tarea (RF-03)**
- Given: Existe una tarea "Comprar leche" creada previamente.
- When: El usuario abre la tarea, cambia la fecha de vencimiento y presiona "Guardar".
- Then: La tarea muestra la fecha actualizada en la vista principal y el cambio se persiste (se verifica tras recargar o sincronizar).

**Función clave C — Marcar como completada (RF-05)**
- Given: Hay una tarea activa en la lista.
- When: El usuario marca la tarea como completada (checkbox o swipe).
- Then: La tarea cambia visualmente a estado "Completada" (p.ej. tachado), desaparece de la vista "Activas" y aparece en "Completadas"; el cambio puede revertirse mediante "Desmarcar".

**Adicional — Sincronización (RF-14) (criterio)**
- Given: Usuario A tiene la app abierta en dos dispositivos con la misma cuenta.
- When: Usuario A crea o edita una tarea en dispositivo 1 y guarda.
- Then: El cambio aparece en dispositivo 2 dentro del tiempo máximo especificado (p.ej. 30s) o tras un refresh manual.

## 6. Suposiciones y restricciones
**Suposiciones**
- La aplicación está diseñada principalmente como un gestor de tareas personales (no para gestión avanzada de proyectos multiusuario).
- Si hay sincronización, el servicio de backend y notificaciones pueden ser provistos por servicios en la nube (p.ej. Firebase, AWS).
- El usuario desea una experiencia rápida y minimalista; complejidad extra (workflows avanzados) se prioriza después del MVP.
- Plataformas objetivo iniciales: Web (responsive) y móviles (iOS/Android) o progresive web app (PWA) según decisión de alcance.

**Restricciones**
- Si se usa almacenamiento en la nube, se aplican límites de cuota y costos operativos.
- El soporte offline y resolución de conflictos puede incrementar la complejidad; definir alcance para MVP.
- Integración con servicios de terceros (calendar, email, slack) requerirá acuerdos y permisos adicionales.
- Si se requiere cumplimiento legal (GDPR), se debe incluir puntos de privacidad y eliminación de datos.

## 7. Riesgos y ambigüedades (para discusión con el cliente)
- Alcance de sincronización: ¿es obligatorio sincronizar entre dispositivos en el MVP o se deja como mejora?
- Modo local vs cuentas: ¿se requiere que TODOS los usuarios tengan cuenta o se acepta modo local sin autenticación?
- Nivel de detalle para recurrencia: Las reglas complejas de recurrencia (p. ej. "cada primer lunes") pueden ser costosas de implementar — confirmar alcance.
- Notificaciones push: ¿Se aceptan soluciones basadas en servicios externos (p. ej. FCM/APNs)? Requerirá manejo de tokens y permisos.
- Adjuntos y cuotas: Definir política clara sobre tamaño y tipos de archivos permitidos.
- Conflictos al sincronizar cambios concurrentes: confirmar la política de resolución preferida (último escritor gana, merge, UI de resolución).
- Requisitos legales y de privacidad según mercados objetivo (GDPR, local data residency) — confirmar si aplican.
- Compatibilidad multiplataforma: ¿se prioriza PWA o apps nativas? Impacta diseño, notificaciones y offline.

---

Entrega: documento estructurado listo para revisión.

Siguientes pasos propuestos (si quieres que continúe):
- Actualizo este contenido en `requerimientos.md` del repositorio.
- Genero una versión "MVP" priorizando RFs de alta prioridad (RF-02, RF-03, RF-05, RF-06, RF-07).
- Si confirmas, creo criterios de aceptación adicionales y un backlog mínimo para el sprint 0.

Dime cuál de los siguientes prefieres: actualizar `requerimientos.md` con este contenido ahora, o primero ajustar prioridades/alcance para un MVP.

