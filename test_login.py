#!/usr/bin/env python3
"""
Script de prueba para verificar el login y la pestaña de usuarios
"""

import tkinter as tk
from database import Database
from login import LoginWindow

def test_login():
    """Probar el sistema de login"""
    root = tk.Tk()
    root.withdraw()  # Ocultar ventana principal
    
    print("Probando sistema de login...")
    
    # Crear ventana de login
    login = LoginWindow(root)
    root.wait_window(login.login_window)
    
    # Verificar si el usuario se autenticó
    usuario_actual = login.get_usuario_actual()
    
    if usuario_actual:
        print(f"✅ Login exitoso!")
        print(f"Usuario: {usuario_actual['nombre_completo']}")
        print(f"Rol: {usuario_actual['rol']}")
        
        # Verificar que sea admin
        if usuario_actual['rol'] == 'admin':
            print("✅ Usuario es administrador - debería ver la pestaña de usuarios")
        else:
            print("❌ Usuario no es administrador")
    else:
        print("❌ Login falló")
    
    root.destroy()

def test_database():
    """Probar la base de datos"""
    print("\nProbando base de datos...")
    
    db = Database()
    
    # Verificar usuarios
    usuarios = db.obtener_usuarios()
    print(f"Usuarios en la base de datos: {len(usuarios)}")
    
    for usuario in usuarios:
        id_user, username, nombre, rol, activo, fecha = usuario
        estado = "Activo" if activo else "Inactivo"
        print(f"  - {username} ({nombre}) - Rol: {rol} - Estado: {estado}")
    
    # Verificar autenticación
    usuario = db.autenticar_usuario("admin", "admin123")
    if usuario:
        print("✅ Autenticación de admin exitosa")
    else:
        print("❌ Autenticación de admin falló")

if __name__ == "__main__":
    print("=== PRUEBA DEL SISTEMA MYPYME ===\n")
    
    test_database()
    test_login()
    
    print("\n=== FIN DE PRUEBAS ===") 