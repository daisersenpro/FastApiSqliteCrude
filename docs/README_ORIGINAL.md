# 🚀 FastAPI SQLite CRUD

Un proyecto simple de **CRUD** (Create, Read, Update, Delete) usando **FastAPI**, **SQLAlchemy** y **SQLite** para gestionar usuarios.

## 📋 Características

- ✅ **FastAPI**: Framework web moderno y rápido para Python
- ✅ **SQLAlchemy**: ORM para manejo de base de datos
- ✅ **SQLite**: Base de datos ligera
- ✅ **Pydantic**: Validación de datos
- ✅ **Documentación automática**: Swagger UI incluida
- ✅ **API REST**: Endpoints estándar

## 🛠️ Tecnologías utilizadas

- **Python 3.x**
- **FastAPI**: Framework web
- **Uvicorn**: Servidor ASGI
- **SQLAlchemy**: ORM
- **Pydantic**: Validación de datos
- **SQLite**: Base de datos

## 📁 Estructura del proyecto

```
fastapi_sqlite_crud/
├── venv/                 # Entorno virtual
├── main.py              # Aplicación principal
├── requirements.txt     # Dependencias
├── usuarios.db          # Base de datos SQLite (se crea automáticamente)
└── README.md           # Este archivo
```

## 🚀 Instalación y configuración

### 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd fastapi_sqlite_crud
```

### 2. Crear entorno virtual
```bash
python -m venv venv
```

### 3. Activar entorno virtual

**Windows:**
```bash
.\venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 5. Ejecutar la aplicación
```bash
uvicorn main:app --reload
```

## 🌐 Endpoints de la API

### Base URL: `http://127.0.0.1:8000`

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/usuarios` | Obtener todos los usuarios |
| POST | `/usuarios` | Crear un nuevo usuario |
| DELETE | `/usuarios/{usuario_id}` | Eliminar un usuario por ID |

## 📖 Documentación interactiva

Una vez que el servidor esté ejecutándose, puedes acceder a:

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## 🧪 Ejemplos de uso

### 1. Listar todos los usuarios
```bash
GET http://127.0.0.1:8000/usuarios
```

**Respuesta:**
```json
[
  {
    "id": 1,
    "nombre": "Juan Pérez",
    "email": "juan@ejemplo.com"
  }
]
```

### 2. Crear un nuevo usuario
```bash
POST http://127.0.0.1:8000/usuarios
Content-Type: application/json

{
  "id": 2,
  "nombre": "María García",
  "email": "maria@ejemplo.com"
}
```

**Respuesta:**
```json
{
  "id": 2,
  "nombre": "María García",
  "email": "maria@ejemplo.com"
}
```

### 3. Eliminar un usuario
```bash
DELETE http://127.0.0.1:8000/usuarios/1
```

**Respuesta:**
```json
{
  "mensaje": "Eliminado"
}
```

## 🏗️ Arquitectura del código

### Modelo de datos (SQLAlchemy ORM)
```python
class UsuarioORM(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    email = Column(String)
```

### Modelo de validación (Pydantic)
```python
class Usuario(BaseModel):
    id: int
    nombre: str
    email: str
    class Config:
        orm_mode = True
```

### Configuración de base de datos
- **Motor**: SQLite
- **Archivo**: `usuarios.db`
- **ORM**: SQLAlchemy
- **Sesiones**: SessionLocal

## 🔧 Funcionalidades

### ✅ Listar usuarios (`GET /usuarios`)
- Obtiene todos los usuarios de la base de datos
- Retorna una lista JSON con todos los registros

### ✅ Crear usuario (`POST /usuarios`)
- Crea un nuevo usuario en la base de datos
- Requiere: `id`, `nombre`, `email`
- Valida los datos usando Pydantic

### ✅ Eliminar usuario (`DELETE /usuarios/{usuario_id}`)
- Elimina un usuario por su ID
- Retorna error 404 si no existe
- Confirma eliminación con mensaje

## 🚨 Manejo de errores

- **404 Not Found**: Usuario no encontrado
- **422 Validation Error**: Datos inválidos
- **500 Internal Server Error**: Error del servidor

## 📝 Notas importantes

1. **Base de datos**: Se crea automáticamente al ejecutar la aplicación
2. **Entorno virtual**: Siempre activar antes de trabajar
3. **Recarga automática**: `--reload` reinicia al detectar cambios
4. **Validación**: Pydantic valida automáticamente los datos

## 🔮 Mejoras futuras

- [ ] Añadir endpoint PUT para actualizar usuarios
- [ ] Implementar paginación
- [ ] Añadir autenticación
- [ ] Validaciones más robustas
- [ ] Tests unitarios
- [ ] Docker support

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Añadir nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la licencia MIT.

## 📧 Contacto

Si tienes preguntas o sugerencias, no dudes en contactarme.

---

**¡Disfruta desarrollando con FastAPI!** 🐍⚡
