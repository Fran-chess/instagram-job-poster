from fastapi import APIRouter, Depends, HTTPException, status, Form, File, UploadFile
from typing import List, Optional
from datetime import datetime

from app.db.models import PostResponse, PostCreate, PostUpdate
from app.services.image_generator import ImageGenerator
from app.services.instagram_api import InstagramPublisher

router = APIRouter(prefix="/posts", tags=["posts"])

@router.get("/", response_model=List[PostResponse])
async def get_posts():
    """Obtener todas las publicaciones"""
    # Implementación real debería obtener posts de la base de datos
    return []

@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    job_title: str = Form(...),
    location: str = Form(...),
    email: str = Form(...),
    requirements: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None)
):
    """Crear una nueva publicación de oferta laboral"""
    try:
        # Inicializar generador de imágenes
        image_generator = ImageGenerator()
        
        # Generar imagen
        image_path = image_generator.generate_job_post_image(
            job_title=job_title,
            location=location,
            email=email,
            requirements=requirements
        )
        
        # En una implementación real, guardaríamos el post en la base de datos
        # y podríamos usar el servicio de Instagram para publicarlo
        
        return {
            "id": 1,  # ID ficticio
            "job_title": job_title,
            "location": location,
            "email": email,
            "requirements": requirements,
            "image_path": image_path,
            "status": "draft",
            "created_at": datetime.now(),
            "published_at": None,
            "instagram_post_id": None
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear la publicación: {str(e)}"
        )

@router.post("/{post_id}/publish", response_model=PostResponse)
async def publish_post(post_id: int):
    """Publicar una oferta laboral en Instagram"""
    # Implementación real debería publicar en Instagram
    # y actualizar el estado del post en la base de datos
    
    return {
        "id": post_id,
        "job_title": "Ejemplo",
        "location": "Ejemplo",
        "email": "ejemplo@email.com",
        "requirements": None,
        "image_path": "/media/generated/example.png",
        "status": "published",
        "created_at": datetime.now(),
        "published_at": datetime.now(),
        "instagram_post_id": "123456789"
    }

@router.get("/{post_id}", response_model=PostResponse)
async def get_post(post_id: int):
    """Obtener información de una publicación específica"""
    # Implementación real debería obtener el post de la base de datos
    
    return {
        "id": post_id,
        "job_title": "Ejemplo",
        "location": "Ejemplo",
        "email": "ejemplo@email.com",
        "requirements": None,
        "image_path": "/media/generated/example.png",
        "status": "draft",
        "created_at": datetime.now(),
        "published_at": None,
        "instagram_post_id": None
    }

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int):
    """Eliminar una publicación"""
    # Implementación real debería eliminar el post de la base de datos
    return None
