#!/usr/bin/env python3
"""
Script de instalación para el Sistema de Gestión MYPYME
Verifica e instala las dependencias necesarias
"""

import sys
import subprocess
import os

def check_python_version():
    """Verificar versión de Python"""
    if sys.version_info < (3, 7):
        print("❌ Error: Se requiere Python 3.7 o superior")
        print(f"   Versión actual: {sys.version}")
        return False
    else:
        print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detectado")
        return True

def check_tkinter():
    """Verificar si tkinter está disponible"""
    try:
        import tkinter
        print("✅ tkinter disponible")
        return True
    except ImportError:
        print("❌ Error: tkinter no está disponible")
        print("   En Windows, reinstala Python con tkinter habilitado")
        print("   En Linux: sudo apt-get install python3-tk")
        print("   En macOS: brew install python-tk")
        return False

def install_requirements():
    """Instalar dependencias desde requirements.txt"""
    try:
        print("📦 Instalando dependencias...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencias instaladas correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al instalar dependencias: {e}")
        return False
    except FileNotFoundError:
        print("❌ Error: requirements.txt no encontrado")
        return False

def test_imports():
    """Probar que todas las dependencias se pueden importar"""
    required_modules = [
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'sqlite3',
        'datetime',
        'reportlab',
        'PIL'
    ]
    
    print("🔍 Verificando importaciones...")
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            return False
    return True

def create_directories():
    """Crear directorios necesarios"""
    directories = ['reports', 'backups']
    
    print("📁 Creando directorios...")
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Creado directorio: {directory}")
        else:
            print(f"✅ Directorio ya existe: {directory}")

def main():
    """Función principal de instalación"""
    print("🚀 Instalador del Sistema de Gestión MYPYME")
    print("=" * 50)
    
    # Verificar Python
    if not check_python_version():
        sys.exit(1)
    
    # Verificar tkinter
    if not check_tkinter():
        sys.exit(1)
    
    # Instalar dependencias
    if not install_requirements():
        sys.exit(1)
    
    # Probar importaciones
    if not test_imports():
        print("❌ Algunas dependencias no se pueden importar")
        print("   Intenta reinstalar las dependencias manualmente:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    
    # Crear directorios
    create_directories()
    
    print("\n" + "=" * 50)
    print("✅ Instalación completada exitosamente!")
    print("\n📋 Para ejecutar la aplicación:")
    print("   python main.py")
    print("\n📖 Para más información, consulta README.md")
    print("=" * 50)

if __name__ == "__main__":
    main() 