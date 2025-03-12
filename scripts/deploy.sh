#!/bin/bash
# Script para desplegar la aplicación

# Variables
DEPLOY_ENV=${1:-"development"}  # Por defecto, desplegar en entorno de desarrollo

# Validar el entorno
if [[ "$DEPLOY_ENV" != "development" && "$DEPLOY_ENV" != "production" ]]; then
  echo "Error: El entorno debe ser 'development' o 'production'"
  exit 1
fi

echo "Desplegando en entorno: $DEPLOY_ENV"

# Actualizar código desde el repositorio
git pull origin main

# Construir imágenes de Docker
docker-compose build

# Detener contenedores antiguos y iniciar los nuevos
docker-compose down
docker-compose up -d

echo "Despliegue completado con éxito en entorno $DEPLOY_ENV"
