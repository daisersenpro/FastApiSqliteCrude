#!/usr/bin/env python3
"""
🧪 Script de pruebas rápidas para la API FastAPI
Ejecuta: python test_api.py
"""

import requests
import json
import sys

# Configuración
BASE_URL = "http://127.0.0.1:8000"

def verificar_servidor():
    """Verifica si el servidor está ejecutándose"""
    try:
        response = requests.get(f"{BASE_URL}/usuarios")
        return True
    except requests.exceptions.ConnectionError:
        print("❌ Error: El servidor no está ejecutándose")
        print("💡 Ejecuta: uvicorn main:app --reload")
        return False

def listar_usuarios():
    """Lista todos los usuarios"""
    try:
        response = requests.get(f"{BASE_URL}/usuarios")
        usuarios = response.json()
        print(f"📋 Usuarios encontrados: {len(usuarios)}")
        for usuario in usuarios:
            print(f"   👤 ID: {usuario['id']}, Nombre: {usuario['nombre']}, Email: {usuario['email']}")
        return usuarios
    except Exception as e:
        print(f"❌ Error al listar usuarios: {e}")
        return []

def crear_usuario(id, nombre, email):
    """Crea un nuevo usuario"""
    usuario_data = {
        "id": id,
        "nombre": nombre,
        "email": email
    }
    
    try:
        response = requests.post(f"{BASE_URL}/usuarios", json=usuario_data)
        if response.status_code == 200:
            usuario = response.json()
            print(f"✅ Usuario creado: {usuario['nombre']} ({usuario['email']})")
            return usuario
        else:
            print(f"❌ Error al crear usuario: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error al crear usuario: {e}")
        return None

def eliminar_usuario(id):
    """Elimina un usuario por ID"""
    try:
        response = requests.delete(f"{BASE_URL}/usuarios/{id}")
        if response.status_code == 200:
            resultado = response.json()
            print(f"🗑️ Usuario {id} eliminado: {resultado['mensaje']}")
            return True
        elif response.status_code == 404:
            print(f"❌ Usuario {id} no encontrado")
            return False
        else:
            print(f"❌ Error al eliminar usuario: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error al eliminar usuario: {e}")
        return False

def menu_principal():
    """Menú interactivo principal"""
    while True:
        print("\n" + "="*50)
        print("🚀 FASTAPI CRUD - MENÚ DE PRUEBAS")
        print("="*50)
        print("1. 📋 Listar todos los usuarios")
        print("2. ➕ Crear usuario nuevo")
        print("3. 🗑️ Eliminar usuario")
        print("4. 🧪 Ejecutar prueba completa")
        print("5. 🚪 Salir")
        print("="*50)
        
        opcion = input("Selecciona una opción (1-5): ").strip()
        
        if opcion == "1":
            print("\n📋 LISTANDO USUARIOS...")
            listar_usuarios()
            
        elif opcion == "2":
            print("\n➕ CREAR NUEVO USUARIO")
            try:
                id = int(input("ID del usuario: "))
                nombre = input("Nombre: ")
                email = input("Email: ")
                crear_usuario(id, nombre, email)
            except ValueError:
                print("❌ Error: El ID debe ser un número")
                
        elif opcion == "3":
            print("\n🗑️ ELIMINAR USUARIO")
            try:
                id = int(input("ID del usuario a eliminar: "))
                eliminar_usuario(id)
            except ValueError:
                print("❌ Error: El ID debe ser un número")
                
        elif opcion == "4":
            print("\n🧪 EJECUTANDO PRUEBA COMPLETA...")
            ejecutar_prueba_completa()
            
        elif opcion == "5":
            print("\n👋 ¡Hasta luego!")
            break
            
        else:
            print("❌ Opción inválida. Intenta de nuevo.")

def ejecutar_prueba_completa():
    """Ejecuta una prueba completa del CRUD"""
    print("\n🚀 Iniciando prueba completa del CRUD...")
    
    # 1. Verificar estado inicial
    print("\n1️⃣ Verificando estado inicial...")
    usuarios_iniciales = listar_usuarios()
    
    # 2. Crear usuarios de prueba
    print("\n2️⃣ Creando usuarios de prueba...")
    usuarios_prueba = [
        (101, "Test Usuario 1", "test1@ejemplo.com"),
        (102, "Test Usuario 2", "test2@ejemplo.com"),
        (103, "Test Usuario 3", "test3@ejemplo.com")
    ]
    
    for id, nombre, email in usuarios_prueba:
        crear_usuario(id, nombre, email)
    
    # 3. Listar usuarios después de crear
    print("\n3️⃣ Verificando usuarios después de crear...")
    listar_usuarios()
    
    # 4. Eliminar usuarios de prueba
    print("\n4️⃣ Eliminando usuarios de prueba...")
    for id, _, _ in usuarios_prueba:
        eliminar_usuario(id)
    
    # 5. Verificar estado final
    print("\n5️⃣ Verificando estado final...")
    listar_usuarios()
    
    print("\n✅ ¡Prueba completa finalizada!")

def main():
    """Función principal"""
    print("🚀 Iniciando script de pruebas para FastAPI CRUD")
    
    # Verificar que el servidor esté ejecutándose
    if not verificar_servidor():
        sys.exit(1)
    
    print("✅ Servidor FastAPI detectado correctamente")
    
    # Verificar si hay argumentos de línea de comandos
    if len(sys.argv) > 1:
        comando = sys.argv[1].lower()
        
        if comando == "test":
            ejecutar_prueba_completa()
        elif comando == "list":
            listar_usuarios()
        else:
            print(f"❌ Comando desconocido: {comando}")
            print("💡 Comandos disponibles: test, list")
    else:
        # Mostrar menú interactivo
        menu_principal()

if __name__ == "__main__":
    main()
