"""
Servicio de lógica de negocio para usuarios
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List, Optional
from datetime import datetime

from app.models.user import UsuarioORM
from app.schemas.user import UsuarioCrear, UsuarioActualizar


class UsuarioService:
    """Servicio para manejar la lógica de negocio de usuarios"""
    
    @staticmethod
    def obtener_usuarios(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        activo: Optional[bool] = None
    ) -> List[UsuarioORM]:
        """Obtener lista de usuarios con filtros"""
        query = db.query(UsuarioORM)
        
        if activo is not None:
            query = query.filter(UsuarioORM.activo == activo)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def obtener_usuario_por_id(db: Session, usuario_id: int) -> UsuarioORM:
        """Obtener usuario por ID"""
        usuario = db.query(UsuarioORM).filter(UsuarioORM.id == usuario_id).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return usuario
    
    @staticmethod
    def obtener_usuario_por_email(db: Session, email: str) -> Optional[UsuarioORM]:
        """Obtener usuario por email"""
        return db.query(UsuarioORM).filter(UsuarioORM.email == email).first()
    
    @staticmethod
    def crear_usuario(db: Session, usuario_data: UsuarioCrear) -> UsuarioORM:
        """Crear nuevo usuario"""
        # Verificar si el email ya existe
        usuario_existente = UsuarioService.obtener_usuario_por_email(db, usuario_data.email)
        if usuario_existente:
            raise HTTPException(
                status_code=400, 
                detail="El email ya está registrado"
            )
        
        # Crear nuevo usuario
        nuevo_usuario = UsuarioORM(**usuario_data.model_dump())
        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)
        return nuevo_usuario
    
    @staticmethod
    def actualizar_usuario(
        db: Session, 
        usuario_id: int, 
        usuario_data: UsuarioActualizar
    ) -> UsuarioORM:
        """Actualizar usuario existente"""
        usuario = UsuarioService.obtener_usuario_por_id(db, usuario_id)
        
        # Actualizar solo los campos proporcionados
        update_data = usuario_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(usuario, field, value)
        
        db.commit()
        db.refresh(usuario)
        return usuario
    
    @staticmethod
    def eliminar_usuario(db: Session, usuario_id: int) -> bool:
        """Eliminar usuario"""
        usuario = UsuarioService.obtener_usuario_por_id(db, usuario_id)
        db.delete(usuario)
        db.commit()
        return True
    
    @staticmethod
    def obtener_estadisticas(db: Session) -> dict:
        """Obtener estadísticas de usuarios"""
        total_usuarios = db.query(UsuarioORM).count()
        usuarios_activos = db.query(UsuarioORM).filter(UsuarioORM.activo == True).count()
        usuarios_hoy = db.query(UsuarioORM).filter(
            UsuarioORM.created_at >= datetime.now().date()
        ).count()
        
        return {
            "total_usuarios": total_usuarios,
            "usuarios_activos": usuarios_activos,
            "usuarios_inactivos": total_usuarios - usuarios_activos,
            "usuarios_hoy": usuarios_hoy
        }
