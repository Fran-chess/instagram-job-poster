#!/bin/bash
# Script para configurar el proyecto Instagram Job Poster sin Docker
# Ejecutar con: bash setup.sh [development|production]

# Colores para mensajes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Variables
PROJECT_DIR=$(pwd)
ENV_TYPE="${1:-development}"  # Por defecto, desarrollo

# Verificar el entorno solicitado
if [[ "$ENV_TYPE" != "development" && "$ENV_TYPE" != "production" ]]; then
  echo -e "${RED}Error: El entorno debe ser 'development' o 'production'${NC}"
  exit 1
fi

echo -e "${GREEN}Configurando el proyecto Instagram Job Poster en entorno: $ENV_TYPE${NC}"

# 1. Verificar prerrequisitos
echo -e "\n${YELLOW}Verificando prerrequisitos...${NC}"

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 no está instalado.${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | awk '{print $2}' | cut -d '.' -f 1,2)
if (( $(echo "$PYTHON_VERSION < 3.8" | bc -l) )); then
    echo -e "${RED}Error: Se requiere Python 3.8 o superior. Versión detectada: $PYTHON_VERSION${NC}"
    exit 1
fi

# Verificar Node.js
if ! command -v node &> /dev/null; then
    echo -e "${RED}Error: Node.js no está instalado.${NC}"
    exit 1
fi

NODE_VERSION=$(node --version | cut -d 'v' -f 2 | cut -d '.' -f 1)
if [[ "$NODE_VERSION" -lt 16 ]]; then
    echo -e "${RED}Error: Se requiere Node.js 16 o superior. Versión detectada: $(node --version)${NC}"
    exit 1
fi

# 2. Configurar variables de entorno
echo -e "\n${YELLOW}Configurando variables de entorno...${NC}"
if [ ! -f "$PROJECT_DIR/.env" ]; then
    cp "$PROJECT_DIR/.env.example" "$PROJECT_DIR/.env"
    echo -e "${GREEN}Archivo .env creado. Por favor edítalo con tus configuraciones.${NC}"
    
    # Configurar URLs según el entorno
    if [ "$ENV_TYPE" = "development" ]; then
        echo "NEXT_PUBLIC_API_URL=http://localhost:8000/api" >> "$PROJECT_DIR/.env"
    else
        echo -e "${YELLOW}Por favor, añade NEXT_PUBLIC_API_URL=https://tudominio.com/api al archivo .env${NC}"
    fi
fi

# 3. Configurar Backend
echo -e "\n${YELLOW}Configurando el backend...${NC}"

# Crear entorno virtual
VENV_DIR="$PROJECT_DIR/backend/venv"
python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"

# Instalar dependencias
pip install --upgrade pip
pip install -r "$PROJECT_DIR/backend/requirements.txt"

# Crear directorios necesarios
mkdir -p "$PROJECT_DIR/backend/media/uploads"
mkdir -p "$PROJECT_DIR/backend/media/generated"
mkdir -p "$PROJECT_DIR/backend/resources/fonts"

echo -e "${GREEN}Configuración del backend completada.${NC}"

# 4. Configurar Frontend
echo -e "\n${YELLOW}Configurando el frontend...${NC}"

# Instalar dependencias
cd "$PROJECT_DIR/frontend"
npm install

# Crear directorio para archivos estáticos
mkdir -p "$PROJECT_DIR/frontend/public/placeholder"

# Si estamos en producción, construir el frontend
if [ "$ENV_TYPE" = "production" ]; then
    npm run build
fi

echo -e "${GREEN}Configuración del frontend completada.${NC}"

# 5. Configurar sistema según entorno
if [ "$ENV_TYPE" = "production" ]; then
    echo -e "\n${YELLOW}Configurando para producción...${NC}"
    
    # Aquí podrías añadir comandos adicionales para producción
    echo -e "${GREEN}Nota: Para el entorno de producción, sigue las instrucciones detalladas en docs/despliegue_sin_docker.md${NC}"
else
    echo -e "\n${YELLOW}Configurando para desarrollo...${NC}"
    
    # Configurar scripts para iniciar
    cat > "$PROJECT_DIR/start_dev.sh" << 'EOF'
#!/bin/bash
# Script para iniciar el entorno de desarrollo

# Variables
PROJECT_DIR=$(pwd)

# Iniciar backend
echo "Iniciando backend..."
cd "$PROJECT_DIR/backend"
source venv/bin/activate
uvicorn app.app:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Iniciar frontend
echo "Iniciando frontend..."
cd "$PROJECT_DIR/frontend"
npm run dev &
FRONTEND_PID=$!

# Función para manejar cierre
function cleanup {
    echo "Deteniendo servicios..."
    kill $BACKEND_PID
    kill $FRONTEND_PID
    exit 0
}

# Capturar señales de cierre
trap cleanup SIGINT SIGTERM

echo "Servicios iniciados. Presiona Ctrl+C para detener."
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:3000"

# Mantener script en ejecución
wait
EOF
    
    chmod +x "$PROJECT_DIR/start_dev.sh"
    echo -e "${GREEN}Script start_dev.sh creado. Ejecútalo para iniciar el entorno de desarrollo.${NC}"
fi

# 6. Mensaje final
echo -e "\n${GREEN}Configuración completada exitosamente.${NC}"
echo -e "Para iniciar el entorno de desarrollo: ${YELLOW}./start_dev.sh${NC}"
echo -e "Para activar el entorno virtual manualmente: ${YELLOW}source backend/venv/bin/activate${NC}"
echo -e "Para iniciar el backend manualmente: ${YELLOW}cd backend && uvicorn app.app:app --reload${NC}"
echo -e "Para iniciar el frontend manualmente: ${YELLOW}cd frontend && npm run dev${NC}"

if [ "$ENV_TYPE" = "production" ]; then
    echo -e "\nConsulta ${YELLOW}docs/despliegue_sin_docker.md${NC} para las instrucciones completas de despliegue en producción."
fi