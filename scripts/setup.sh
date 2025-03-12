#!/bin/bash
# Script de configuración inicial del proyecto

# Verificar prerrequisitos
echo "Verificando prerrequisitos..."
command -v python3 >/dev/null 2>&1 || { echo "Python 3 no está instalado. Abortando."; exit 1; }
command -v pip >/dev/null 2>&1 || { echo "Pip no está instalado. Abortando."; exit 1; }
command -v node >/dev/null 2>&1 || { echo "Node.js no está instalado. Abortando."; exit 1; }
command -v npm >/dev/null 2>&1 || { echo "NPM no está instalado. Abortando."; exit 1; }

# Configurar entorno virtual Python
echo "Configurando entorno virtual Python..."
cd ../backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configurar variables de entorno
echo "Configurando variables de entorno..."
cd ..
cp .env.example .env
echo "Por favor, edita el archivo .env con tus configuraciones."

# Instalar dependencias de frontend
echo "Instalando dependencias de frontend..."
cd frontend
npm install

echo "Configuración completada con éxito."
echo "Para iniciar el backend: cd ../backend && source venv/bin/activate && uvicorn app.main:app --reload"
echo "Para iniciar el frontend: cd ../frontend && npm run dev"
