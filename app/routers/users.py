"""
Router para endpoints de usuarios
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.schemas.user import Usuario, UsuarioCrear, UsuarioActualizar, UsuarioLista
from app.services.user_service import UsuarioService

router = APIRouter(
    prefix="/api/usuarios",
    tags=["usuarios"],
    responses={404: {"description": "Usuario no encontrado"}}
)


@router.get("/", response_model=List[UsuarioLista])
def listar_usuarios(
    skip: int = 0,
    limit: int = 100,
    activo: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """
    Listar usuarios con paginación y filtros
    
    - **skip**: Número de registros a omitir
    - **limit**: Máximo número de registros a retornar
    - **activo**: Filtrar por estado activo (True/False)
    """
    usuarios = UsuarioService.obtener_usuarios(db, skip, limit, activo)
    return usuarios


@router.get("/{usuario_id}", response_model=Usuario)
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """
    Obtener un usuario específico por ID
    """
    usuario = UsuarioService.obtener_usuario_por_id(db, usuario_id)
    return usuario


@router.post("/", response_model=Usuario, status_code=201)
def crear_usuario(usuario: UsuarioCrear, db: Session = Depends(get_db)):
    """
    Crear un nuevo usuario
    
    - **nombre**: Nombre completo del usuario
    - **email**: Email único del usuario
    - **edad**: Edad del usuario (opcional)
    - **activo**: Estado del usuario (por defecto True)
    """
    nuevo_usuario = UsuarioService.crear_usuario(db, usuario)
    return nuevo_usuario


@router.put("/{usuario_id}", response_model=Usuario)
def actualizar_usuario(
    usuario_id: int,
    usuario_data: UsuarioActualizar,
    db: Session = Depends(get_db)
):
    """
    Actualizar un usuario existente
    
    Solo se actualizan los campos proporcionados
    """
    usuario_actualizado = UsuarioService.actualizar_usuario(db, usuario_id, usuario_data)
    return usuario_actualizado


@router.delete("/{usuario_id}")
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """
    Eliminar un usuario
    """
    UsuarioService.eliminar_usuario(db, usuario_id)
    return {"mensaje": "Usuario eliminado correctamente", "id": usuario_id}
