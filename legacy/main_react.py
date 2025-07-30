"""
FastAPI Backend mejorado con CORS para React Frontend
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, EmailStr, validator
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from datetime import datetime
from typing import List, Optional
import os

# Configuración de BD
DATABASE_URL = "sqlite:///./usuarios.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

# Modelo ORM mejorado
class UsuarioORM(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    edad = Column(Integer, nullable=True)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

# Crear tablas
Base.metadata.create_all(bind=engine)

# Modelos Pydantic mejorados
class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr
    edad: Optional[int] = None
    activo: bool = True
    
    @validator('nombre')
    def validar_nombre(cls, v):
        if len(v.strip()) < 2:
            raise ValueError('El nombre debe tener al menos 2 caracteres')
        return v.strip().title()
    
    @validator('edad')
    def validar_edad(cls, v):
        if v is not None and (v < 0 or v > 120):
            raise ValueError('La edad debe estar entre 0 y 120 años')
        return v

class UsuarioCrear(UsuarioBase):
    pass

class UsuarioActualizar(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    edad: Optional[int] = None
    activo: Optional[bool] = None

class Usuario(UsuarioBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Dependencia para BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crear aplicación FastAPI
app = FastAPI(
    title="FastAPI + React CRUD",
    description="API REST para gestión de usuarios con interfaz React",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Configurar CORS para React
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React dev server
        "http://127.0.0.1:3000",
        "http://localhost:5173",  # Vite dev server
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Servir archivos estáticos de React (si está compilado)
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# API Endpoints con prefijo /api
@app.get("/api/")
def api_root():
    return {
        "mensaje": "FastAPI + React Backend funcionando! 🚀",
        "version": "2.0.0",
        "docs": "/api/docs"
    }

@app.get("/api/usuarios", response_model=List[Usuario])
def listar_usuarios(
    skip: int = 0, 
    limit: int = 100,
    activo: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Listar usuarios con paginación y filtros"""
    query = db.query(UsuarioORM)
    
    if activo is not None:
        query = query.filter(UsuarioORM.activo == activo)
    
    usuarios = query.offset(skip).limit(limit).all()
    return usuarios

@app.get("/api/usuarios/{usuario_id}", response_model=Usuario)
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """Obtener un usuario específico por ID"""
    usuario = db.query(UsuarioORM).filter(UsuarioORM.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@app.post("/api/usuarios", response_model=Usuario, status_code=201)
def crear_usuario(usuario: UsuarioCrear, db: Session = Depends(get_db)):
    """Crear un nuevo usuario"""
    # Verificar email único
    usuario_existente = db.query(UsuarioORM).filter(UsuarioORM.email == usuario.email).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    
    nuevo_usuario = UsuarioORM(**usuario.model_dump())
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

@app.put("/api/usuarios/{usuario_id}", response_model=Usuario)
def actualizar_usuario(
    usuario_id: int, 
    usuario_data: UsuarioActualizar, 
    db: Session = Depends(get_db)
):
    """Actualizar un usuario existente"""
    usuario = db.query(UsuarioORM).filter(UsuarioORM.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Actualizar solo los campos proporcionados
    update_data = usuario_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(usuario, field, value)
    
    db.commit()
    db.refresh(usuario)
    return usuario

@app.delete("/api/usuarios/{usuario_id}")
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """Eliminar un usuario"""
    usuario = db.query(UsuarioORM).filter(UsuarioORM.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    db.delete(usuario)
    db.commit()
    return {"mensaje": "Usuario eliminado correctamente", "id": usuario_id}

@app.get("/api/estadisticas")
def obtener_estadisticas(db: Session = Depends(get_db)):
    """Estadísticas para el dashboard"""
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

@app.get("/api/health")
def health_check():
    """Endpoint de salud para monitoreo"""
    return {
        "status": "OK", 
        "timestamp": datetime.now(),
        "version": "2.0.0"
    }

# Servir página principal (React app)
@app.get("/")
def home():
    """Servir la aplicación React desde la raíz"""
    index_file = "static/index.html"
    if os.path.exists(index_file):
        return FileResponse(index_file)
    
    return {
        "mensaje": "FastAPI + React Backend funcionando! 🚀",
        "frontend": "Interfaz React disponible cuando se compile",
        "api_docs": "http://127.0.0.1:8000/api/docs",
        "redoc": "http://127.0.0.1:8000/api/redoc"
    }

# Servir otras rutas de React (para SPA routing)
@app.get("/{full_path:path}")
def serve_react_app(full_path: str):
    """Servir archivos estáticos o la aplicación React"""
    # Evitar conflictos con rutas API
    if full_path.startswith("api/"):
        raise HTTPException(status_code=404, detail="API endpoint not found")
    
    # Si existe el archivo estático específico, servirlo
    static_file = f"static/{full_path}"
    if os.path.exists(static_file) and os.path.isfile(static_file):
        return FileResponse(static_file)
    
    # Para rutas de React SPA, servir index.html
    index_file = "static/index.html"
    if os.path.exists(index_file):
        return FileResponse(index_file)
    
    # Fallback
    return {
        "mensaje": "Ruta no encontrada",
        "available_routes": {
            "home": "http://127.0.0.1:8000/",
            "api_docs": "http://127.0.0.1:8000/api/docs",
            "api": "http://127.0.0.1:8000/api/"
        }
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Iniciando FastAPI + React Backend...")
    print("📖 Documentación API: http://127.0.0.1:8000/api/docs")
    print("🌐 React App: http://127.0.0.1:8000")
    uvicorn.run("main_react:app", host="127.0.0.1", port=8000, reload=True)
