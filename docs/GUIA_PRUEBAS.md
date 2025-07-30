# 🧪 GUÍA DE PRUEBAS - FastAPI CRUD

## 🎯 Cómo probar tu API paso a paso

### 📋 Antes de empezar
1. Asegúrate de que el servidor esté ejecutándose:
   ```bash
   uvicorn main:app --reload
   ```
2. Deberías ver: `Uvicorn running on http://127.0.0.1:8000`

---

## 🌐 MÉTODO 1: Swagger UI (Recomendado para principiantes)

### 1. Abrir la documentación
- Ve a: http://127.0.0.1:8000/docs
- Verás una interfaz bonita con todos tus endpoints

### 2. Probar GET /usuarios (Listar usuarios)
1. Haz clic en **"GET /usuarios"**
2. Clic en **"Try it out"**
3. Clic en **"Execute"**
4. Verás la respuesta abajo

### 3. Probar POST /usuarios (Crear usuario)
1. Haz clic en **"POST /usuarios"**
2. Clic en **"Try it out"**
3. En el campo de texto, reemplaza con:
   ```json
   {
     "id": 1,
     "nombre": "Ana López",
     "email": "ana@email.com"
   }
   ```
4. Clic en **"Execute"**
5. ¡Verás que se creó el usuario!

### 4. Probar DELETE /usuarios/{usuario_id}
1. Haz clic en **"DELETE /usuarios/{usuario_id}"**
2. Clic en **"Try it out"**
3. En **usuario_id** escribe: `1`
4. Clic en **"Execute"**

---

## 💻 MÉTODO 2: PowerShell (Para Windows)

### 1. Listar usuarios
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/usuarios" -Method GET
```

### 2. Crear usuario
```powershell
$usuario = @{
    id = 3
    nombre = "Carlos Ruiz"
    email = "carlos@email.com"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/usuarios" -Method POST -Body $usuario -ContentType "application/json"
```

### 3. Eliminar usuario
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/usuarios/3" -Method DELETE
```

---

## 🔧 MÉTODO 3: Usando Python

Crea un archivo `test_api.py`:

```python
import requests

# URL base de tu API
BASE_URL = "http://127.0.0.1:8000"

# 1. Listar usuarios
def listar_usuarios():
    response = requests.get(f"{BASE_URL}/usuarios")
    print("📋 Usuarios:", response.json())

# 2. Crear usuario
def crear_usuario(id, nombre, email):
    usuario = {
        "id": id,
        "nombre": nombre,
        "email": email
    }
    response = requests.post(f"{BASE_URL}/usuarios", json=usuario)
    print("✅ Usuario creado:", response.json())

# 3. Eliminar usuario
def eliminar_usuario(id):
    response = requests.delete(f"{BASE_URL}/usuarios/{id}")
    print("🗑️ Resultado:", response.json())

# Ejecutar pruebas
if __name__ == "__main__":
    print("🚀 Probando API...")
    
    # Listar usuarios (inicialmente vacío)
    listar_usuarios()
    
    # Crear algunos usuarios
    crear_usuario(1, "Pedro García", "pedro@email.com")
    crear_usuario(2, "Laura Martín", "laura@email.com")
    
    # Listar usuarios (ahora con datos)
    listar_usuarios()
    
    # Eliminar un usuario
    eliminar_usuario(1)
    
    # Listar usuarios finales
    listar_usuarios()
```

Para ejecutar:
```bash
pip install requests
python test_api.py
```

---

## 🎭 MÉTODO 4: Ejemplos con diferentes escenarios

### ✅ Escenario 1: Flujo normal
```json
# 1. Crear usuario
POST /usuarios
{
  "id": 1,
  "nombre": "María José",
  "email": "maria@email.com"
}

# 2. Listar para verificar
GET /usuarios
# Respuesta: [{"id": 1, "nombre": "María José", "email": "maria@email.com"}]

# 3. Eliminar
DELETE /usuarios/1
# Respuesta: {"mensaje": "Eliminado"}
```

### ❌ Escenario 2: Errores comunes
```json
# 1. Intentar eliminar usuario que no existe
DELETE /usuarios/999
# Respuesta: {"detail": "No encontrado"} (Error 404)

# 2. Crear usuario con datos inválidos
POST /usuarios
{
  "id": "texto",  # ❌ Debería ser número
  "nombre": 123,  # ❌ Debería ser texto
  "email": null   # ❌ Debería ser texto
}
# Respuesta: Error de validación 422
```

---

## 📊 RESULTADOS ESPERADOS

### Cuando todo va bien:
```json
# GET /usuarios (con datos)
[
  {
    "id": 1,
    "nombre": "Ana López",
    "email": "ana@email.com"
  },
  {
    "id": 2,
    "nombre": "Pedro García", 
    "email": "pedro@email.com"
  }
]

# POST /usuarios (crear)
{
  "id": 3,
  "nombre": "Laura Ruiz",
  "email": "laura@email.com"
}

# DELETE /usuarios/3 (eliminar)
{
  "mensaje": "Eliminado"
}
```

### Cuando hay errores:
```json
# Usuario no encontrado (404)
{
  "detail": "No encontrado"
}

# Datos inválidos (422)
{
  "detail": [
    {
      "loc": ["body", "id"],
      "msg": "value is not a valid integer",
      "type": "type_error.integer"
    }
  ]
}
```

---

## 🔍 VERIFICAR QUE FUNCIONA

### ✅ Checklist de pruebas:
- [ ] El servidor inicia sin errores
- [ ] GET /usuarios devuelve lista (vacía o con datos)
- [ ] POST /usuarios crea un usuario nuevo
- [ ] DELETE /usuarios/{id} elimina un usuario existente
- [ ] DELETE con ID inexistente devuelve 404
- [ ] POST con datos inválidos devuelve 422
- [ ] La documentación en /docs funciona

### 🎯 Comandos rápidos para probar todo:
```powershell
# 1. Verificar que está vacío
Invoke-RestMethod -Uri "http://127.0.0.1:8000/usuarios" -Method GET

# 2. Crear usuario de prueba
$test = @{id=99; nombre="Test User"; email="test@test.com"} | ConvertTo-Json
Invoke-RestMethod -Uri "http://127.0.0.1:8000/usuarios" -Method POST -Body $test -ContentType "application/json"

# 3. Verificar que se creó
Invoke-RestMethod -Uri "http://127.0.0.1:8000/usuarios" -Method GET

# 4. Eliminar usuario de prueba
Invoke-RestMethod -Uri "http://127.0.0.1:8000/usuarios/99" -Method DELETE
```

---

## 🚀 ¡Listo para GitHub!

Tu proyecto ya está completo con:
- ✅ Código funcional
- ✅ Documentación detallada  
- ✅ Ejemplos de uso
- ✅ Guía de pruebas
- ✅ README profesional

¡Perfecto para mostrar en tu portafolio! 🎉
