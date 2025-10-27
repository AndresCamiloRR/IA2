"""
crud.py

Funciones CRUD (Create, Read, Update, Delete) para gestionar tareas.
"""

from sqlalchemy.orm import Session
from models import Task
from schemas import TaskCreate, TaskUpdate


def get_tasks(db: Session, skip: int = 0, limit: int = 100, status: str = None):
    """
    Obtiene todas las tareas (no eliminadas).
    
    Args:
        db (Session): Sesión de base de datos.
        skip (int): Número de registros a saltar (para paginación).
        limit (int): Número máximo de registros a retornar.
        status (str): Filtrar por estado ('pending' o 'completed').
    
    Returns:
        list[Task]: Lista de tareas encontradas.
    """
    query = db.query(Task).filter(Task.is_deleted == False)
    
    if status:
        query = query.filter(Task.status == status)
    
    return query.offset(skip).limit(limit).all()


def get_task(db: Session, task_id: int):
    """
    Obtiene una tarea específica por su ID.
    
    Args:
        db (Session): Sesión de base de datos.
        task_id (int): ID de la tarea a recuperar.
    
    Returns:
        Task: Objeto de tarea o None si no existe.
    """
    return db.query(Task).filter(Task.id == task_id, Task.is_deleted == False).first()


def create_task(db: Session, task: TaskCreate):
    """
    Crea una nueva tarea en la base de datos.
    
    Args:
        db (Session): Sesión de base de datos.
        task (TaskCreate): Datos de la tarea a crear.
    
    Returns:
        Task: Objeto de la tarea creada.
    """
    db_task = Task(
        title=task.title,
        description=task.description,
        priority=task.priority,
        due_date=task.due_date,
        status="pending"
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(db: Session, task_id: int, task_update: TaskUpdate):
    """
    Actualiza una tarea existente.
    
    Args:
        db (Session): Sesión de base de datos.
        task_id (int): ID de la tarea a actualizar.
        task_update (TaskUpdate): Datos a actualizar.
    
    Returns:
        Task: Objeto de la tarea actualizada o None si no existe.
    """
    db_task = get_task(db, task_id)
    if not db_task:
        return None
    
    # Actualizar solo los campos que fueron proporcionados
    update_data = task_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int):
    """
    Elimina (soft-delete) una tarea existente.
    
    Args:
        db (Session): Sesión de base de datos.
        task_id (int): ID de la tarea a eliminar.
    
    Returns:
        bool: True si la tarea fue eliminada, False si no existe.
    """
    db_task = get_task(db, task_id)
    if not db_task:
        return False
    
    db_task.is_deleted = True
    db.commit()
    return True


def restore_task(db: Session, task_id: int):
    """
    Restaura una tarea eliminada (soft-delete).
    
    Args:
        db (Session): Sesión de base de datos.
        task_id (int): ID de la tarea a restaurar.
    
    Returns:
        Task: Objeto de la tarea restaurada o None si no existe.
    """
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        return None
    
    db_task.is_deleted = False
    db.commit()
    db.refresh(db_task)
    return db_task
