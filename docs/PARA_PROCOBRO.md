# 🚀 FastAPI para Procobro - Extensiones empresariales

## 📋 Requisitos de la empresa vs. Tu proyecto actual

### ✅ **Lo que ya tienes cubierto:**
- **Python**: ✅ Fundamentos sólidos
- **FastAPI**: ✅ CRUD funcional con documentación
- **Base de datos**: ✅ SQLAlchemy ORM + SQLite
- **API REST**: ✅ Endpoints estándar
- **Documentación**: ✅ Swagger UI automática

### 🔄 **Lo que necesitas agregar/mejorar:**

---

## 🗄️ **1. Consultas SQL avanzadas**

### Ejemplo de extracción de información de BBDD:
```python
from sqlalchemy import text, func
from datetime import datetime, timedelta

# Consulta SQL directa para reportes
@app.get("/reportes/usuarios-por-fecha")
def reporte_usuarios_fecha(fecha_desde: str, fecha_hasta: str):
    db = SessionLocal()
    
    # Consulta SQL directa (como piden en la empresa)
    query = text("""
        SELECT 
            COUNT(*) as total_usuarios,
            DATE(created_at) as fecha_registro
        FROM usuarios 
        WHERE created_at BETWEEN :fecha_desde AND :fecha_hasta
        GROUP BY DATE(created_at)
        ORDER BY fecha_registro DESC
    """)
    
    resultado = db.execute(query, {
        "fecha_desde": fecha_desde,
        "fecha_hasta": fecha_hasta
    })
    
    db.close()
    return [{"fecha": row.fecha_registro, "total": row.total_usuarios} 
            for row in resultado]

# Extracción para Excel/reportes
@app.get("/exportar/usuarios-excel")
def exportar_usuarios_excel():
    import pandas as pd
    
    db = SessionLocal()
    usuarios = db.query(UsuarioORM).all()
    db.close()
    
    # Convertir a DataFrame para Excel
    data = [{
        "ID": u.id,
        "Nombre": u.nombre,
        "Email": u.email,
        "Fecha_Registro": u.created_at
    } for u in usuarios]
    
    df = pd.DataFrame(data)
    df.to_excel("reporte_usuarios.xlsx", index=False)
    
    return {"mensaje": "Excel generado", "archivo": "reporte_usuarios.xlsx"}
```

---

## 📊 **2. Procesos de carga/descarga masiva**

```python
from fastapi import UploadFile, File
import csv
import io

# Carga masiva desde CSV
@app.post("/carga-masiva/usuarios")
async def carga_masiva_usuarios(archivo: UploadFile = File(...)):
    if not archivo.filename.endswith('.csv'):
        raise HTTPException(400, "Solo archivos CSV")
    
    contenido = await archivo.read()
    csv_data = csv.DictReader(io.StringIO(contenido.decode('utf-8')))
    
    db = SessionLocal()
    usuarios_creados = 0
    
    try:
        for fila in csv_data:
            nuevo_usuario = UsuarioORM(
                id=int(fila['id']),
                nombre=fila['nombre'],
                email=fila['email']
            )
            db.add(nuevo_usuario)
            usuarios_creados += 1
        
        db.commit()
        return {
            "mensaje": "Carga completada",
            "usuarios_creados": usuarios_creados
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(500, f"Error en carga: {str(e)}")
    finally:
        db.close()

# Descarga masiva a CSV
@app.get("/descarga-masiva/usuarios")
def descarga_masiva_usuarios():
    db = SessionLocal()
    usuarios = db.query(UsuarioORM).all()
    db.close()
    
    # Crear CSV en memoria
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Cabeceras
    writer.writerow(['ID', 'Nombre', 'Email'])
    
    # Datos
    for usuario in usuarios:
        writer.writerow([usuario.id, usuario.nombre, usuario.email])
    
    return {
        "data": output.getvalue(),
        "filename": f"usuarios_{datetime.now().strftime('%Y%m%d')}.csv"
    }
```

---

## 📈 **3. Sistema de reportes para jefatura**

```python
from datetime import datetime
import smtplib
from email.mime.text import MimeText

# Reporte diario automático
@app.get("/reportes/diario")
def reporte_diario():
    db = SessionLocal()
    
    # Estadísticas del día
    hoy = datetime.now().date()
    total_usuarios = db.query(UsuarioORM).count()
    usuarios_hoy = db.query(UsuarioORM).filter(
        func.date(UsuarioORM.created_at) == hoy
    ).count()
    
    reporte = {
        "fecha": str(hoy),
        "total_usuarios": total_usuarios,
        "usuarios_nuevos_hoy": usuarios_hoy,
        "status": "OK"
    }
    
    db.close()
    
    # Enviar por email (simulado)
    enviar_reporte_email(reporte)
    
    return reporte

def enviar_reporte_email(reporte):
    """Envía reporte automático a jefatura"""
    # Aquí iría la lógica de envío de email
    print(f"📧 Reporte enviado a jefatura: {reporte}")
```

---

## 🚨 **4. Monitoreo y manejo de incidencias**

```python
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('api_logs.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Middleware para monitoreo
@app.middleware("http")
async def log_requests(request, call_next):
    start_time = datetime.now()
    
    try:
        response = await call_next(request)
        
        # Log exitoso
        logger.info(f"✅ {request.method} {request.url} - {response.status_code}")
        
        return response
        
    except Exception as e:
        # Log de error - reportar incidencia
        logger.error(f"❌ ERROR en {request.method} {request.url}: {str(e)}")
        
        # Reportar incidencia crítica
        if "database" in str(e).lower():
            reportar_incidencia_critica(f"Error de BD: {str(e)}")
        
        raise e

def reportar_incidencia_critica(mensaje):
    """Reporta incidencias críticas de forma oportuna"""
    incidencia = {
        "timestamp": datetime.now().isoformat(),
        "nivel": "CRITICO",
        "mensaje": mensaje,
        "sistema": "FastAPI CRUD"
    }
    
    # Aquí irían notificaciones automáticas
    logger.critical(f"🚨 INCIDENCIA CRÍTICA: {incidencia}")
    
    # Guardar en BD de incidencias
    # enviar_alerta_slack(incidencia)
    # enviar_email_urgente(incidencia)

# Endpoint para consultar logs
@app.get("/admin/logs")
def obtener_logs(lineas: int = 100):
    """Obtiene los últimos logs para análisis"""
    try:
        with open('api_logs.log', 'r') as f:
            logs = f.readlines()
            return {"logs": logs[-lineas:]}
    except FileNotFoundError:
        return {"logs": [], "mensaje": "No hay logs disponibles"}
```

---

## 💼 **5. Características empresariales adicionales**

### Autenticación y autorización:
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer

security = HTTPBearer()

def verificar_token(token = Depends(security)):
    """Verificar token de autenticación"""
    # Lógica de verificación de token
    if not validar_token(token.credentials):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )
    return token

@app.get("/admin/usuarios", dependencies=[Depends(verificar_token)])
def listar_usuarios_admin():
    """Endpoint protegido para administradores"""
    # Solo accesible con token válido
    pass
```

### Validaciones robustas:
```python
from pydantic import EmailStr, validator
from typing import Optional

class UsuarioEmpresarial(BaseModel):
    id: int
    nombre: str
    email: EmailStr  # Validación automática de email
    telefono: Optional[str] = None
    activo: bool = True
    
    @validator('nombre')
    def validar_nombre(cls, v):
        if len(v) < 2:
            raise ValueError('Nombre muy corto')
        return v.title()
    
    @validator('telefono')
    def validar_telefono(cls, v):
        if v and not v.replace('+', '').replace('-', '').isdigit():
            raise ValueError('Teléfono inválido')
        return v
```

---

## 📚 **6. Habilidades que demuestra este proyecto:**

### ✅ **Desarrollo Full Stack:**
- Backend con FastAPI
- Base de datos con SQLAlchemy
- APIs REST estándar
- Documentación automática

### ✅ **Extracción de información de BBDD:**
- Consultas SQL directas
- Reportes automáticos
- Exportación a Excel/CSV

### ✅ **Procesos de carga/descarga:**
- Carga masiva desde CSV
- Descarga masiva a archivos
- Manejo de errores robusto

### ✅ **Reportes a jefatura:**
- Reportes automáticos
- Estadísticas en tiempo real
- Envío por email

### ✅ **Manejo de incidencias:**
- Logging completo
- Monitoreo automático
- Alertas de errores críticos

---

## 🎯 **Para la entrevista técnica:**

### Prepárate para explicar:
1. **Arquitectura del proyecto**: ORM, API, validación
2. **Consultas SQL**: Joins, agregaciones, subconsultas
3. **Manejo de errores**: Try/catch, logging, rollbacks
4. **Performance**: Índices, paginación, cache
5. **Seguridad**: Autenticación, validación, sanitización

### Términos técnicos importantes:
- **ORM**: Object-Relational Mapping
- **CRUD**: Create, Read, Update, Delete
- **API REST**: Representational State Transfer
- **JSON**: JavaScript Object Notation
- **HTTP Status Codes**: 200, 201, 404, 500, etc.
- **Async/Await**: Programación asíncrona

---

## 💡 **Próximos pasos para mejorar:**

1. **Agregar PUT endpoint** (Update completo)
2. **Implementar paginación** para listas grandes
3. **Añadir filtros** en las consultas
4. **Cache con Redis** para mejor performance
5. **Tests unitarios** con pytest
6. **Documentación de API** más detallada
7. **Docker** para deployment

¡Con estos conceptos y ejemplos estarás bien preparado para la entrevista! 🚀
