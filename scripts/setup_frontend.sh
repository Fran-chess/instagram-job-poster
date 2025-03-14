#!/bin/bash
# Script para configurar el entorno del frontend sin Docker

# Variables
NODE_VERSION="20"
PROJECT_DIR=$(pwd)
ENV_FILE="$PROJECT_DIR/.env"
NODE_MODULES_DIR="$PROJECT_DIR/frontend/node_modules"

echo "Configurando el entorno para el frontend de Instagram Job Poster..."

# Comprobar si Node.js está instalado
if ! command -v node &> /dev/null; then
    echo "Node.js no está instalado."
    echo "Instálalo desde https://nodejs.org/ o mediante NVM"
    exit 1
fi

# Verificar la versión de Node.js
CURRENT_NODE_VERSION=$(node -v | cut -d 'v' -f 2 | cut -d '.' -f 1)
if [ "$CURRENT_NODE_VERSION" -lt "$NODE_VERSION" ]; then
    echo "Se requiere Node.js versión $NODE_VERSION o superior."
    echo "Versión actual: $(node -v)"
    echo "Por favor, actualiza Node.js"
    exit 1
fi

# Instalar dependencias
echo "Instalando dependencias del frontend..."
cd $PROJECT_DIR/frontend
npm install

# Crear directorios necesarios
mkdir -p $PROJECT_DIR/frontend/public/placeholder

# Verificar archivo .env
if [ ! -f "$ENV_FILE" ]; then
    echo "Creando archivo .env a partir de la plantilla..."
    cp $PROJECT_DIR/.env.example $ENV_FILE
    echo "Por favor edita el archivo $ENV_FILE con tus configuraciones."
else
    # Asegurarse de que la variable NEXT_PUBLIC_API_URL está configurada
    if ! grep -q "NEXT_PUBLIC_API_URL" "$ENV_FILE"; then
        echo "Añadiendo NEXT_PUBLIC_API_URL al archivo .env..."
        echo "NEXT_PUBLIC_API_URL=http://localhost:8000/api" >> $ENV_FILE
    fi
fi

echo "Configuración del frontend completada."
echo "Para iniciar el servidor de desarrollo, ejecuta: cd frontend && npm run dev"