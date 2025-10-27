"""
schemas.py

Definición de los esquemas de validación usando Pydantic.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TaskCreate(BaseModel):
    """
    Esquema para la creación de una nueva tarea.
    
    Atributos:
        title (str): Título de la tarea (requerido).
        description (str): Descripción detallada (opcional).
        priority (str): Prioridad ('low', 'medium', 'high').
        due_date (str): Fecha de vencimiento en formato YYYY-MM-DD (opcional).
    """
    title: str = Field(..., min_length=1, max_length=255, description="Título de la tarea")
    description: Optional[str] = Field(None, max_length=2000, description="Descripción de la tarea")
    priority: str = Field("medium", pattern="^(low|medium|high)$", description="Prioridad de la tarea")
    due_date: Optional[str] = Field(None, pattern=r"^\d{4}-\d{2}-\d{2}$", description="Fecha de vencimiento (YYYY-MM-DD)")


class TaskUpdate(BaseModel):
    """
    Esquema para actualizar una tarea existente.
    Todos los campos son opcionales.
    
    Atributos:
        title (str): Nuevo título (opcional).
        description (str): Nueva descripción (opcional).
        status (str): Nuevo estado ('pending' o 'completed').
        priority (str): Nueva prioridad.
        due_date (str): Nueva fecha de vencimiento.
    """
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)
    status: Optional[str] = Field(None, pattern="^(pending|completed)$")
    priority: Optional[str] = Field(None, pattern="^(low|medium|high)$")
    due_date: Optional[str] = Field(None, pattern=r"^\d{4}-\d{2}-\d{2}$")


class TaskResponse(BaseModel):
    """
    Esquema de respuesta para una tarea.
    Utilizado en las respuestas de la API.
    
    Atributos:
        id (int): Identificador único.
        title (str): Título.
        description (str): Descripción.
        status (str): Estado actual.
        priority (str): Prioridad.
        due_date (str): Fecha de vencimiento.
        created_at (datetime): Fecha de creación.
        updated_at (datetime): Fecha de última actualización.
    """
    id: int
    title: str
    description: Optional[str]
    status: str
    priority: str
    due_date: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Permite construir el esquema desde objetos ORM
