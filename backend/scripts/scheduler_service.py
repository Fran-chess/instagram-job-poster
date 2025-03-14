# scripts/scheduler_service.py
import time
import logging
import signal
import sys
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("scheduler.log")
    ]
)

logger = logging.getLogger(__name__)

def handle_exit(signum, frame):
    """
    Manejador de señales para salir limpiamente.
    """
    logger.info("Recibida señal de salida. Deteniendo programador...")
    if 'scheduler' in globals():
        scheduler.shutdown()
    sys.exit(0)

def main():
    """
    Función principal para iniciar el servicio de programación.
    """
    logger.info("Iniciando servicio de programación de Instagram Job Poster...")
    
    # Registrar manejadores de señales
    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)
    
    # Iniciar programador
    from app.services.scheduler import PostScheduler
    global scheduler
    scheduler = PostScheduler()
    
    logger.info("Programador de tareas iniciado. Esperando trabajos programados...")
    
    # Mantener el proceso en ejecución
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Interrumpido por el usuario. Deteniendo programador...")
        scheduler.shutdown()
        sys.exit(0)

if __name__ == "__main__":
    main()