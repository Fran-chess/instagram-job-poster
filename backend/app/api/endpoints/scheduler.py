# app/api/endpoints/scheduler.py
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.api.deps import get_db, get_current_user
from app.db.models import User, Post, ScheduleSettings
from app.services.scheduler import PostScheduler
from app.utils.image_utils import get_image_url

router = APIRouter(prefix="/scheduler", tags=["scheduler"])

@router.get("/upcoming")
def get_upcoming_posts(
    hours: int = 24,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Obtener posts programados para las próximas X horas.
    """
    # Usar el servicio de programación
    scheduler = PostScheduler()
    posts = scheduler.get_pending_posts(hours)
    
    # Agregar URL de imagen para la respuesta
    for post in posts:
        # Buscar la imagen generada (si existe)
        import glob, os
        
        image_files = glob.glob(f"media/generated/post_{post.post_id}_*.png")
        if image_files:
            post.image_url = get_image_url(image_files[0])
        else:
            post.image_url = None
    
    # Formatear la respuesta
    result = []
    for post in posts:
        result.append({
            "post_id": post.post_id,
            "job_title": post.job_title,
            "location": post.location,
            "email": post.email,
            "status": post.status,
            "scheduled_for": post.scheduled_for,
            "image_url": getattr(post, "image_url", None)
        })
    
    return result

@router.get("/calendar")
def get_calendar(
    start_date: datetime,
    end_date: datetime,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Obtener posts programados en un rango de fechas.
    """
    # Verificar que el rango sea válido
    if end_date < start_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La fecha final debe ser posterior a la fecha inicial"
        )
    
    # Limitar el rango a 90 días para evitar consultas muy pesadas
    if (end_date - start_date).days > 90:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El rango máximo permitido es de 90 días"
        )
    
    # Obtener posts programados en el rango
    posts = db.query(Post).filter(
        Post.status == "scheduled",
        Post.scheduled_for >= start_date,
        Post.scheduled_for <= end_date
    ).all()
    
    # Formatear la respuesta para calendario
    calendar_events = []
    for post in posts:
        calendar_events.append({
            "id": post.post_id,
            "title": post.job_title,
            "start": post.scheduled_for.isoformat(),
            "end": (post.scheduled_for + timedelta(minutes=30)).isoformat(),
            "location": post.location,
            "status": post.status
        })
    
    return calendar_events

@router.get("/settings/{post_id}")
def get_schedule_settings(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Obtener configuración de programación para un post.
    """
    # Verificar que el post existe
    post = db.query(Post).filter(Post.post_id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Publicación no encontrada"
        )
    
    # Obtener configuración de programación
    schedule = db.query(ScheduleSettings).filter(
        ScheduleSettings.post_id == post_id
    ).first()
    
    if not schedule:
        return {
            "post_id": post_id,
            "has_schedule": False,
            "scheduled_time": post.scheduled_for,
            "frequency": "once",
            "is_active": False
        }
    
    return {
        "post_id": post_id,
        "has_schedule": True,
        "scheduled_time": schedule.scheduled_time,
        "frequency": schedule.frequency,
        "recurrence_pattern": schedule.recurrence_pattern,
        "end_date": schedule.end_date,
        "is_active": schedule.is_active
    }

@router.put("/settings/{post_id}")
def update_schedule_settings(
    post_id: int,
    scheduled_time: datetime,
    frequency: str = "once",
    recurrence_pattern: str = None,
    end_date: datetime = None,
    is_active: bool = True,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Actualizar configuración de programación para un post.
    """
    # Verificar que el post existe
    post = db.query(Post).filter(Post.post_id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Publicación no encontrada"
        )
    
    # Obtener o crear configuración de programación
    schedule = db.query(ScheduleSettings).filter(
        ScheduleSettings.post_id == post_id
    ).first()
    
    if not schedule:
        schedule = ScheduleSettings(
            post_id=post_id,
            scheduled_time=scheduled_time,
            frequency=frequency,
            recurrence_pattern=recurrence_pattern,
            end_date=end_date,
            is_active=is_active
        )
        db.add(schedule)
    else:
        schedule.scheduled_time = scheduled_time
        schedule.frequency = frequency
        schedule.recurrence_pattern = recurrence_pattern
        schedule.end_date = end_date
        schedule.is_active = is_active
    
    # Actualizar estado del post
    if is_active:
        post.status = "scheduled"
        post.scheduled_for = scheduled_time
    else:
        post.status = "draft"
        post.scheduled_for = None
    
    db.commit()
    
    # Actualizar programación
    scheduler = PostScheduler()
    if is_active:
        scheduler.schedule_post(post_id, scheduled_time, frequency)
    else:
        scheduler.cancel_scheduled_post(post_id)
    
    return {
        "success": True,
        "message": "Configuración de programación actualizada",
        "post_id": post_id,
        "scheduled_time": scheduled_time
    }