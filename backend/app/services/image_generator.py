# app/services/image_generator.py
import os
import logging
from datetime import datetime
from typing import Optional, Dict, Tuple
from PIL import Image, ImageDraw, ImageFont

from app.core.config import settings
from app.db.models import Template, Post
from app.utils.image_utils import (
    get_font, overlay_text, save_image, calculate_text_position, get_image_url
)

logger = logging.getLogger(__name__)

class ImageGenerator:
    """Servicio para generar imágenes para publicaciones de Instagram."""
    
    def __init__(self):
        """Inicializar el generador de imágenes."""
        self.templates_dir = settings.TEMPLATES_DIR
        self.generated_dir = settings.GENERATED_DIR
        
        # Asegurar que los directorios existan
        os.makedirs(self.templates_dir, exist_ok=True)
        os.makedirs(self.generated_dir, exist_ok=True)
    
    def generate_post_image(self, post: Post) -> Tuple[str, str]:
        """
        Generar una imagen para una publicación de Instagram.
        
        Args:
            post: Objeto Post con los datos de la publicación
            
        Returns:
            Tupla con la ruta de la imagen generada y la URL para el frontend
        """
        try:
            template = post.template
            
            # Cargar imagen de plantilla
            if template.template_image:
                # Si la plantilla tiene una imagen almacenada en la base de datos
                import io
                template_image = Image.open(io.BytesIO(template.template_image))
            else:
                # Buscar imagen en el sistema de archivos
                template_path = os.path.join(self.templates_dir, f"template_{template.template_id}.png")
                if os.path.exists(template_path):
                    template_image = Image.open(template_path)
                else:
                    # Crear una imagen en blanco si no hay plantilla
                    logger.warning(f"No se encontró imagen para la plantilla {template.template_id}")
                    template_image = Image.new('RGB', (1080, 1080), color=template.background_color or "#FFFFFF")
            
            # Crear una copia para no modificar la original
            img = template_image.copy()
            
            # Dibujar título del puesto
            title_font_size = 50 + (post.position_priority * 5)  # Aumentar tamaño según prioridad
            title_position = calculate_text_position(
                img, post.job_title.upper(), get_font(size=title_font_size), position="top"
            )
            title_position = (title_position[0], title_position[1] + 150)  # Ajustar posición vertical
            
            img = overlay_text(
                img,
                post.job_title.upper(),
                title_position,
                font_size=title_font_size,
                color="#FFFFFF",
                outline_color="#000000",
                outline_width=2
            )
            
            # Dibujar ubicación
            location_font_size = 30 + (post.location_priority * 2)
            location_position = calculate_text_position(
                img, f"📍 {post.location}", get_font(size=location_font_size), position="center"
            )
            location_position = (location_position[0], location_position[1] - 100)  # Ajustar posición
            
            img = overlay_text(
                img,
                f"📍 {post.location}",
                location_position,
                font_size=location_font_size,
                color=template.text_color or "#000000"
            )
            
            # Dibujar email
            email_font_size = 25 + (post.email_priority * 2)
            email_text = f"Dejanos tu CV: {post.email}"
            email_position = calculate_text_position(
                img, email_text, get_font(size=email_font_size), position="center"
            )
            email_position = (email_position[0], email_position[1] + 50)  # Ajustar posición
            
            img = overlay_text(
                img,
                email_text,
                email_position,
                font_size=email_font_size,
                color=template.text_color or "#000000"
            )
            
            # Dibujar requisitos (si existen)
            if post.requirements:
                req_font_size = 20 + (post.requirements_priority * 1)
                req_lines = post.requirements.split('\n')
                
                # Limitar a 5 líneas para que quepa en la imagen
                if len(req_lines) > 5:
                    req_lines = req_lines[:4] + ['...']
                
                req_y_start = email_position[1] + 100  # Comenzar debajo del email
                
                # Título de requisitos
                img = overlay_text(
                    img,
                    "Requisitos:",
                    (100, req_y_start),
                    font_size=req_font_size + 5,
                    color="#000000",
                    outline_color="#FFFFFF",
                    outline_width=1
                )
                
                # Cada línea de requisitos
                for i, line in enumerate(req_lines):
                    img = overlay_text(
                        img,
                        f"• {line.strip()}",
                        (120, req_y_start + 40 + (i * (req_font_size + 10))),
                        font_size=req_font_size,
                        color=template.text_color or "#000000"
                    )
            
            # Añadir pie de página (si existe)
            if template.footer_text:
                footer_position = calculate_text_position(
                    img, template.footer_text, get_font(size=25), position="bottom"
                )
                
                img = overlay_text(
                    img,
                    template.footer_text,
                    footer_position,
                    font_size=25,
                    color=template.text_color or "#000000"
                )
            
            # Generar nombre único para la imagen
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            image_filename = f"post_{post.post_id}_{timestamp}.png"
            image_path = os.path.join(self.generated_dir, image_filename)
            
            # Guardar imagen
            save_image(img, image_path)
            
            # Calcular URL para el frontend
            image_url = get_image_url(image_path)
            
            # Guardar imagen generada en el post (si estuviera implementado)
            # post.generated_image = open(image_path, 'rb').read()
            
            return image_path, image_url
            
        except Exception as e:
            logger.error(f"Error al generar imagen: {str(e)}")
            raise ValueError(f"No se pudo generar la imagen: {str(e)}")
    
    def generate_preview(
        self,
        template_id: int,
        job_title: str,
        location: str,
        email: str,
        requirements: Optional[str] = None,
        position_priority: int = 5,
        location_priority: int = 3,
        email_priority: int = 3,
        requirements_priority: int = 4
    ) -> Tuple[str, str]:
        """
        Generar una vista previa de imagen para un formulario.
        
        Args:
            template_id: ID de la plantilla
            job_title: Título del puesto
            location: Ubicación
            email: Email de contacto
            requirements: Requisitos (opcional)
            position_priority: Prioridad del título
            location_priority: Prioridad de la ubicación
            email_priority: Prioridad del email
            requirements_priority: Prioridad de los requisitos
            
        Returns:
            Tupla con la ruta de la imagen generada y la URL para el frontend
        """
        # Crear un objeto Post temporal para usar la misma lógica
        from app.db.database import SessionLocal
        
        db = SessionLocal()
        try:
            template = db.query(Template).filter(Template.template_id == template_id).first()
            
            if not template:
                raise ValueError(f"No se encontró la plantilla con ID {template_id}")
            
            # Crear un post temporal
            temp_post = Post(
                post_id=0,  # ID temporal
                user_id=0,  # ID temporal
                template_id=template_id,
                job_title=job_title,
                location=location,
                email=email,
                requirements=requirements,
                position_priority=position_priority,
                location_priority=location_priority,
                email_priority=email_priority,
                requirements_priority=requirements_priority,
                template=template
            )
            
            # Generar la imagen
            image_path, image_url = self.generate_post_image(temp_post)
            
            return image_path, image_url
            
        finally:
            db.close()