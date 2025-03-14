# backend/app/db/models.py
import datetime
from typing import List, Optional
from sqlalchemy import Boolean, Column, Integer, String, Text, LargeBinary, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    last_login = Column(DateTime, default=func.now())
    is_active = Column(Boolean, default=True)
    
    # Relaciones
    posts = relationship("Post", back_populates="creator")

class Template(Base):
    __tablename__ = "templates"
    
    template_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    background_color = Column(String(20), default="#FFFFFF")
    text_color = Column(String(20), default="#000000")
    footer_text = Column(String(200))
    template_image = Column(LargeBinary, nullable=True)  # Imagen base para la plantilla
    created_at = Column(DateTime, default=func.now())
    is_active = Column(Boolean, default=True)
    
    # Relaciones
    posts = relationship("Post", back_populates="template")

class Post(Base):
    __tablename__ = "posts"
    
    post_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    template_id = Column(Integer, ForeignKey("templates.template_id"), nullable=False)
    
    # Campos de la oferta laboral
    job_title = Column(String(100), nullable=False)
    location = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    requirements = Column(Text)
    
    # Prioridades visuales
    position_priority = Column(Integer, default=5)
    location_priority = Column(Integer, default=3)
    email_priority = Column(Integer, default=3)
    requirements_priority = Column(Integer, default=4)
    
    # Campos relacionados con la publicación
    generated_image = Column(LargeBinary, nullable=True)  # Imagen generada
    instagram_post_id = Column(String(100), nullable=True)  # ID de la publicación en Instagram
    status = Column(String(20), default="draft")  # draft, scheduled, published, failed
    
    # Fechas
    created_at = Column(DateTime, default=func.now())
    scheduled_for = Column(DateTime, nullable=True)
    published_at = Column(DateTime, nullable=True)
    
    # Relaciones
    creator = relationship("User", back_populates="posts")
    template = relationship("Template", back_populates="posts")
    logs = relationship("PostLog", back_populates="post")
    schedule = relationship("ScheduleSettings", back_populates="post", uselist=False)

class PostLog(Base):
    __tablename__ = "post_logs"
    
    log_id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.post_id"), nullable=False)
    action = Column(String(50), nullable=False)  # generate, schedule, publish, error
    status = Column(String(20), nullable=False)  # success, error
    error_message = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=func.now())
    
    # Relaciones
    post = relationship("Post", back_populates="logs")

class ScheduleSettings(Base):
    __tablename__ = "schedule_settings"
    
    schedule_id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.post_id"), unique=True, nullable=False)
    scheduled_time = Column(DateTime, nullable=False)
    frequency = Column(String(20), nullable=True)  # once, daily, weekly, monthly
    recurrence_pattern = Column(String(50), nullable=True)  # Para definir patrones específicos
    end_date = Column(DateTime, nullable=True)  # Para publicaciones recurrentes
    is_active = Column(Boolean, default=True)
    
    # Relaciones
    post = relationship("Post", back_populates="schedule")