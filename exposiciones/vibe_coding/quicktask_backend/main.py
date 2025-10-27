"""
main.py

Aplicación principal de FastAPI con los endpoints CRUD para gestionar tareas.
"""

from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import engine, get_db, Base
import crud
import models
import schemas

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Crear la aplicación FastAPI
app = FastAPI(
    title="QuickTask API",
    description="API REST para gestionar tareas personales",
    version="1.0.0"
)


# ============================================================================
# ENDPOINTS CRUD
# ============================================================================

@app.get("/", tags=["Health"])
def read_root():
    """
    Endpoint raíz para verificar que la API está activa.
    
    Returns:
        dict: Mensaje de bienvenida.
    """
    return {
        "message": "¡Bienvenido a QuickTask API!",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/tasks", response_model=list[schemas.TaskResponse], tags=["Tasks"])
def list_tasks(
    skip: int = Query(0, ge=0, description="Número de tareas a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de tareas"),
    status: str = Query(None, regex="^(pending|completed)$", description="Filtrar por estado"),
    db: Session = Depends(get_db)
):
    """
    Lista todas las tareas (no eliminadas).
    
    Query Parameters:
        skip (int): Offset para paginación.
        limit (int): Límite de resultados.
        status (str): Filtro opcional por estado ('pending' o 'completed').
    
    Returns:
        list[TaskResponse]: Lista de tareas.
    """
    tasks = crud.get_tasks(db, skip=skip, limit=limit, status=status)
    return tasks


@app.get("/tasks/{task_id}", response_model=schemas.TaskResponse, tags=["Tasks"])
def get_task(task_id: int, db: Session = Depends(get_db)):
    """
    Obtiene una tarea específica por su ID.
    
    Path Parameters:
        task_id (int): ID de la tarea.
    
    Returns:
        TaskResponse: Datos de la tarea.
    
    Raises:
        HTTPException: Si la tarea no existe (404).
    """
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return db_task


@app.post("/tasks", response_model=schemas.TaskResponse, status_code=201, tags=["Tasks"])
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    """
    Crea una nueva tarea.
    
    Body:
        TaskCreate: Datos de la tarea a crear.
    
    Returns:
        TaskResponse: Datos de la tarea creada.
    """
    return crud.create_task(db=db, task=task)


@app.put("/tasks/{task_id}", response_model=schemas.TaskResponse, tags=["Tasks"])
def update_task(
    task_id: int,
    task_update: schemas.TaskUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualiza una tarea existente.
    
    Path Parameters:
        task_id (int): ID de la tarea.
    
    Body:
        TaskUpdate: Datos a actualizar (todos opcionales).
    
    Returns:
        TaskResponse: Datos de la tarea actualizada.
    
    Raises:
        HTTPException: Si la tarea no existe (404).
    """
    db_task = crud.update_task(db=db, task_id=task_id, task_update=task_update)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return db_task


@app.patch("/tasks/{task_id}", response_model=schemas.TaskResponse, tags=["Tasks"])
def patch_task(
    task_id: int,
    task_update: schemas.TaskUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualiza parcialmente una tarea (alias para PUT).
    
    Path Parameters:
        task_id (int): ID de la tarea.
    
    Body:
        TaskUpdate: Datos a actualizar.
    
    Returns:
        TaskResponse: Datos de la tarea actualizada.
    
    Raises:
        HTTPException: Si la tarea no existe (404).
    """
    db_task = crud.update_task(db=db, task_id=task_id, task_update=task_update)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return db_task


@app.delete("/tasks/{task_id}", status_code=204, tags=["Tasks"])
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """
    Elimina una tarea (soft-delete).
    
    Path Parameters:
        task_id (int): ID de la tarea.
    
    Raises:
        HTTPException: Si la tarea no existe (404).
    """
    success = crud.delete_task(db=db, task_id=task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")


@app.post("/tasks/{task_id}/restore", response_model=schemas.TaskResponse, tags=["Tasks"])
def restore_task(task_id: int, db: Session = Depends(get_db)):
    """
    Restaura una tarea eliminada.
    
    Path Parameters:
        task_id (int): ID de la tarea.
    
    Returns:
        TaskResponse: Datos de la tarea restaurada.
    
    Raises:
        HTTPException: Si la tarea no existe (404).
    """
    db_task = crud.restore_task(db=db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return db_task


# ============================================================================
# MANEJO DE ERRORES GLOBAL
# ============================================================================

@app.exception_handler(ValueError)
def value_error_handler(request, exc):
    """Maneja excepciones de valor."""
    return {"detail": str(exc)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
