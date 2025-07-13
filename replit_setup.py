# ========================================
# CONFIGURACIÓN PARA REPLIT - GENERAR APK
# ========================================

print("🚀 Configurando Replit para generar APK MYPYME...")

# Crear archivo principal de la app
main_app = '''
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

# Crear buildozer.spec optimizado para Replit
buildozer_spec = '''[app]
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
'''

# Crear archivo de configuración de Replit
replit_config = '''{
  "language": "python3",
  "run": "python main.py",
  "packages": ["buildozer", "cython"]
}
'''

# Crear archivo .replit
replit_file = '''language = "python3"
run = "python main.py"
packages = ["buildozer", "cython"]
'''

# Crear archivo pyproject.toml
pyproject_toml = '''[tool.replit]
language = "python3"
run = "python main.py"

[tool.replit.packages]
buildozer = "*"
cython = "*"
'''

print("✅ Archivos de configuración creados")
print("\n📋 INSTRUCCIONES PARA REPLIT:")
print("=" * 50)
print("1. Ve a https://replit.com")
print("2. Crea un nuevo proyecto Python")
print("3. Copia estos archivos:")
print("   - main.py (código de la app)")
print("   - buildozer.spec (configuración)")
print("   - .replit (configuración de Replit)")
print("4. Ejecuta: buildozer android debug")
print("5. Descarga el APK desde la carpeta bin/")
print("=" * 50)

# Guardar archivos
with open('main.py', 'w') as f:
    f.write(main_app)

with open('buildozer.spec', 'w') as f:
    f.write(buildozer_spec)

with open('.replit', 'w') as f:
    f.write(replit_file)

with open('pyproject.toml', 'w') as f:
    f.write(pyproject_toml)

print("\n✅ Archivos guardados:")
print("- main.py")
print("- buildozer.spec") 
print("- .replit")
print("- pyproject.toml")

print("\n🚀 ¡Listo para usar en Replit!") 