# app/schemas/user.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

# Esquema base para User
class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: str = Field(..., min_length=3, max_length=100)
    is_active: bool = True

# Esquema para crear un usuario
class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

# Esquema para actualizar un usuario
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None

# Esquema para respuesta de usuario
class UserInDB(UserBase):
    user_id: int
    last_login: Optional[datetime] = None
    
    class Config:
        orm_mode = True

# Esquema para login
class UserLogin(BaseModel):
    username: str
    password: str

# Esquema para token
class Token(BaseModel):
    access_token: str
    token_type: str

# Esquema para datos del payload del token
class TokenPayload(BaseModel):
    sub: Optional[int] = None