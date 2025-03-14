# app/services/scheduler.py
import logging
from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy import and_
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor

from app.core.config import settings
from app.db.database import SessionLocal, engine
from app.db.models import Post, ScheduleSettings
from app.services.instagram_publisher import InstagramPublisher

logger = logging.getLogger(__name__)

class PostScheduler:
    """Servicio para programar publicaciones en Instagram."""
    
    _instance = None
    
    def __new__(cls):
        """Implementar patrón Singleton."""
        if cls._instance is None:
            cls._instance = super(PostScheduler, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Inicializar el programador de tareas."""
        if not self._initialized:
            # Configurar jobstore para guardar tareas en la base de datos
            jobstores = {
                'default': SQLAlchemyJobStore(url=str(engine.url))
            }
            
            # Configurar executors
            executors = {
                'default': ThreadPoolExecutor(20)
            }
            
            # Configurar programador
            self.scheduler = BackgroundScheduler(
                jobstores=jobstores,
                executors=executors,
                timezone='UTC'
            )
            
            # Iniciar el programador
            self.scheduler.start()
            
            logger.info("Programador de tareas iniciado")
            self._initialized = True
    
    def schedule_post(self, post_id: int, scheduled_time: datetime, frequency: str = "once") -> bool:
        """
        Programar la publicación de un post.
        
        Args:
            post_id: ID del post a programar
            scheduled_time: Fecha y hora programada
            frequency: Frecuencia ('once', 'daily', 'weekly', 'monthly')
            
        Returns:
            True si la programación fue exitosa, False en caso contrario
        """
        try:
            db = SessionLocal()
            try:
                # Obtener el post
                post = db.query(Post).filter(Post.post_id == post_id).first()
                
                if not post:
                    logger.error(f"No se encontró el post con ID {post_id}")
                    return False
                
                # Actualizar estado del post
                post.status = "scheduled"
                post.scheduled_for = scheduled_time
                
                # Crear o actualizar configuración de programación
                schedule = db.query(ScheduleSettings).filter(
                    ScheduleSettings.post_id == post_id
                ).first()
                
                if not schedule:
                    schedule = ScheduleSettings(
                        post_id=post_id,
                        scheduled_time=scheduled_time,
                        frequency=frequency,
                        is_active=True
                    )
                    db.add(schedule)
                else:
                    schedule.scheduled_time = scheduled_time
                    schedule.frequency = frequency
                    schedule.is_active = True
                
                # Guardar cambios
                db.commit()
                
                # Programar la tarea
                job_id = f"post_{post_id}"
                
                # Eliminar job existente si lo hay
                if self.scheduler.get_job(job_id):
                    self.scheduler.remove_job(job_id)
                
                # Programar según frecuencia
                if frequency == "once":
                    self.scheduler.add_job(
                        self._publish_post,
                        'date',
                        run_date=scheduled_time,
                        id=job_id,
                        args=[post_id]
                    )
                elif frequency == "daily":
                    self.scheduler.add_job(
                        self._publish_post,
                        'interval',
                        days=1,
                        start_date=scheduled_time,
                        id=job_id,
                        args=[post_id]
                    )
                elif frequency == "weekly":
                    self.scheduler.add_job(
                        self._publish_post,
                        'interval',
                        weeks=1,
                        start_date=scheduled_time,
                        id=job_id,
                        args=[post_id]
                    )
                elif frequency == "monthly":
                    self.scheduler.add_job(
                        self._publish_post,
                        'interval',
                        months=1,
                        start_date=scheduled_time,
                        id=job_id,
                        args=[post_id]
                    )
                else:
                    logger.error(f"Frecuencia no válida: {frequency}")
                    return False
                
                logger.info(f"Post {post_id} programado para {scheduled_time}")
                return True
                
            finally:
                db.close()
                
        except Exception as e:
            logger.error(f"Error al programar post: {str(e)}")
            return False
    
    def cancel_scheduled_post(self, post_id: int) -> bool:
        """
        Cancelar una publicación programada.
        
        Args:
            post_id: ID del post a cancelar
            
        Returns:
            True si la cancelación fue exitosa, False en caso contrario
        """
        try:
            db = SessionLocal()
            try:
                # Obtener el post
                post = db.query(Post).filter(Post.post_id == post_id).first()
                
                if not post:
                    logger.error(f"No se encontró el post con ID {post_id}")
                    return False
                
                # Desactivar programación
                schedule = db.query(ScheduleSettings).filter(
                    ScheduleSettings.post_id == post_id
                ).first()
                
                if schedule:
                    schedule.is_active = False
                
                # Actualizar estado del post
                post.status = "draft"
                post.scheduled_for = None
                
                # Guardar cambios
                db.commit()
                
                # Eliminar job
                job_id = f"post_{post_id}"
                if self.scheduler.get_job(job_id):
                    self.scheduler.remove_job(job_id)
                    logger.info(f"Programación cancelada para post {post_id}")
                    return True
                else:
                    logger.warning(f"No se encontró job programado para post {post_id}")
                    return True  # Consideramos exitoso ya que no hay job que cancelar
                
            finally:
                db.close()
                
        except Exception as e:
            logger.error(f"Error al cancelar programación: {str(e)}")
            return False
    
    def get_pending_posts(self, hours: int = 24) -> List[Post]:
        """
        Obtener posts programados para las próximas X horas.
        
        Args:
            hours: Número de horas a considerar
            
        Returns:
            Lista de posts programados
        """
        db = SessionLocal()
        try:
            now = datetime.utcnow()
            end_time = now + timedelta(hours=hours)
            
            posts = db.query(Post).filter(
                and_(
                    Post.status == "scheduled",
                    Post.scheduled_for >= now,
                    Post.scheduled_for <= end_time
                )
            ).all()
            
            return posts
            
        finally:
            db.close()
    
    def _publish_post(self, post_id: int) -> None:
        """
        Publicar un post programado.
        
        Args:
            post_id: ID del post a publicar
        """
        db = SessionLocal()
        try:
            # Obtener el post
            post = db.query(Post).filter(Post.post_id == post_id).first()
            
            if not post:
                logger.error(f"No se encontró el post con ID {post_id}")
                return
            
            # Verificar si está activo y programado
            schedule = db.query(ScheduleSettings).filter(
                ScheduleSettings.post_id == post_id
            ).first()
            
            if not schedule or not schedule.is_active:
                logger.info(f"Programación inactiva para post {post_id}")
                return
            
            # Publicar en Instagram
            publisher = InstagramPublisher()
            success, post_id, error = publisher.publish_post(post, db)
            
            if success:
                logger.info(f"Post {post_id} publicado exitosamente")
                
                # Si la frecuencia es "once", desactivar la programación
                if schedule.frequency == "once":
                    schedule.is_active = False
                    db.commit()
            else:
                logger.error(f"Error al publicar post {post_id}: {error}")
                
                # Actualizar estado del post
                post.status = "failed"
                db.commit()
            
        except Exception as e:
            logger.error(f"Error en la publicación programada: {str(e)}")
            
        finally:
            db.close()
    
    def shutdown(self):
        """Detener el programador de tareas."""
        if hasattr(self, 'scheduler'):
            self.scheduler.shutdown()
            logger.info("Programador de tareas detenido")