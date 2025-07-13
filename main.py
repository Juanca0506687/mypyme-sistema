
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
