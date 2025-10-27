"""
models.py

Definición de los modelos ORM usando SQLAlchemy.
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.sql import func
from database import Base


class Task(Base):
    """
    Modelo ORM para la tabla 'task'.
    
    Atributos:
        id (int): Identificador único de la tarea (clave primaria).
        title (str): Título de la tarea (requerido).
        description (str): Descripción detallada de la tarea (opcional).
        status (str): Estado de la tarea ('pending', 'completed').
        priority (str): Prioridad de la tarea ('low', 'medium', 'high').
        due_date (str): Fecha de vencimiento (formato ISO 8601).
        created_at (datetime): Fecha de creación (autogenerada).
        updated_at (datetime): Fecha de última actualización (autogenerada).
    """
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    status = Column(String(20), default="pending", index=True)  # 'pending' o 'completed'
    priority = Column(String(20), default="medium")  # 'low', 'medium', 'high'
    due_date = Column(String(10), nullable=True)  # Formato: YYYY-MM-DD
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', status='{self.status}')>"
