"""
Punto de entrada para ejecutar la aplicación
"""

import uvicorn
from app.main import app

if __name__ == "__main__":
    print("🚀 Iniciando FastAPI + React Professional Backend...")
    print("📖 Documentación API: http://127.0.0.1:8000/api/docs")
    print("🌐 React App: http://127.0.0.1:8000")
    print("📋 Arquitectura: Modular y Profesional")
    
    uvicorn.run(
        "app.main:app", 
        host="127.0.0.1", 
        port=8000, 
        reload=True
    )
