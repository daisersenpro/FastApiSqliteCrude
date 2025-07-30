"""
Router para estadísticas y monitoreo
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.services.user_service import UsuarioService

router = APIRouter(
    prefix="/api",
    tags=["sistema"]
)


@router.get("/")
def api_root():
    """Información de la API"""
    return {
        "mensaje": "FastAPI + React Backend funcionando! 🚀",
        "version": "2.0.0",
        "docs": "/api/docs"
    }


@router.get("/estadisticas")
def obtener_estadisticas(db: Session = Depends(get_db)):
    """
    Estadísticas del sistema para el dashboard
    
    Retorna información sobre usuarios registrados
    """
    estadisticas = UsuarioService.obtener_estadisticas(db)
    return estadisticas


@router.get("/health")
def health_check():
    """
    Endpoint de salud para monitoreo
    
    Útil para verificar que la API esté funcionando
    """
    return {
        "status": "OK",
        "timestamp": datetime.now(),
        "version": "2.0.0"
    }
