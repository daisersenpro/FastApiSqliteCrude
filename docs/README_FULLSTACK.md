# 🚀 FastAPI + React Full Stack CRUD

**Proyecto integrado**: Backend FastAPI + Frontend React en un solo servidor

## 🎯 **¿Qué hace este proyecto?**

- ✅ **Backend**: API REST con FastAPI y Python
- ✅ **Frontend**: Interfaz React moderna y responsive
- ✅ **Base de datos**: SQLite con SQLAlchemy ORM
- ✅ **Todo integrado**: Un solo servidor para todo
- ✅ **Listo para producción**: Configuración profesional

## 🏗️ **Arquitectura**

```
FastAPI Server (Puerto 8000)
├── /                    → React App (Frontend)
├── /api/               → API REST (Backend)
│   ├── /usuarios       → CRUD de usuarios
│   ├── /estadisticas   → Reportes
│   └── /docs          → Documentación
└── /static/           → Archivos React compilados
```

## 🚀 **Instalación y ejecución**

### **1. Preparar entorno:**
```bash
cd "c:\Users\anyelo\Desktop\fastapi_sqlite_crud"
.\venv\Scripts\activate
pip install fastapi uvicorn sqlalchemy pydantic[email] python-multipart
```

### **2. Ejecutar servidor:**
```bash
uvicorn main_react:app --reload
```

### **3. Abrir aplicación:**
- 🌐 **App completa**: http://127.0.0.1:8000
- 📖 **API docs**: http://127.0.0.1:8000/api/docs
- 🔧 **API status**: http://127.0.0.1:8000/api/

## 🎨 **Características del Frontend**

### **Dashboard con estadísticas:**
- 📊 Total de usuarios
- ✅ Usuarios activos
- 📅 Usuarios creados hoy

### **Gestión de usuarios:**
- ➕ Crear usuarios con validación
- 👥 Lista visual de todos los usuarios
- 🗑️ Eliminar usuarios con confirmación
- 🔄 Actualización automática

### **Diseño moderno:**
- 📱 Responsive (mobile-friendly)
- 🎨 Gradientes y animaciones
- 🖱️ Hover effects
- 📋 Formularios intuitivos

## 🛠️ **Funcionalidades técnicas**

### **Backend (FastAPI):**
- 🔒 CORS configurado para desarrollo
- 📋 Validación con Pydantic
- 🗄️ ORM con SQLAlchemy
- 📊 Endpoints de estadísticas
- 🚨 Manejo robusto de errores
- 📖 Documentación automática

### **Frontend (React):**
- ⚛️ React 18 con Hooks
- 🔄 Estado global con useState
- 🌐 Fetch API para HTTP requests
- 🎨 CSS moderno con Grid y Flexbox
- 📱 Diseño responsive
- 🚫 Manejo de errores UI

## 📁 **Estructura de archivos**

```
fastapi_sqlite_crud/
├── main_react.py           # 🚀 Servidor principal
├── static/
│   └── index.html         # ⚛️ React App
├── main.py                # 📄 Versión básica
├── README.md              # 📖 Documentación
├── requirements.txt       # 📦 Dependencias
├── usuarios.db            # 🗄️ Base de datos
└── venv/                  # 🐍 Entorno virtual
```

## 🎯 **Para Procobro - Funcionalidades empresariales**

### **✅ Lo que demuestra:**
- **Python + FastAPI**: Backend robusto
- **JavaScript + React**: Frontend moderno
- **SQL**: Manejo de base de datos
- **APIs REST**: Integración entre sistemas
- **Full Stack**: Conocimiento completo

### **✅ Casos de uso empresariales:**
- **Gestión de clientes/usuarios**
- **Reportes en tiempo real**
- **Interfaces web modernas**
- **Integración frontend-backend**
- **Validación de datos**

## 🧪 **Cómo probar**

### **1. Probar la interfaz:**
- Ve a http://127.0.0.1:8000
- Crea algunos usuarios
- Observa las estadísticas en tiempo real
- Elimina usuarios y ve los cambios

### **2. Probar la API directamente:**
- Ve a http://127.0.0.1:8000/api/docs
- Usa la documentación interactiva
- Prueba todos los endpoints

### **3. Verificar integración:**
- Los cambios en la interfaz se reflejan en la API
- Las estadísticas se actualizan automáticamente
- Los errores se manejan elegantemente

## 🔧 **Personalización**

### **Cambiar estilos:**
Edita `static/index.html` en la sección `<style>`

### **Añadir funcionalidades:**
- Modifica `main_react.py` para nuevos endpoints
- Actualiza el JavaScript en `index.html`

### **Base de datos:**
- SQLite se crea automáticamente
- Ubicación: `usuarios.db`

## 🚀 **Deploy en producción**

### **Para servidor:**
```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar con Gunicorn
pip install gunicorn
gunicorn main_react:app -w 4 -k uvicorn.workers.UvicornWorker
```

### **Variables de entorno:**
```bash
# Opcional: configurar puerto
export PORT=8000
```

## 💡 **Ventajas de esta arquitectura**

### **✅ Pros:**
- **Un solo servidor** - Fácil deployment
- **Sin CORS issues** - Todo en el mismo dominio
- **Rápido desarrollo** - Cambios inmediatos
- **Fácil mantenimiento** - Todo en un lugar

### **⚠️ Consideraciones:**
- Para equipos grandes, separar frontend/backend
- Para CDN, compilar React por separado
- Para microservicios, dividir la aplicación

## 🎓 **Para la entrevista**

### **Puntos a destacar:**
- **"Integré FastAPI con React en un solo servidor"**
- **"Configuré CORS y manejo de rutas SPA"**
- **"Implementé un CRUD completo con interfaz moderna"**
- **"Separé lógica de negocio (API) de presentación (React)"**
- **"Usé validaciones tanto en frontend como backend"**

¡Proyecto completo y profesional listo para impresionar! 🚀✨
