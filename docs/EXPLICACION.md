# 📚 EXPLICACIÓN DETALLADA DEL CÓDIGO

## 🎯 ¿Qué hace este proyecto?

Este es un **CRUD** (Create, Read, Update, Delete) que permite:
- **Crear** usuarios nuevos
- **Leer** (listar) todos los usuarios  
- **Eliminar** usuarios por ID

### 🏢 Aplicación empresarial
Este proyecto demuestra habilidades clave para desarrollo Full Stack:
- **Backend**: API REST con FastAPI y Python
- **Base de datos**: SQLAlchemy ORM con SQLite
- **Validación**: Pydantic para validación de datos
- **Documentación**: Swagger UI automática
- **Arquitectura**: Separación de responsabilidades (ORM, API, validación)

---

## 🧩 PARTE 1: IMPORTACIONES

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
```

**¿Qué hace cada una?**
- `FastAPI`: El framework principal para crear la API
- `HTTPException`: Para manejar errores HTTP (como 404)
- `BaseModel`: Para validar los datos que llegan
- `SQLAlchemy`: Para trabajar con la base de datos de forma fácil

---

## 🗄️ PARTE 2: CONFIGURACIÓN DE BASE DE DATOS

```python
DATABASE_URL = "sqlite:///./usuarios.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()
```

**¿Qué significa esto?**
- `DATABASE_URL`: La dirección de nuestra base de datos (archivo usuarios.db)
- `engine`: El "motor" que conecta Python con SQLite
- `SessionLocal`: Una "fábrica" de sesiones para hablar con la BD
- `Base`: La clase base para crear nuestros modelos

---

## 🏗️ PARTE 3: MODELO DE LA BASE DE DATOS (ORM)

```python
class UsuarioORM(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    email = Column(String)
```

**¿Qué es esto?**
- `UsuarioORM`: Representa la tabla "usuarios" en la base de datos
- `__tablename__`: El nombre real de la tabla en SQLite
- `Column`: Define cada columna de la tabla
- `primary_key=True`: El ID es la clave principal (único)

---

## ✅ PARTE 4: CREAR LAS TABLAS

```python
Base.metadata.create_all(bind=engine)
```

**¿Qué hace?**
- Si no existe la tabla "usuarios", la crea automáticamente
- Es como ejecutar: `CREATE TABLE usuarios (id, nombre, email)`

---

## 📋 PARTE 5: MODELO DE VALIDACIÓN (Pydantic)

```python
class Usuario(BaseModel):
    id: int
    nombre: str
    email: str
    class Config:
        orm_mode = True
```

**¿Para qué sirve?**
- Valida que los datos que llegan sean correctos
- `id: int`: El ID debe ser un número entero
- `nombre: str`: El nombre debe ser texto
- `orm_mode = True`: Permite convertir objetos de BD a JSON

---

## 🚀 PARTE 6: CREAR LA APLICACIÓN

```python
app = FastAPI()
```

**¿Qué es?**
- Crea la aplicación FastAPI
- Es como encender el servidor web

---

## 🛣️ PARTE 7: LOS ENDPOINTS (RUTAS)

### 📖 LISTAR USUARIOS - GET /usuarios

```python
@app.get("/usuarios")
def listar_usuarios():
    db = SessionLocal()          # Abre conexión a BD
    datos = db.query(UsuarioORM).all()  # Busca TODOS los usuarios
    db.close()                   # Cierra conexión
    return datos                 # Devuelve la lista
```

**¿Cómo funciona?**
1. Alguien visita: `GET http://127.0.0.1:8000/usuarios`
2. Se abre una conexión a la base de datos
3. Se buscan TODOS los usuarios
4. Se cierra la conexión
5. Se devuelve la lista en formato JSON

### ➕ CREAR USUARIO - POST /usuarios

```python
@app.post("/usuarios")
def crear_usuario(usuario: Usuario):
    db = SessionLocal()          # Abre conexión
    nuevo = UsuarioORM(          # Crea nuevo usuario
        id=usuario.id, 
        nombre=usuario.nombre, 
        email=usuario.email
    )
    db.add(nuevo)               # Añade a la BD
    db.commit()                 # Guarda cambios
    db.refresh(nuevo)           # Actualiza el objeto
    db.close()                  # Cierra conexión
    return nuevo                # Devuelve el usuario creado
```

**¿Cómo funciona?**
1. Alguien envía: `POST http://127.0.0.1:8000/usuarios` con datos JSON
2. Pydantic valida que los datos sean correctos
3. Se crea un nuevo registro en la base de datos
4. Se guarda permanentemente
5. Se devuelve el usuario creado

### 🗑️ ELIMINAR USUARIO - DELETE /usuarios/{usuario_id}

```python
@app.delete("/usuarios/{usuario_id}")
def eliminar_usuario(usuario_id: int):
    db = SessionLocal()          # Abre conexión
    usuario = db.query(UsuarioORM).filter(
        UsuarioORM.id == usuario_id
    ).first()                    # Busca el usuario por ID
    
    if not usuario:              # Si no existe
        db.close()
        raise HTTPException(status_code=404, detail="No encontrado")
    
    db.delete(usuario)           # Elimina el usuario
    db.commit()                  # Guarda cambios
    db.close()                   # Cierra conexión
    return {"mensaje": "Eliminado"}
```

**¿Cómo funciona?**
1. Alguien envía: `DELETE http://127.0.0.1:8000/usuarios/1`
2. Se busca el usuario con ID = 1
3. Si no existe, devuelve error 404
4. Si existe, lo elimina de la base de datos
5. Devuelve confirmación

---

## 🔄 FLUJO GENERAL

1. **Cliente** → Envía petición HTTP
2. **FastAPI** → Recibe y valida la petición
3. **SQLAlchemy** → Se conecta a la base de datos
4. **SQLite** → Ejecuta la operación (leer/escribir/eliminar)
5. **FastAPI** → Devuelve respuesta en JSON
6. **Cliente** → Recibe la respuesta

---

## 💡 CONCEPTOS CLAVE

### 🔸 ORM (Object-Relational Mapping)
- Permite trabajar con la BD usando objetos Python
- En lugar de escribir SQL, usas métodos Python

### 🔸 API REST
- **GET**: Para obtener datos
- **POST**: Para crear datos nuevos
- **DELETE**: Para eliminar datos

### 🔸 JSON
- Formato estándar para intercambiar datos
- Fácil de leer para humanos y máquinas

### 🔸 Base de Datos
- **SQLite**: Base de datos en un archivo
- **Tabla**: Como una hoja de Excel
- **Registro**: Una fila en la tabla
- **Campo**: Una columna en la tabla

---

## 🎯 ¿Por qué usar FastAPI?

1. **Rápido**: Muy alta performance
2. **Fácil**: Sintaxis simple y clara
3. **Documentación automática**: Swagger UI gratis
4. **Validación**: Pydantic valida automáticamente
5. **Moderno**: Usa las últimas características de Python

---

## 🚀 ¿Cómo ejecutar?

```bash
# 1. Activar entorno virtual
.\venv\Scripts\activate

# 2. Ejecutar servidor
uvicorn main:app --reload

# 3. Abrir en navegador
http://127.0.0.1:8000/docs
```

¡Y listo! Tienes una API completamente funcional. 🎉
