# ========================================
# GENERADOR DE APK MYPYME - GOOGLE COLAB
# ========================================

import os
import subprocess
import time
from google.colab import files

def generar_apk_mypyme():
    print("🚀 GENERANDO APK MYPYME...")
    print("=" * 50)
    
    # Paso 1: Instalar dependencias
    print("\n📦 Instalando dependencias...")
    os.system("pip install buildozer")
    os.system("pip install cython")
    
    # Paso 2: Crear aplicación
    print("\n Creando aplicación MYPYME...")
    app_code = '''
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.core.window import Window

class MYPYMEMobileApp(App):
    def build(self):
        Window.size = (400, 600)
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Título
        title = Label(
            text='SISTEMA MYPYME',
            size_hint_y=None,
            height=60,
            font_size='24sp',
            bold=True,
            color=(0.2, 0.6, 0.8, 1)
        )
        layout.add_widget(title)
        
        # Subtítulo
        subtitle = Label(
            text='Sistema de Gestión Empresarial',
            size_hint_y=None,
            height=40,
            font_size='14sp',
            color=(0.4, 0.4, 0.4, 1)
        )
        layout.add_widget(subtitle)
        
        # Botones principales
        buttons_data = [
            ('VENTAS', (0.2, 0.8, 0.2, 1)),
            ('INVENTARIO', (0.2, 0.6, 0.8, 1)),
            ('REPORTES', (0.8, 0.4, 0.2, 1)),
            ('CONFIGURACIÓN', (0.6, 0.2, 0.8, 1))
        ]
        
        for text, color in buttons_data:
            btn = Button(
                text=text,
                size_hint_y=None,
                height=70,
                background_color=color,
                font_size='16sp',
                bold=True
            )
            btn.bind(on_press=lambda x, t=text: self.mostrar_popup(t))
            layout.add_widget(btn)
        
        # Información de versión
        version_label = Label(
            text='Versión 1.0 - MYPYME Sistema',
            size_hint_y=None,
            height=40,
            font_size='10sp',
            color=(0.6, 0.6, 0.6, 1)
        )
        layout.add_widget(version_label)
        
        return layout
    
    def mostrar_popup(self, titulo):
        popup = Popup(
            title=titulo,
            content=Label(text=f'Módulo {titulo} en desarrollo'),
            size_hint=(None, None),
            size=(300, 200)
        )
        popup.open()

if __name__ == '__main__':
    MYPYMEMobileApp().run()
'''
    
    with open('main.py', 'w') as f:
        f.write(app_code)
    
    print("✅ Aplicación creada")
    
    # Paso 3: Crear buildozer.spec
    print("\n⚙️ Creando configuración...")
    buildozer_spec = """[app]
title = MYPYME Sistema
package.name = mypyme
package.domain = org.mypyme
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

requirements = python3,kivy

orientation = portrait
fullscreen = 0
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

android.api = 28
android.minapi = 21
android.ndk = 25b
android.sdk = 28
android.arch = arm64-v8a

android.allow_backup = True
android.logcat_filters = *:S python:D

[buildozer]
log_level = 2
warn_on_root = 1
"""
    
    with open('buildozer.spec', 'w') as f:
        f.write(buildozer_spec)
    
    print("✅ Configuración creada")
    
    # Paso 4: Limpiar caché anterior
    print("\n🧹 Limpiando caché anterior...")
    os.system("rm -rf .buildozer")
    
    # Paso 5: Generar APK
    print("\n🔨 Generando APK...")
    print("⏳ Esto puede tardar 10-15 minutos...")
    
    # Ejecutar buildozer
    result = os.system("buildozer android debug")
    
    # Paso 6: Verificar resultado
    print("\n📋 Verificando resultado...")
    
    if os.path.exists('bin/'):
        apk_files = [f for f in os.listdir('bin/') if f.endswith('.apk')]
        if apk_files:
            apk_file = apk_files[0]
            apk_size = os.path.getsize(f'bin/{apk_file}') / 1024 / 1024
            
            print(f"✅ ¡APK GENERADO EXITOSAMENTE!")
            print(f"📱 Archivo: {apk_file}")
            print(f"📏 Tamaño: {apk_size:.2f} MB")
            
            # Descargar APK
            files.download(f'bin/{apk_file}')
            print("⬇️ APK descargado a tu computadora")
            print("🎉 ¡Listo para instalar en tu Android!")
            
            return True
        else:
            print("❌ Carpeta bin/ existe pero no hay archivo .apk")
            return False
    else:
        print("❌ No se creó la carpeta bin/")
        return False

# Ejecutar la generación
if __name__ == "__main__":
    success = generar_apk_mypyme()
    if success:
        print("\n✨ ¡APK generado exitosamente!")
    else:
        print("\n❌ Error al generar el APK") 