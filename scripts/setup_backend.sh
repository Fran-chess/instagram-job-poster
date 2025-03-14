#!/bin/bash
# Script para configurar el entorno del backend sin Docker

# Variables
PYTHON_VERSION="3.10"
PROJECT_DIR=$(pwd)
VENV_DIR="$PROJECT_DIR/backend/venv"
ENV_FILE="$PROJECT_DIR/.env"

echo "Configurando el entorno para el backend de Instagram Job Poster..."

# Comprobar si Python está instalado
if ! command -v python$PYTHON_VERSION &> /dev/null; then
    echo "Python $PYTHON_VERSION no está instalado."
    echo "Intenta con: sudo apt install python$PYTHON_VERSION python$PYTHON_VERSION-venv python$PYTHON_VERSION-dev"
    exit 1
fi

# Crear entorno virtual
echo "Creando entorno virtual..."
python$PYTHON_VERSION -m venv $VENV_DIR

# Activar entorno virtual
source $VENV_DIR/bin/activate

# Instalar dependencias
echo "Instalando dependencias..."
pip install --upgrade pip
pip install -r $PROJECT_DIR/backend/requirements.txt

# Crear directorios necesarios
mkdir -p $PROJECT_DIR/backend/media/uploads
mkdir -p $PROJECT_DIR/backend/media/generated
mkdir -p $PROJECT_DIR/backend/resources/fonts

# Configurar variables de entorno
if [ ! -f "$ENV_FILE" ]; then
    echo "Creando archivo .env a partir de la plantilla..."
    cp $PROJECT_DIR/.env.example $ENV_FILE
    echo "Por favor edita el archivo $ENV_FILE con tus configuraciones."
fi

echo "Configuración del backend completada."
echo "Para activar el entorno virtual, ejecuta: source $VENV_DIR/bin/activate"
echo "Para iniciar el servidor de desarrollo, ejecuta: cd backend && uvicorn app.app:app --reload --host 0.0.0.0 --port 8000"