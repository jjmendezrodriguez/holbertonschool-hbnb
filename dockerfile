# Use the official Python 3.9 Alpine Linux image / Usa la imagen oficial de Python 3.9 basada en Alpine Linux
FROM python:3.9-alpine

# Set environment variables for unbuffered Python output and app directory / Establece variables de entorno para salida sin búfer de Python y directorio de la aplicación
ENV PYTHONUNBUFFERED=1 \
    APP_HOME=/app

# Set the working directory / Establecer el directorio de trabajo
WORKDIR $APP_HOME

# Install necessary packages and upgrade pip /Instala paquetes necesarios y actualizar pip
RUN apk update && apk add --no-cache \
    build-base \
    libffi-dev \
    openssl-dev \
    python3-dev \
    postgresql-dev \
    && pip install --upgrade pip

# Copy requirements file and install dependencies / Copia el archivo de requisitos e instalar dependencias
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the application code / Copia el código de la aplicación
COPY . .

# Expose port 8000 / Expone el puerto 8000
EXPOSE 8000

# Create a volume for persistent storage / Crea un volumen para almacenamiento persistente
VOLUME /app/data

# Start the app with Gunicorn / Inicia la aplicación con Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
