"""
database.py

Configuración de la conexión a SQLite y creación del engine de SQLAlchemy.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Ruta a la base de datos SQLite
DATABASE_URL = "sqlite:///./tasks.db"

# Crear el engine de SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # Necesario para SQLite
)

# Crear la sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos ORM
Base = declarative_base()


def get_db():
    """
    Dependencia para inyectar la sesión de base de datos en las rutas.
    
    Yields:
        Session: Sesión de SQLAlchemy para la solicitud actual.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
