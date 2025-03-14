# app/schemas/post.py
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field

# Esquema base para Post
class PostBase(BaseModel):
    job_title: str = Field(..., min_length=3, max_length=100)
    location: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    requirements: Optional[str] = None
    position_priority: int = Field(5, ge=1, le=10)
    location_priority: int = Field(3, ge=1, le=10)
    email_priority: int = Field(3, ge=1, le=10)
    requirements_priority: int = Field(4, ge=1, le=10)

# Esquema para crear un post
class PostCreate(PostBase):
    template_id: int
    
# Esquema para programar un post
class PostSchedule(BaseModel):
    post_id: int
    scheduled_for: datetime
    frequency: Optional[str] = "once"  # once, daily, weekly, monthly
    recurrence_pattern: Optional[str] = None
    end_date: Optional[datetime] = None

# Esquema para actualizar un post
class PostUpdate(BaseModel):
    job_title: Optional[str] = None
    location: Optional[str] = None
    email: Optional[EmailStr] = None
    requirements: Optional[str] = None
    position_priority: Optional[int] = None
    location_priority: Optional[int] = None
    email_priority: Optional[int] = None
    requirements_priority: Optional[int] = None
    template_id: Optional[int] = None
    status: Optional[str] = None

# Esquema para respuesta de post
class PostInDB(PostBase):
    post_id: int
    user_id: int
    template_id: int
    status: str
    instagram_post_id: Optional[str] = None
    created_at: datetime
    scheduled_for: Optional[datetime] = None
    published_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True

# Esquema para respuesta con URL de imagen
class PostResponse(PostInDB):
    image_url: Optional[str] = None

# Esquema para publicación inmediata
class PostPublishNow(BaseModel):
    post_id: int