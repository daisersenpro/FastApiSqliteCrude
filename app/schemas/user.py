"""
Schemas Pydantic para Usuario
"""

from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime


class UsuarioBase(BaseModel):
    """Schema base para Usuario"""
    nombre: str
    email: EmailStr
    edad: Optional[int] = None
    activo: bool = True
    
    @validator('nombre')
    def validar_nombre(cls, v):
        """Validar que el nombre tenga al menos 2 caracteres"""
        if len(v.strip()) < 2:
            raise ValueError('El nombre debe tener al menos 2 caracteres')
        return v.strip().title()
    
    @validator('edad')
    def validar_edad(cls, v):
        """Validar que la edad esté en rango válido"""
        if v is not None and (v < 0 or v > 120):
            raise ValueError('La edad debe estar entre 0 y 120 años')
        return v


class UsuarioCrear(UsuarioBase):
    """Schema para crear usuario"""
    pass


class UsuarioActualizar(BaseModel):
    """Schema para actualizar usuario (campos opcionales)"""
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    edad: Optional[int] = None
    activo: Optional[bool] = None


class Usuario(UsuarioBase):
    """Schema de respuesta con datos completos"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class UsuarioLista(BaseModel):
    """Schema para listado de usuarios"""
    id: int
    nombre: str
    email: str
    activo: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
