# Ejecutar QuickTask con Docker y docker-compose

Este documento explica cómo construir, levantar y probar la aplicación QuickTask localmente usando Docker y `docker-compose` en Windows PowerShell.

Prerequisitos
- Docker Desktop instalado y funcionando (con WSL2 o el backend que uses).
- `docker-compose` disponible (Docker Desktop incluye compose).
- Estar en la raíz del repositorio donde se encuentra `docker-compose.yaml`.

Resumen de la configuración creada
- `quicktask_backend/Dockerfile` — imagen basada en Python 3.11 que instala dependencias desde `requirements.txt` y ejecuta `uvicorn main:app` en el puerto 8000.
- `docker-compose.yaml` — levanta el servicio `quicktask`, hace build desde `./quicktask_backend`, bind-mountea `./quicktask_backend:/app` para desarrollo y mapea el puerto `8000:8000`.

Puntos importantes
- La aplicación usa SQLite con URL `sqlite:///./tasks.db` (ver `quicktask_backend/database.py`). Esto crea el archivo `tasks.db` en el directorio de trabajo de la app (`/app/tasks.db` dentro del contenedor). Debido al bind-mount, verás `./quicktask_backend/tasks.db` en tu host. Eso proporciona persistencia entre reinicios del contenedor.

Comandos básicos (PowerShell)

1) Construir y levantar en primer plano (útil para ver logs):

```powershell
# Desde la raíz del repo (donde está docker-compose.yaml)
docker-compose up --build
```

2) Levantar en segundo plano (detached):

```powershell
docker-compose up --build -d
```

3) Ver logs del servicio:

```powershell
docker-compose logs -f
# o logs de un servicio específico
docker-compose logs -f quicktask
```

4) Parar y eliminar contenedores creados por compose (no borra archivos locales):

```powershell
docker-compose down
```

5) Parar, eliminar contenedores e imágenes y volúmenes asociados (cuidado con los volúmenes):

```powershell
# Elimina contenedores y red creada por compose
docker-compose down
# Si quieres además eliminar todo lo no usado (contenedores detenidos, imágenes sin etiqueta, volúmenes):
docker system prune --all --volumes
```

Pruebas rápidas (endpoints)

Abrir en navegador
- Health: http://localhost:8000/
- Docs interactivos: http://localhost:8000/docs

Usando PowerShell para llamadas HTTP

- GET raíz (health):

```powershell
Invoke-RestMethod -Uri http://localhost:8000/ -Method GET
```

- Listar tareas (vacío inicialmente):

```powershell
Invoke-RestMethod -Uri http://localhost:8000/tasks -Method GET
```

- Crear una tarea (POST):

```powershell
$body = @{ title = 'Prueba Docker' ; description = 'Creada via docker-compose' } | ConvertTo-Json
Invoke-RestMethod -Uri http://localhost:8000/tasks -Method Post -ContentType 'application/json' -Body $body
```

Ubicación del archivo SQLite

- Dentro del contenedor: `/app/tasks.db`
- En tu host (por el bind-mount): `./quicktask_backend/tasks.db`

Si necesitas usar un volumen Docker para la BD en lugar de bind-mount

La configuración actual monta el código completo para facilitar desarrollo. Si prefieres que el código quede embebido en la imagen y que la base de datos viva en un volumen Docker, hay que:

1. Quitar o modificar el bind-mount en `docker-compose.yaml`.
2. Añadir un volumen y mapearlo a `/app/tasks.db` o a `/app/data` y ajustar `DATABASE_URL` para apuntar a `sqlite:////data/tasks.db`.

Nota sobre rebuild de dependencias
- Si actualizas `requirements.txt`, vuelve a construir la imagen para que pip instale los cambios:

```powershell
docker-compose build --no-cache quicktask
docker-compose up -d
```

Consejos y resolución de problemas
- Si el puerto 8000 ya está en uso, cambia la línea `ports:` en `docker-compose.yaml` (por ejemplo `"8080:8000"`) y usa http://localhost:8080.
- Si ves errores relacionados con dependencias faltantes al iniciar el contenedor, ejecuta los logs (`docker-compose logs`) y revisa que `requirements.txt` contiene las librerías requeridas (FastAPI, uvicorn, SQLAlchemy, etc.).
- En Windows, si tienes problemas con permisos/locks sobre `tasks.db`, asegúrate de que ningún otro proceso local esté abriendo el archivo y que Docker tenga acceso al directorio (WSL2/Shared Drives configurado).

¿Quieres que haga algo más?
- Puedo actualizar la app para leer la URL de la base de datos desde la variable de entorno `DATABASE_URL` (mejor para producción) y luego ajustar `docker-compose.yaml` para usar un volumen nombrado solo para la BD. Dime si te interesa y lo implemento.

---

Archivo(s) relevantes:
- `quicktask_backend/Dockerfile`
- `docker-compose.yaml`
- `quicktask_backend/database.py`