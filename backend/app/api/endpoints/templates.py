# app/api/endpoints/templates.py
import os
import shutil
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.db.models import Template, User
from app.schemas.template import TemplateCreate, TemplateUpdate, TemplateResponse
from app.core.config import settings
from app.utils.image_utils import get_image_url

router = APIRouter(prefix="/templates", tags=["templates"])

@router.get("/", response_model=List[TemplateResponse])
def get_templates(
    skip: int = 0, 
    limit: int = 100,
    active_only: bool = True,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Obtener todas las plantillas.
    """
    # Construir query base
    query = db.query(Template)
    
    # Filtrar por activas si se especifica
    if active_only:
        query = query.filter(Template.is_active == True)
    
    # Obtener plantillas con paginación
    templates = query.offset(skip).limit(limit).all()
    
    # Agregar URL de imagen para la respuesta
    for template in templates:
        # Buscar la imagen de plantilla (si existe)
        import glob
        
        template_path = os.path.join(settings.TEMPLATES_DIR, f"template_{template.template_id}.png")
        if os.path.exists(template_path):
            template.image_url = get_image_url(template_path)
        else:
            template.image_url = None
    
    return templates

@router.post("/", response_model=TemplateResponse)
def create_template(
    name: str = Form(...),
    description: str = Form(None),
    background_color: str = Form("#FFFFFF"),
    text_color: str = Form("#000000"),
    footer_text: str = Form(None),
    image: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Crear una nueva plantilla.
    """
    # Crear plantilla en la base de datos
    db_template = Template(
        name=name,
        description=description,
        background_color=background_color,
        text_color=text_color,
        footer_text=footer_text,
        is_active=True
    )
    
    # Si se proporciona imagen, guardarla
    if image:
        # Leer contenido del archivo
        template_image = image.file.read()
        db_template.template_image = template_image
    
    db.add(db_template)
    db.commit()
    db.refresh(db_template)
    
    # Si se proporcionó imagen, guardarla también en el sistema de archivos
    if image:
        # Guardar en el sistema de archivos
        os.makedirs(settings.TEMPLATES_DIR, exist_ok=True)
        template_path = os.path.join(settings.TEMPLATES_DIR, f"template_{db_template.template_id}.png")
        
        with open(template_path, "wb") as f:
            # Volver al inicio del archivo
            image.file.seek(0)
            shutil.copyfileobj(image.file, f)
        
        # Agregar URL de la imagen a la respuesta
        db_template.image_url = get_image_url(template_path)
    else:
        db_template.image_url = None
    
    return db_template

@router.get("/{template_id}", response_model=TemplateResponse)
def get_template(
    template_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Obtener una plantilla por ID.
    """
    template = db.query(Template).filter(Template.template_id == template_id).first()
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plantilla no encontrada"
        )
    
    # Agregar URL de imagen para la respuesta
    template_path = os.path.join(settings.TEMPLATES_DIR, f"template_{template.template_id}.png")
    if os.path.exists(template_path):
        template.image_url = get_image_url(template_path)
    else:
        template.image_url = None
    
    return template

@router.put("/{template_id}", response_model=TemplateResponse)
def update_template(
    template_id: int,
    template_data: TemplateUpdate = Depends(),
    image: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Actualizar una plantilla.
    """
    template = db.query(Template).filter(Template.template_id == template_id).first()
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plantilla no encontrada"
        )
    
    # Actualizar solo los campos proporcionados
    update_data = template_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(template, key, value)
    
    # Si se proporciona imagen, actualizarla
    if image:
        # Leer contenido del archivo
        template_image = image.file.read()
        template.template_image = template_image
        
        # Guardar en el sistema de archivos
        os.makedirs(settings.TEMPLATES_DIR, exist_ok=True)
        template_path = os.path.join(settings.TEMPLATES_DIR, f"template_{template.template_id}.png")
        
        with open(template_path, "wb") as f:
            # Volver al inicio del archivo
            image.file.seek(0)
            shutil.copyfileobj(image.file, f)
    
    db.commit()
    db.refresh(template)
    
    # Agregar URL de imagen para la respuesta
    template_path = os.path.join(settings.TEMPLATES_DIR, f"template_{template.template_id}.png")
    if os.path.exists(template_path):
        template.image_url = get_image_url(template_path)
    else:
        template.image_url = None
    
    return template

@router.delete("/{template_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_template(
    template_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Eliminar una plantilla (soft delete).
    """
    template = db.query(Template).filter(Template.template_id == template_id).first()
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plantilla no encontrada"
        )
    
    # Soft delete (mejor que eliminar completamente)
    template.is_active = False
    db.commit()
    
    return None