# 🎯 Preguntas de Entrevista Técnica - FastAPI/Python

## 📋 Preguntas básicas de Python

### **P: ¿Qué es Python y por qué lo elegirías para desarrollo backend?**
**R:** Python es un lenguaje de programación interpretado, de alto nivel y propósito general. Lo elegiría para backend porque:
- **Sintaxis clara y legible**: Fácil de mantener
- **Gran ecosistema**: Miles de librerías disponibles
- **Comunidad activa**: Mucho soporte y documentación
- **Frameworks robustos**: Django, FastAPI, Flask
- **Ideal para APIs**: JSON nativo, HTTP libraries

### **P: ¿Qué son las comprehensions en Python?**
```python
# List comprehension
numeros = [x**2 for x in range(10) if x % 2 == 0]

# Dict comprehension  
cuadrados = {x: x**2 for x in range(5)}

# Más eficiente que loops tradicionales
```

### **P: Explica la diferencia entre `==` y `is`**
```python
a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(a == b)  # True (mismo contenido)
print(a is b)  # False (diferentes objetos en memoria)
print(a is c)  # True (mismo objeto)
```

---

## 🚀 Preguntas de FastAPI

### **P: ¿Por qué FastAPI en lugar de Flask o Django?**
**R:** FastAPI es ideal porque:
- **Velocidad**: Uno de los frameworks más rápidos
- **Tipado automático**: Type hints de Python 3.6+
- **Documentación automática**: Swagger UI incluido
- **Validación automática**: Con Pydantic
- **Async nativo**: Soporte completo para programación asíncrona
- **Estándares modernos**: OpenAPI, JSON Schema

### **P: ¿Qué es Pydantic y para qué sirve?**
```python
from pydantic import BaseModel, EmailStr, validator

class Usuario(BaseModel):
    nombre: str
    email: EmailStr
    edad: int
    
    @validator('edad')
    def validar_edad(cls, v):
        if v < 0 or v > 120:
            raise ValueError('Edad inválida')
        return v

# Validación automática
usuario = Usuario(nombre="Juan", email="juan@email.com", edad=25)
```

### **P: ¿Cómo manejas errores en FastAPI?**
```python
from fastapi import HTTPException

@app.get("/usuarios/{user_id}")
def get_usuario(user_id: int):
    usuario = db.query(Usuario).filter(Usuario.id == user_id).first()
    if not usuario:
        raise HTTPException(
            status_code=404, 
            detail="Usuario no encontrado"
        )
    return usuario
```

---

## 🗄️ Preguntas de Base de Datos / SQL

### **P: ¿Qué es un ORM y cuáles son sus ventajas?**
**R:** ORM (Object-Relational Mapping) mapea objetos Python a tablas de BD:

**Ventajas:**
- **Abstracción**: No escribes SQL directo
- **Seguridad**: Previene SQL injection
- **Portabilidad**: Cambiar BD sin cambiar código
- **Mantenibilidad**: Código más limpio

```python
# Con ORM (SQLAlchemy)
usuarios = db.query(Usuario).filter(Usuario.activo == True).all()

# Equivale a SQL:
# SELECT * FROM usuarios WHERE activo = true;
```

### **P: Explica los tipos de JOIN en SQL**
```sql
-- INNER JOIN: Solo registros que coinciden en ambas tablas
SELECT u.nombre, p.titulo 
FROM usuarios u 
INNER JOIN pedidos p ON u.id = p.usuario_id;

-- LEFT JOIN: Todos los usuarios, con o sin pedidos
SELECT u.nombre, p.titulo 
FROM usuarios u 
LEFT JOIN pedidos p ON u.id = p.usuario_id;

-- RIGHT JOIN: Todos los pedidos, con o sin usuario
SELECT u.nombre, p.titulo 
FROM usuarios u 
RIGHT JOIN pedidos p ON u.id = p.usuario_id;
```

### **P: ¿Qué son las transacciones y por qué son importantes?**
```python
def transferir_dinero(origen_id, destino_id, monto):
    db = SessionLocal()
    try:
        # Inicio de transacción automática
        origen = db.query(Cuenta).filter(Cuenta.id == origen_id).first()
        destino = db.query(Cuenta).filter(Cuenta.id == destino_id).first()
        
        origen.saldo -= monto
        destino.saldo += monto
        
        db.commit()  # Confirmar cambios
    except Exception as e:
        db.rollback()  # Revertir si hay error
        raise e
    finally:
        db.close()
```

---

## 🏗️ Preguntas de Arquitectura

### **P: ¿Qué es REST y cuáles son sus principios?**
**R:** REST (Representational State Transfer) es un estilo arquitectónico:

**Principios:**
- **Stateless**: Sin estado entre requests
- **Client-Server**: Separación de responsabilidades
- **Cacheable**: Respuestas pueden ser cacheadas
- **Uniform Interface**: URLs y métodos HTTP estándar

```python
# Ejemplos RESTful
GET    /usuarios        # Listar usuarios
GET    /usuarios/123    # Obtener usuario específico
POST   /usuarios        # Crear usuario
PUT    /usuarios/123    # Actualizar usuario completo
PATCH  /usuarios/123    # Actualizar usuario parcial
DELETE /usuarios/123    # Eliminar usuario
```

### **P: ¿Cómo estructurarías un proyecto FastAPI grande?**
```
proyecto/
├── app/
│   ├── __init__.py
│   ├── main.py              # Aplicación principal
│   ├── models/              # Modelos de BD
│   │   ├── __init__.py
│   │   └── usuario.py
│   ├── schemas/             # Modelos Pydantic
│   │   ├── __init__.py
│   │   └── usuario.py
│   ├── routers/             # Endpoints por módulo
│   │   ├── __init__.py
│   │   ├── usuarios.py
│   │   └── reportes.py
│   ├── database.py          # Configuración BD
│   ├── dependencies.py      # Dependencias compartidas
│   └── utils.py            # Utilidades
├── tests/                   # Tests unitarios
├── requirements.txt
└── README.md
```

---

## 💼 Preguntas específicas para Procobro

### **P: ¿Cómo harías extracción de información de BD para reportes?**
```python
@app.get("/reportes/cobranzas")
def reporte_cobranzas(fecha_desde: str, fecha_hasta: str):
    query = text("""
        SELECT 
            DATE(c.fecha_cobro) as fecha,
            COUNT(*) as total_cobranzas,
            SUM(c.monto) as monto_total,
            AVG(c.monto) as monto_promedio
        FROM cobranzas c 
        WHERE c.fecha_cobro BETWEEN :fecha_desde AND :fecha_hasta
        GROUP BY DATE(c.fecha_cobro)
        ORDER BY fecha DESC
    """)
    
    resultado = db.execute(query, {
        "fecha_desde": fecha_desde,
        "fecha_hasta": fecha_hasta
    })
    
    return [dict(row) for row in resultado]
```

### **P: ¿Cómo implementarías carga masiva de datos?**
```python
@app.post("/carga-masiva/clientes")
async def carga_masiva_clientes(archivo: UploadFile = File(...)):
    if not archivo.filename.endswith('.csv'):
        raise HTTPException(400, "Solo archivos CSV")
    
    contenido = await archivo.read()
    csv_data = csv.DictReader(io.StringIO(contenido.decode('utf-8')))
    
    clientes_creados = []
    errores = []
    
    for index, fila in enumerate(csv_data, 1):
        try:
            cliente = ClienteORM(**fila)
            db.add(cliente)
            clientes_creados.append(cliente.id)
        except Exception as e:
            errores.append(f"Fila {index}: {str(e)}")
    
    if not errores:
        db.commit()
        return {"exito": True, "creados": len(clientes_creados)}
    else:
        db.rollback()
        return {"exito": False, "errores": errores}
```

### **P: ¿Cómo reportarías incidencias automáticamente?**
```python
import logging
from datetime import datetime

def reportar_incidencia(tipo, mensaje, critica=False):
    incidencia = {
        "timestamp": datetime.now().isoformat(),
        "tipo": tipo,
        "mensaje": mensaje,
        "nivel": "CRITICA" if critica else "NORMAL"
    }
    
    # Log local
    if critica:
        logger.critical(f"🚨 INCIDENCIA CRÍTICA: {incidencia}")
    else:
        logger.warning(f"⚠️ Incidencia: {incidencia}")
    
    # Enviar notificación si es crítica
    if critica:
        enviar_alerta_slack(incidencia)
        enviar_email_urgente(incidencia)
    
    return incidencia

# Uso en endpoints
@app.get("/procesos/criticos")
def proceso_critico():
    try:
        resultado = ejecutar_proceso_importante()
        return resultado
    except Exception as e:
        reportar_incidencia(
            "PROCESO_CRITICO_FALLO", 
            f"Error en proceso crítico: {str(e)}", 
            critica=True
        )
        raise HTTPException(500, "Error crítico del sistema")
```

---

## 🚀 Preguntas avanzadas

### **P: ¿Qué es async/await y cuándo lo usarías?**
```python
import asyncio
import aiohttp

# Función síncrona (bloquea)
def consultar_api_sincrono():
    response = requests.get("https://api.ejemplo.com/datos")
    return response.json()

# Función asíncrona (no bloquea)
async def consultar_api_async():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.ejemplo.com/datos") as response:
            return await response.json()

# Endpoint asíncrono en FastAPI
@app.get("/datos-externos")
async def obtener_datos_externos():
    # Puede manejar múltiples requests simultáneamente
    datos = await consultar_api_async()
    return datos
```

### **P: ¿Cómo optimizarías consultas de BD lentas?**
```python
# 1. Usar índices
class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True)
    email = Column(String, index=True)  # Índice para búsquedas rápidas
    
# 2. Paginación
@app.get("/usuarios")
def listar_usuarios(skip: int = 0, limit: int = 100):
    return db.query(Usuario).offset(skip).limit(limit).all()

# 3. Carga específica (evitar SELECT *)
def obtener_usuarios_basico():
    return db.query(Usuario.id, Usuario.nombre).all()

# 4. Joins eficientes
def usuarios_con_pedidos():
    return db.query(Usuario).join(Pedido).all()
```

---

## 💡 Consejos para la entrevista

### **Durante la entrevista técnica:**
1. **Explica tu razonamiento** mientras codificas
2. **Pregunta sobre requisitos** antes de empezar
3. **Considera casos edge** (errores, datos vacíos)
4. **Habla de performance** y escalabilidad
5. **Menciona testing** y documentación

### **Frases clave que impresionan:**
- "Implementaríamos logging para monitorear esto"
- "Consideraría añadir validación para casos edge"
- "Esto se podría optimizar con caching"
- "Sería importante añadir tests unitarios"
- "Para producción, añadiría autenticación"

### **Proyectos que demuestran experiencia:**
- ✅ **Este CRUD**: Muestra conocimiento de FastAPI, BD, APIs
- ✅ **Script de reportes**: Demuestra habilidades de extracción de datos
- ✅ **Sistema de logging**: Muestra consciencia de monitoreo
- ✅ **Validaciones robustas**: Indica pensamiento empresarial

¡Con esta preparación estarás listo para impresionar en Procobro! 🚀💼
