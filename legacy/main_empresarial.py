"""
FastAPI CRUD Empresarial - Versión mejorada para Procobro
Incluye funcionalidades empresariales como reportes, logging y validaciones robustas
"""

from fastapi import FastAPI, HTTPException, Depends, Query
from pydantic import BaseModel, EmailStr, validator
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, func, text
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from datetime import datetime
from typing import List, Optional
import logging

# Configurar logging empresarial
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('fastapi_empresa.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("FastAPI-Empresa")

# Configuración de BD
DATABASE_URL = "sqlite:///./empresa_usuarios.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

# Modelo ORM mejorado para empresa
class UsuarioORM(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    telefono = Column(String, nullable=True)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Crear tablas
Base.metadata.create_all(bind=engine)

# Modelos Pydantic empresariales
class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr
    telefono: Optional[str] = None
    activo: bool = True
    
    @validator('nombre')
    def validar_nombre(cls, v):
        if len(v.strip()) < 2:
            raise ValueError('El nombre debe tener al menos 2 caracteres')
        return v.strip().title()
    
    @validator('telefono')
    def validar_telefono(cls, v):
        if v:
            # Remover espacios y caracteres especiales
            limpio = v.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
            if not limpio.replace('+', '').isdigit():
                raise ValueError('Formato de teléfono inválido')
        return v

class UsuarioCrear(UsuarioBase):
    pass

class UsuarioActualizar(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    activo: Optional[bool] = None

class Usuario(UsuarioBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ReporteUsuarios(BaseModel):
    total_usuarios: int
    usuarios_activos: int
    usuarios_inactivos: int
    usuarios_hoy: int
    fecha_reporte: datetime

# Dependencia para obtener sesión de BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Error en base de datos: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

# Crear aplicación FastAPI
app = FastAPI(
    title="Sistema CRUD Empresarial",
    description="API para gestión de usuarios con funcionalidades empresariales",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Middleware para logging de requests
@app.middleware("http")
async def log_requests(request, call_next):
    start_time = datetime.now()
    
    try:
        response = await call_next(request)
        
        # Log de request exitoso
        duration = (datetime.now() - start_time).total_seconds()
        logger.info(f"✅ {request.method} {request.url.path} - {response.status_code} - {duration:.2f}s")
        
        return response
        
    except Exception as e:
        # Log de error
        logger.error(f"❌ ERROR {request.method} {request.url.path}: {str(e)}")
        raise

# =============================================================================
# ENDPOINTS BÁSICOS MEJORADOS
# =============================================================================

@app.get("/usuarios", response_model=List[Usuario])
def listar_usuarios(
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Máximo registros a devolver"),
    activo: Optional[bool] = Query(None, description="Filtrar por usuarios activos/inactivos"),
    db: Session = Depends(get_db)
):
    """
    Listar usuarios con paginación y filtros
    - Soporte para paginación empresarial
    - Filtro por estado activo/inactivo
    - Logging automático
    """
    try:
        query = db.query(UsuarioORM)
        
        if activo is not None:
            query = query.filter(UsuarioORM.activo == activo)
        
        usuarios = query.offset(skip).limit(limit).all()
        
        logger.info(f"📋 Listado de usuarios: {len(usuarios)} registros (skip={skip}, limit={limit})")
        
        return usuarios
        
    except Exception as e:
        logger.error(f"Error al listar usuarios: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@app.post("/usuarios", response_model=Usuario, status_code=201)
def crear_usuario(usuario: UsuarioCrear, db: Session = Depends(get_db)):
    """
    Crear nuevo usuario con validaciones empresariales
    - Validación de email único
    - Logging de operaciones
    - Manejo robusto de errores
    """
    try:
        # Verificar si el email ya existe
        usuario_existente = db.query(UsuarioORM).filter(UsuarioORM.email == usuario.email).first()
        if usuario_existente:
            logger.warning(f"Intento de crear usuario con email duplicado: {usuario.email}")
            raise HTTPException(status_code=400, detail="El email ya está registrado")
        
        # Crear usuario
        nuevo_usuario = UsuarioORM(**usuario.model_dump())
        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)
        
        logger.info(f"✅ Usuario creado: {nuevo_usuario.nombre} ({nuevo_usuario.email})")
        
        return nuevo_usuario
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error al crear usuario: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@app.put("/usuarios/{usuario_id}", response_model=Usuario)
def actualizar_usuario(usuario_id: int, usuario_data: UsuarioActualizar, db: Session = Depends(get_db)):
    """
    Actualizar usuario existente (funcionalidad faltante en versión básica)
    """
    try:
        usuario = db.query(UsuarioORM).filter(UsuarioORM.id == usuario_id).first()
        if not usuario:
            logger.warning(f"Intento de actualizar usuario inexistente: ID {usuario_id}")
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # Actualizar solo los campos proporcionados
        update_data = usuario_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(usuario, field, value)
        
        usuario.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(usuario)
        
        logger.info(f"📝 Usuario actualizado: ID {usuario_id} - {usuario.nombre}")
        
        return usuario
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error al actualizar usuario {usuario_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@app.delete("/usuarios/{usuario_id}")
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """
    Eliminar usuario (soft delete recomendado para empresas)
    """
    try:
        usuario = db.query(UsuarioORM).filter(UsuarioORM.id == usuario_id).first()
        if not usuario:
            logger.warning(f"Intento de eliminar usuario inexistente: ID {usuario_id}")
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # Soft delete - marcar como inactivo en lugar de eliminar
        usuario.activo = False
        usuario.updated_at = datetime.utcnow()
        db.commit()
        
        logger.info(f"🗑️ Usuario desactivado: ID {usuario_id} - {usuario.nombre}")
        
        return {"mensaje": "Usuario desactivado correctamente", "id": usuario_id}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error al eliminar usuario {usuario_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

# =============================================================================
# ENDPOINTS EMPRESARIALES - REPORTES Y ANÁLISIS
# =============================================================================

@app.get("/reportes/usuarios", response_model=ReporteUsuarios)
def generar_reporte_usuarios(db: Session = Depends(get_db)):
    """
    Generar reporte completo de usuarios para jefatura
    - Estadísticas generales
    - Usuarios creados hoy
    - Estado activo/inactivo
    """
    try:
        hoy = datetime.now().date()
        
        total_usuarios = db.query(UsuarioORM).count()
        usuarios_activos = db.query(UsuarioORM).filter(UsuarioORM.activo == True).count()
        usuarios_inactivos = total_usuarios - usuarios_activos
        usuarios_hoy = db.query(UsuarioORM).filter(
            func.date(UsuarioORM.created_at) == hoy
        ).count()
        
        reporte = ReporteUsuarios(
            total_usuarios=total_usuarios,
            usuarios_activos=usuarios_activos,
            usuarios_inactivos=usuarios_inactivos,
            usuarios_hoy=usuarios_hoy,
            fecha_reporte=datetime.now()
        )
        
        logger.info(f"📊 Reporte generado: {total_usuarios} usuarios totales, {usuarios_hoy} nuevos hoy")
        
        return reporte
        
    except Exception as e:
        logger.error(f"Error al generar reporte: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@app.get("/consultas/sql")
def ejecutar_consulta_personalizada(
    query: str = Query(..., description="Consulta SQL personalizada"),
    db: Session = Depends(get_db)
):
    """
    Ejecutar consultas SQL personalizadas (para extracción de información)
    ⚠️ En producción, restringir a usuarios admin únicamente
    """
    try:
        # Validar que sea solo SELECT (seguridad básica)
        if not query.strip().upper().startswith('SELECT'):
            raise HTTPException(status_code=400, detail="Solo se permiten consultas SELECT")
        
        result = db.execute(text(query))
        rows = result.fetchall()
        
        # Convertir a lista de diccionarios
        columns = result.keys()
        data = [dict(zip(columns, row)) for row in rows]
        
        logger.info(f"🔍 Consulta SQL ejecutada: {len(data)} registros devueltos")
        
        return {"data": data, "count": len(data)}
        
    except Exception as e:
        logger.error(f"Error en consulta SQL: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error en consulta: {str(e)}")

# =============================================================================
# ENDPOINTS DE MONITOREO Y SALUD DEL SISTEMA
# =============================================================================

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    """
    Endpoint de salud del sistema para monitoreo
    """
    try:
        # Verificar conectividad de BD
        db.execute(text("SELECT 1"))
        
        return {
            "status": "healthy",
            "timestamp": datetime.now(),
            "database": "connected",
            "version": "2.0.0"
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail="Sistema no disponible")

@app.get("/logs/recientes")
def obtener_logs_recientes(lineas: int = Query(50, ge=1, le=1000)):
    """
    Obtener logs recientes del sistema para análisis de incidencias
    """
    try:
        with open('fastapi_empresa.log', 'r', encoding='utf-8') as f:
            todas_las_lineas = f.readlines()
            logs_recientes = todas_las_lineas[-lineas:]
        
        return {
            "logs": logs_recientes,
            "total_lineas": len(logs_recientes),
            "timestamp": datetime.now()
        }
    except FileNotFoundError:
        return {"logs": [], "mensaje": "Archivo de logs no encontrado"}
    except Exception as e:
        logger.error(f"Error al obtener logs: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al acceder a logs")

# =============================================================================
# EVENTOS DE INICIO Y CIERRE
# =============================================================================

@app.on_event("startup")
async def startup_event():
    """Evento de inicio de la aplicación"""
    logger.info("🚀 FastAPI Empresarial iniciado correctamente")
    logger.info("📊 Base de datos conectada")
    logger.info("🔧 Sistema listo para recibir requests")

@app.on_event("shutdown")
async def shutdown_event():
    """Evento de cierre de la aplicación"""
    logger.info("🛑 FastAPI Empresarial cerrando...")
    logger.info("💾 Cerrando conexiones de base de datos")

if __name__ == "__main__":
    import uvicorn
    logger.info("🔥 Iniciando servidor en modo desarrollo")
    uvicorn.run("main_empresarial:app", host="127.0.0.1", port=8000, reload=True)
