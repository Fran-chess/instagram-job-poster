# app/services/instagram_publisher.py
import os
import time
import logging
from typing import Dict, Any, Optional, Tuple
import requests
from datetime import datetime
from instagrapi import Client
from instagrapi.exceptions import (
    LoginRequired, ClientError, ClientLoginRequired,
    ClientCookieExpiredError, ClientConnectionError
)

from app.core.config import settings
from app.db.models import Post, PostLog

logger = logging.getLogger(__name__)

class InstagramPublisher:
    """Servicio para publicar en Instagram usando instagrapi."""
    
    def __init__(self):
        """Inicializar el cliente de Instagram."""
        self.client = Client()
        self.logged_in = False
        
        # Intentar cargar sesión guardada
        session_file = "instagram_session.json"
        if os.path.exists(session_file):
            try:
                self.client.load_settings(session_file)
                self.client.get_timeline_feed()  # Verificar que la sesión es válida
                self.logged_in = True
                logger.info("Sesión de Instagram cargada correctamente")
            except (ClientCookieExpiredError, ClientLoginRequired):
                logger.info("Sesión de Instagram expirada, iniciando sesión nuevamente")
                self._login()
        else:
            self._login()
    
    def _login(self) -> bool:
        """
        Iniciar sesión en Instagram.
        
        Returns:
            True si el inicio de sesión fue exitoso, False en caso contrario
        """
        try:
            self.logged_in = self.client.login(
                settings.INSTAGRAM_USERNAME,
                settings.INSTAGRAM_PASSWORD
            )
            
            if self.logged_in:
                # Guardar sesión para futuros usos
                self.client.dump_settings("instagram_session.json")
                logger.info("Inicio de sesión en Instagram exitoso")
            else:
                logger.error("Error al iniciar sesión en Instagram")
                
            return self.logged_in
            
        except (ClientLoginRequired, ClientCookieExpiredError) as e:
            logger.error(f"Error de autenticación en Instagram: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Error inesperado al iniciar sesión en Instagram: {str(e)}")
            return False
    
    def _ensure_login(self) -> bool:
        """
        Asegurar que el cliente está autenticado.
        
        Returns:
            True si el cliente está autenticado, False en caso contrario
        """
        if not self.logged_in:
            return self._login()
            
        try:
            # Verificar si la sesión es válida
            self.client.get_timeline_feed()
            return True
        except (ClientLoginRequired, ClientCookieExpiredError):
            logger.info("Sesión de Instagram expirada, iniciando sesión nuevamente")
            return self._login()
    
    def publish_post(self, post: Post, db_session) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Publicar una imagen en el feed de Instagram.
        
        Args:
            post: Objeto Post con los datos de la publicación
            db_session: Sesión de base de datos para registrar el resultado
            
        Returns:
            Tupla (éxito, id_publicación, mensaje_error)
        """
        if not self._ensure_login():
            error_msg = "No se pudo iniciar sesión en Instagram"
            self._log_action(post, "publish", "error", error_msg, db_session)
            return False, None, error_msg
        
        try:
            # Verificar si hay una imagen generada
            if not post.generated_image and not os.path.exists(f"{settings.GENERATED_DIR}/post_{post.post_id}_*.png"):
                # Generar la imagen si no existe
                from app.services.image_generator import ImageGenerator
                generator = ImageGenerator()
                image_path, _ = generator.generate_post_image(post)
            else:
                # Usar la imagen existente
                import glob
                image_files = glob.glob(f"{settings.GENERATED_DIR}/post_{post.post_id}_*.png")
                if image_files:
                    image_path = image_files[0]
                else:
                    error_msg = "No se encontró la imagen generada"
                    self._log_action(post, "publish", "error", error_msg, db_session)
                    return False, None, error_msg
            
            # Preparar la leyenda
            caption = self._generate_caption(post)
            
            # Publicar en Instagram
            result = self.client.photo_upload(
                image_path,
                caption=caption
            )
            
            if result:
                instagram_post_id = result.id
                
                # Actualizar post en la base de datos
                post.instagram_post_id = instagram_post_id
                post.status = "published"
                post.published_at = datetime.utcnow()
                db_session.commit()
                
                # Registrar acción
                self._log_action(post, "publish", "success", None, db_session)
                
                logger.info(f"Publicación exitosa en Instagram: {instagram_post_id}")
                return True, instagram_post_id, None
            else:
                error_msg = "Error desconocido al publicar en Instagram"
                self._log_action(post, "publish", "error", error_msg, db_session)
                return False, None, error_msg
                
        except Exception as e:
            error_msg = f"Error al publicar en Instagram: {str(e)}"
            logger.error(error_msg)
            self._log_action(post, "publish", "error", error_msg, db_session)
            return False, None, error_msg
    
    def publish_story(self, post: Post, db_session) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Publicar una imagen como historia de Instagram.
        
        Args:
            post: Objeto Post con los datos de la publicación
            db_session: Sesión de base de datos para registrar el resultado
            
        Returns:
            Tupla (éxito, id_historia, mensaje_error)
        """
        if not self._ensure_login():
            error_msg = "No se pudo iniciar sesión en Instagram"
            self._log_action(post, "publish_story", "error", error_msg, db_session)
            return False, None, error_msg
        
        try:
            # Usar la misma imagen que para el post
            import glob
            image_files = glob.glob(f"{settings.GENERATED_DIR}/post_{post.post_id}_*.png")
            if image_files:
                image_path = image_files[0]
            else:
                error_msg = "No se encontró la imagen generada"
                self._log_action(post, "publish_story", "error", error_msg, db_session)
                return False, None, error_msg
            
            # Publicar en Instagram Stories
            result = self.client.photo_upload_to_story(
                image_path
            )
            
            if result:
                story_id = result.id
                
                # Registrar acción
                self._log_action(post, "publish_story", "success", None, db_session)
                
                logger.info(f"Historia publicada exitosamente en Instagram: {story_id}")
                return True, story_id, None
            else:
                error_msg = "Error desconocido al publicar historia en Instagram"
                self._log_action(post, "publish_story", "error", error_msg, db_session)
                return False, None, error_msg
                
        except Exception as e:
            error_msg = f"Error al publicar historia en Instagram: {str(e)}"
            logger.error(error_msg)
            self._log_action(post, "publish_story", "error", error_msg, db_session)
            return False, None, error_msg
    
    def _generate_caption(self, post: Post) -> str:
        """
        Generar la leyenda para una publicación de Instagram.
        
        Args:
            post: Objeto Post con los datos de la publicación
            
        Returns:
            Leyenda formateada
        """
        hashtags = [
            "#Empleo", 
            "#Trabajo", 
            f"#{post.job_title.replace(' ', '')}", 
            f"#{post.location.replace(' ', '')}", 
            "#Oportunidad", 
            "#BúsquedaLaboral"
        ]
        
        caption = f"📢 BÚSQUEDA LABORAL 📢\n\n"
        caption += f"🔷 Puesto: {post.job_title}\n"
        caption += f"📍 Ubicación: {post.location}\n"
        
        if post.requirements:
            caption += f"\n📋 Requisitos:\n"
            for req in post.requirements.split("\n"):
                if req.strip():
                    caption += f"✓ {req.strip()}\n"
        
        caption += f"\n📧 CV a: {post.email}\n\n"
        caption += " ".join(hashtags)
        
        return caption
    
    def _log_action(self, post: Post, action: str, status: str, error_message: Optional[str], db_session) -> None:
        """
        Registrar una acción en la base de datos.
        
        Args:
            post: Objeto Post relacionado
            action: Tipo de acción ('publish', 'publish_story', etc.)
            status: Estado ('success', 'error')
            error_message: Mensaje de error (solo si status es 'error')
            db_session: Sesión de base de datos
        """
        log = PostLog(
            post_id=post.post_id,
            action=action,
            status=status,
            error_message=error_message,
            timestamp=datetime.utcnow()
        )
        
        db_session.add(log)
        db_session.commit()