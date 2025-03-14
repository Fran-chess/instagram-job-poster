# scripts/init_db.py
import logging
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import get_password_hash
from app.db.database import Base
from app.db.models import User, Template, Post

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db(db: Session) -> None:
    """
    Inicializar la base de datos con datos de ejemplo.
    """
    # Crear usuario administrador
    user = db.query(User).filter(User.username == "admin").first()
    if not user:
        logger.info("Creando usuario admin...")
        admin_user = User(
            username="admin",
            email="admin@darsalud.com",
            full_name="Administrador",
            hashed_password=get_password_hash("admin123"),
            is_active=True
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
    
    # Crear plantillas de ejemplo
    template_count = db.query(Template).count()
    if template_count == 0:
        logger.info("Creando plantillas de ejemplo...")
        templates = [
            Template(
                name="Estándar",
                description="Plantilla estándar para ofertas laborales",
                background_color="#FFFFFF",
                text_color="#000000",
                footer_text="DarSalud - Búsqueda Laboral",
                is_active=True
            ),
            Template(
                name="Médicos",
                description="Plantilla para búsqueda de médicos",
                background_color="#E6F7FF",
                text_color="#003366",
                footer_text="DarSalud - Oportunidades Médicas",
                is_active=True
            ),
            Template(
                name="Enfermería",
                description="Plantilla para búsqueda de personal de enfermería",
                background_color="#E6FFE6",
                text_color="#003300",
                footer_text="DarSalud - Oportunidades en Enfermería",
                is_active=True
            )
        ]
        
        for template in templates:
            db.add(template)
        
        db.commit()
        
        # Crear imágenes de plantilla
        os.makedirs(settings.TEMPLATES_DIR, exist_ok=True)
        
        # Aquí idealmente crearíamos imágenes para cada plantilla
        # Pero como no tenemos capacidades de dibujo, solo creamos placeholders
        import numpy as np
        from PIL import Image, ImageDraw, ImageFont
        
        for i, color in enumerate([
            "#FFFFFF", "#E6F7FF", "#E6FFE6"
        ]):
            # Crear imagen de 1080x1080 (tamaño ideal para Instagram)
            img = Image.new('RGB', (1080, 1080), color=color)
            draw = ImageDraw.Draw(img)
            
            # Dibujar rectángulo para el encabezado
            draw.rectangle(
                [(0, 0), (1080, 150)],
                fill="#0066cc"
            )
            
            # Intentar cargar una fuente
            try:
                font = ImageFont.truetype("arial.ttf", 40)
            except:
                font = ImageFont.load_default()
            
            # Añadir texto de ejemplo
            draw.text(
                (540, 75),
                "Buscamos Profesionales",
                fill="white",
                font=font,
                anchor="mm"
            )
            
            # Guardar la imagen
            template_path = os.path.join(settings.TEMPLATES_DIR, f"template_{i+1}.png")
            img.save(template_path)
            
            logger.info(f"Creada imagen para plantilla {i+1}")

def main() -> None:
    """
    Punto de entrada principal.
    """
    logger.info("Creando las tablas iniciales...")
    
    from app.db.database import engine
    Base.metadata.create_all(bind=engine)
    
    logger.info("Tablas creadas.")
    
    db = Session(engine)
    init_db(db)
    db.close()
    
    logger.info("Base de datos inicializada exitosamente.")

if __name__ == "__main__":
    main()