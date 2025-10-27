FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar solo requirements primero para aprovechar cache de Docker
COPY requirements.txt /app/

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . /app

# Puerto que usa la aplicación (uvicorn por defecto en main.py usa 8000)
EXPOSE 8000

# Comando por defecto
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
