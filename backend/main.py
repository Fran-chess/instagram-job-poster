# main.py en la raíz
import uvicorn
import logging
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("app.log")
    ]
)

logger = logging.getLogger(__name__)

def main():
    """
    Función principal para iniciar la aplicación.
    """
    logger.info("Iniciando aplicación Instagram Job Poster...")
    
    # Asegurarse de que existan los directorios necesarios
    os.makedirs("media", exist_ok=True)
    os.makedirs("media/templates", exist_ok=True)
    os.makedirs("media/generated", exist_ok=True)
    
    # Iniciar programador de tareas (solo para servidor de producción)
    # En desarrollo, esto puede causar problemas con el reinicio automático
    if os.getenv("ENVIRONMENT", "development") == "production":
        from app.services.scheduler import PostScheduler
        scheduler = PostScheduler()
        logger.info("Programador de tareas iniciado")
    
    # Iniciar servidor web
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=os.getenv("ENVIRONMENT", "development") == "development"
    )

if __name__ == "__main__":
    main()