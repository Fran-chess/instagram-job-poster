# app/api/endpoints/posts.py
from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Form, File, UploadFile, Query
from sqlalchemy.orm import Session
from datetime import datetime

from app.api.deps import get_db, get_current_user
from app.db.models import Post, User
from app.schemas.post import (
    PostCreate, PostUpdate, PostResponse, PostInDB, 
    PostSchedule, PostPublishNow
)
from app.services.image_generator import ImageGenerator
from app.services.instagram_publisher import InstagramPublisher

router = APIRouter(prefix="/posts", tags=["posts"])

@router.get("/", response_model=List[PostResponse])
def get_posts(
    skip: int = 0, 
    limit: int = 100,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Obtener todas las publicaciones.
    """
    # Construir query base
    query = db.query(Post)
    
    # Filtrar por estado si se especifica
    if status:
        query = query.filter(Post.status == status)
    
    # Obtener posts con paginación
    posts = query.offset(skip).limit(limit).all()
    
    # Agregar URL de imagen para la respuesta
    for post in posts:
        # Buscar la imagen generada (si existe)
        import glob, os
        from app.utils.image_utils import get_image_url
        
        image_files = glob.glob(f"media/generated/post_{post.post_id}_*.png")
        if image_files:
            post.image_url = get_image_url(image_files[0])
    
    return posts

@router.post("/", response_model=PostResponse)
def create_post(
    post_data: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Crear una nueva publicación.
    """
    # Crear post en la base de datos
    db_post = Post(
        user_id=current_user.user_id,
        template_id=post_data.template_id,
        job_title=post_data.job_title,
        location=post_data.location,
        email=post_data.email,
        requirements=post_data.requirements,
        position_priority=post_data.position_priority,
        location_priority=post_data.location_priority,
        email_priority=post_data.email_priority,
        requirements_priority=post_data.requirements_priority,
        status="draft"
    )
    
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    
    # Generar imagen para la publicación
    image_generator = ImageGenerator()
    try:
        image_path, image_url = image_generator.generate_post_image(db_post)
        
        # Agregar URL de la imagen a la respuesta
        setattr(db_post, "image_url", image_url)
        
        return db_post
    except Exception as e:
        # Si hay error al generar la imagen, aún devolvemos el post creado
        db_post.image_url = None
        return db_post

@router.get("/preview", response_model=dict)
def preview_post(
    template_id: int,
    job_title: str,
    location: str,
    email: str,
    requirements: Optional[str] = None,
    position_priority: int = 5,
    location_priority: int = 3,
    email_priority: int = 3,
    requirements_priority: int = 4,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Generar vista previa de una publicación sin guardarla.
    """
    # Generar imagen para la vista previa
    image_generator = ImageGenerator()
    try:
        _, image_url = image_generator.generate_preview(
            template_id=template_id,
            job_title=job_title,
            location=location,
            email=email,
            requirements=requirements,
            position_priority=position_priority,
            location_priority=location_priority,
            email_priority=email_priority,
            requirements_priority=requirements_priority
        )
        
        return {
            "image_url": image_url,
            "job_title": job_title,
            "location": location,
            "email": email,
            "requirements": requirements
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al generar vista previa: {str(e)}"
        )

@router.get("/{post_id}", response_model=PostResponse)
def get_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Obtener una publicación por ID.
    """
    post = db.query(Post).filter(Post.post_id == post_id).first()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Publicación no encontrada"
        )
    
    # Agregar URL de imagen para la respuesta
    import glob
    from app.utils.image_utils import get_image_url
    
    image_files = glob.glob(f"media/generated/post_{post.post_id}_*.png")
    if image_files:
        post.image_url = get_image_url(image_files[0])
    else:
        post.image_url = None
    
    return post

@router.put("/{post_id}", response_model=PostResponse)
def update_post(
    post_id: int,
    post_data: PostUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Actualizar una publicación.
    """
    post = db.query(Post).filter(Post.post_id == post_id).first()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Publicación no encontrada"
        )
    
    # Actualizar solo los campos proporcionados
    update_data = post_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(post, key, value)
    
    db.commit()
    db.refresh(post)
    
    # Volver a generar la imagen si se modificaron datos relevantes
    relevant_fields = [
        "job_title", "location", "email", "requirements", 
        "position_priority", "location_priority", "email_priority", 
        "requirements_priority", "template_id"
    ]
    
    if any(field in update_data for field in relevant_fields):
        image_generator = ImageGenerator()
        try:
            _, image_url = image_generator.generate_post_image(post)
            setattr(post, "image_url", image_url)
        except Exception as e:
            # Si hay error al generar la imagen, continuamos
            post.image_url = None
    else:
        # Mantener la imagen existente
        import glob
        from app.utils.image_utils import get_image_url
        
        image_files = glob.glob(f"media/generated/post_{post.post_id}_*.png")
        if image_files:
            post.image_url = get_image_url(image_files[0])
        else:
            post.image_url = None
    
    return post

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Eliminar una publicación.
    """
    post = db.query(Post).filter(Post.post_id == post_id).first()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Publicación no encontrada"
        )
    
    # Cancelar programación si está programada
    if post.status == "scheduled":
        from app.services.scheduler import PostScheduler
        scheduler = PostScheduler()
        scheduler.cancel_scheduled_post(post_id)
    
    # Eliminar post
    db.delete(post)
    db.commit()
    
    # Eliminar imágenes asociadas
    import glob, os
    for image_file in glob.glob(f"media/generated/post_{post_id}_*.png"):
        try:
            os.remove(image_file)
        except:
            pass
    
    return None

@router.post("/{post_id}/publish", response_model=dict)
def publish_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Publicar inmediatamente un post en Instagram.
    """
    post = db.query(Post).filter(Post.post_id == post_id).first()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Publicación no encontrada"
        )
    
    # Publicar en Instagram
    publisher = InstagramPublisher()
    success, instagram_post_id, error = publisher.publish_post(post, db)
    
    if success:
        # Publicar también en stories
        story_success, story_id, story_error = publisher.publish_story(post, db)
        
        return {
            "success": True,
            "message": "Publicación realizada con éxito",
            "instagram_post_id": instagram_post_id,
            "story_published": story_success,
            "story_id": story_id
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al publicar: {error}"
        )

@router.post("/{post_id}/schedule", response_model=dict)
def schedule_post(
    post_id: int,
    schedule_data: PostSchedule,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Programar la publicación de un post.
    """
    post = db.query(Post).filter(Post.post_id == post_id).first()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Publicación no encontrada"
        )
    
    # Programar publicación
    from app.services.scheduler import PostScheduler
    scheduler = PostScheduler()
    
    success = scheduler.schedule_post(
        post_id=post_id,
        scheduled_time=schedule_data.scheduled_for,
        frequency=schedule_data.frequency
    )
    
    if success:
        return {
            "success": True,
            "message": "Publicación programada con éxito",
            "scheduled_for": schedule_data.scheduled_for
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al programar la publicación"
        )

@router.post("/{post_id}/cancel-schedule", response_model=dict)
def cancel_schedule(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Cancelar la programación de un post.
    """
    post = db.query(Post).filter(Post.post_id == post_id).first()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Publicación no encontrada"
        )
    
    # Cancelar programación
    from app.services.scheduler import PostScheduler
    scheduler = PostScheduler()
    
    success = scheduler.cancel_scheduled_post(post_id)
    
    if success:
        return {
            "success": True,
            "message": "Programación cancelada con éxito"
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al cancelar la programación"
        )