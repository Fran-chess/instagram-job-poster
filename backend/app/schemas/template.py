# app/schemas/template.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

# Esquema base para Template
class TemplateBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = None
    background_color: str = Field("#FFFFFF", regex=r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$")
    text_color: str = Field("#000000", regex=r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$")
    footer_text: Optional[str] = None

# Esquema para crear un template
class TemplateCreate(TemplateBase):
    pass

# Esquema para actualizar un template
class TemplateUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    background_color: Optional[str] = None
    text_color: Optional[str] = None
    footer_text: Optional[str] = None
    is_active: Optional[bool] = None

# Esquema para respuesta de template
class TemplateInDB(TemplateBase):
    template_id: int
    created_at: datetime
    is_active: bool
    
    class Config:
        orm_mode = True

# Esquema para respuesta con URL de imagen
class TemplateResponse(TemplateInDB):
    image_url: Optional[str] = None