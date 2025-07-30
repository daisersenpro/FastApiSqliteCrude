"""
Aplicación principal FastAPI
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

# Importar routers
from app.routers.users import router as users_router
from app.routers.system import router as system_router
from app.database import engine
from app.models import UsuarioORM

# Crear tablas
UsuarioORM.metadata.create_all(bind=engine)

# Crear aplicación FastAPI
app = FastAPI(
    title="FastAPI + React CRUD Professional",
    description="API REST profesional para gestión de usuarios con interfaz React",
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

# Incluir routers
app.include_router(system_router)
app.include_router(users_router)

# Servir archivos estáticos de React
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")


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


@app.get("/{full_path:path}")
def serve_react_app(full_path: str):
    """Servir archivos estáticos o la aplicación React para SPA routing"""
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
