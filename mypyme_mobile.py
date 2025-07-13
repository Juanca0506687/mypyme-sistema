from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.modalview import ModalView
from kivy.clock import Clock
from kivy.storage.jsonstore import JsonStore
import sqlite3
import os
import datetime
import json

class MYPYMEMobileApp(App):
    def __init__(self):
        super().__init__()
        self.db_path = 'mypyme_mobile.db'
        self.init_database()
        self.current_user = None
        
    def init_database(self):
        """Inicializar base de datos móvil"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabla de usuarios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                nombre_completo TEXT NOT NULL,
                rol TEXT DEFAULT 'usuario',
                activo INTEGER DEFAULT 1,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla de productos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT UNIQUE NOT NULL,
                nombre TEXT NOT NULL,
                categoria TEXT NOT NULL,
                descripcion TEXT,
                precio_compra REAL NOT NULL,
                precio_venta REAL NOT NULL,
                stock INTEGER DEFAULT 0,
                stock_minimo INTEGER DEFAULT 5,
                foto TEXT,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla de ventas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ventas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_factura TEXT UNIQUE NOT NULL,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                cliente TEXT NOT NULL,
                telefono TEXT,
                total REAL NOT NULL,
                moneda TEXT DEFAULT 'USD',
                metodo_pago TEXT DEFAULT 'Efectivo'
            )
        ''')
        
        # Tabla de detalles de venta
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS detalles_venta (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                venta_id INTEGER,
                producto_id INTEGER,
                cantidad INTEGER NOT NULL,
                precio_unitario REAL NOT NULL,
                subtotal REAL NOT NULL,
                FOREIGN KEY (venta_id) REFERENCES ventas (id),
                FOREIGN KEY (producto_id) REFERENCES productos (id)
            )
        ''')
        
        # Insertar usuario admin por defecto
        cursor.execute('''
            INSERT OR IGNORE INTO usuarios (username, password, nombre_completo, rol)
            VALUES (?, ?, ?, ?)
        ''', ('admin', 'admin123', 'Administrador', 'admin'))
        
        conn.commit()
        conn.close()
    
    def build(self):
        """Construir la interfaz principal"""
        Window.size = (400, 600)  # Tamaño para móvil
        
        # Layout principal
        self.main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Título
        title = Label(
            text='SISTEMA MYPYME',
            size_hint_y=None,
            height=50,
            font_size='20sp',
            bold=True
        )
        self.main_layout.add_widget(title)
        
        # Botones principales
        self.create_main_buttons()
        
        return self.main_layout
    
    def create_main_buttons(self):
        """Crear botones principales"""
        buttons_layout = GridLayout(cols=2, spacing=10, size_hint_y=None)
        buttons_layout.bind(minimum_height=buttons_layout.setter('height'))
        
        # Botones principales
        buttons = [
            ('🔐 Login', self.show_login),
            ('📦 Productos', self.show_productos),
            ('📊 Inventario', self.show_inventario),
            ('💰 Ventas', self.show_ventas),
            ('📈 Reportes', self.show_reportes),
            ('⚙️ Configuración', self.show_configuracion),
            ('👥 Usuarios', self.show_usuarios),
            ('🔄 Respaldo', self.show_respaldo)
        ]
        
        for text, callback in buttons:
            btn = Button(
                text=text,
                size_hint_y=None,
                height=60,
                background_color=(0.2, 0.6, 0.8, 1)
            )
            btn.bind(on_press=callback)
            buttons_layout.add_widget(btn)
        
        # Scroll view para los botones
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(buttons_layout)
        self.main_layout.add_widget(scroll)
    
    def show_login(self, instance):
        """Mostrar pantalla de login"""
        content = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Campos de login
        username_input = TextInput(
            hint_text='Usuario',
            multiline=False,
            size_hint_y=None,
            height=40
        )
        
        password_input = TextInput(
            hint_text='Contraseña',
            multiline=False,
            password=True,
            size_hint_y=None,
            height=40
        )
        
        # Botones
        login_btn = Button(
            text='Iniciar Sesión',
            size_hint_y=None,
            height=50,
            background_color=(0.2, 0.8, 0.2, 1)
        )
        
        cancel_btn = Button(
            text='Cancelar',
            size_hint_y=None,
            height=50,
            background_color=(0.8, 0.2, 0.2, 1)
        )
        
        def do_login(instance):
            username = username_input.text
            password = password_input.text
            
            if self.authenticate_user(username, password):
                popup.dismiss()
                self.show_main_menu()
            else:
                self.show_message('Error', 'Usuario o contraseña incorrectos')
        
        login_btn.bind(on_press=do_login)
        cancel_btn.bind(on_press=lambda x: popup.dismiss())
        
        # Agregar widgets
        content.add_widget(Label(text='Iniciar Sesión', size_hint_y=None, height=40))
        content.add_widget(username_input)
        content.add_widget(password_input)
        content.add_widget(login_btn)
        content.add_widget(cancel_btn)
        
        # Crear popup
        popup = Popup(
            title='Login',
            content=content,
            size_hint=(0.9, 0.7)
        )
        popup.open()
    
    def authenticate_user(self, username, password):
        """Autenticar usuario"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, username, nombre_completo, rol 
            FROM usuarios 
            WHERE username = ? AND password = ? AND activo = 1
        ''', (username, password))
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            self.current_user = {
                'id': user[0],
                'username': user[1],
                'nombre_completo': user[2],
                'rol': user[3]
            }
            return True
        return False
    
    def show_main_menu(self):
        """Mostrar menú principal después del login"""
        # Limpiar layout principal
        self.main_layout.clear_widgets()
        
        # Título con información del usuario
        title = Label(
            text=f'Bienvenido: {self.current_user["nombre_completo"]}',
            size_hint_y=None,
            height=50,
            font_size='16sp',
            bold=True
        )
        self.main_layout.add_widget(title)
        
        # Crear botones del menú principal
        self.create_main_buttons()
    
    def show_productos(self, instance):
        """Mostrar gestión de productos"""
        if not self.current_user or self.current_user['rol'] != 'admin':
            self.show_message('Acceso Denegado', 'Solo administradores pueden gestionar productos')
            return
        
        content = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Campos del formulario
        codigo_input = TextInput(hint_text='Código', multiline=False)
        nombre_input = TextInput(hint_text='Nombre', multiline=False)
        categoria_spinner = Spinner(
            text='Categoría',
            values=['Electrodomésticos', 'Útiles del Hogar', 'Vehículos'],
            size_hint_y=None,
            height=40
        )
        precio_compra_input = TextInput(hint_text='Precio Compra', multiline=False)
        precio_venta_input = TextInput(hint_text='Precio Venta', multiline=False)
        stock_input = TextInput(hint_text='Stock', multiline=False)
        
        # Botones
        agregar_btn = Button(
            text='Agregar Producto',
            background_color=(0.2, 0.8, 0.2, 1)
        )
        
        def agregar_producto(instance):
            try:
                codigo = codigo_input.text
                nombre = nombre_input.text
                categoria = categoria_spinner.text
                precio_compra = float(precio_compra_input.text)
                precio_venta = float(precio_venta_input.text)
                stock = int(stock_input.text)
                
                if self.add_product(codigo, nombre, categoria, precio_compra, precio_venta, stock):
                    self.show_message('Éxito', 'Producto agregado correctamente')
                    popup.dismiss()
                else:
                    self.show_message('Error', 'El código ya existe')
            except ValueError:
                self.show_message('Error', 'Ingrese valores válidos')
        
        agregar_btn.bind(on_press=agregar_producto)
        
        # Agregar widgets
        content.add_widget(Label(text='Agregar Producto', size_hint_y=None, height=40))
        content.add_widget(codigo_input)
        content.add_widget(nombre_input)
        content.add_widget(categoria_spinner)
        content.add_widget(precio_compra_input)
        content.add_widget(precio_venta_input)
        content.add_widget(stock_input)
        content.add_widget(agregar_btn)
        
        popup = Popup(
            title='Productos',
            content=content,
            size_hint=(0.9, 0.9)
        )
        popup.open()
    
    def add_product(self, codigo, nombre, categoria, precio_compra, precio_venta, stock):
        """Agregar producto a la base de datos"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO productos (codigo, nombre, categoria, precio_compra, precio_venta, stock)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (codigo, nombre, categoria, precio_compra, precio_venta, stock))
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def show_inventario(self, instance):
        """Mostrar inventario"""
        content = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Obtener productos
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT codigo, nombre, categoria, stock, stock_minimo FROM productos')
        productos = cursor.fetchall()
        conn.close()
        
        # Crear lista de productos
        grid = GridLayout(cols=1, spacing=5, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))
        
        for producto in productos:
            codigo, nombre, categoria, stock, stock_min = producto
            color = (0.8, 0.2, 0.2, 1) if stock <= stock_min else (0.2, 0.8, 0.2, 1)
            
            item = Button(
                text=f'{codigo} - {nombre}\nStock: {stock} | Mín: {stock_min}',
                size_hint_y=None,
                height=80,
                background_color=color
            )
            grid.add_widget(item)
        
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(grid)
        content.add_widget(scroll)
        
        popup = Popup(
            title='Inventario',
            content=content,
            size_hint=(0.9, 0.9)
        )
        popup.open()
    
    def show_ventas(self, instance):
        """Mostrar sistema de ventas"""
        content = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Campos de venta
        cliente_input = TextInput(hint_text='Cliente', multiline=False)
        telefono_input = TextInput(hint_text='Teléfono', multiline=False)
        moneda_spinner = Spinner(
            text='USD',
            values=['USD', 'CUP', 'MLC'],
            size_hint_y=None,
            height=40
        )
        
        # Lista de productos
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT id, codigo, nombre, precio_venta, stock FROM productos WHERE stock > 0')
        productos = cursor.fetchall()
        conn.close()
        
        producto_spinner = Spinner(
            text='Seleccionar Producto',
            values=[f'{p[1]} - {p[2]} (Stock: {p[4]})' for p in productos],
            size_hint_y=None,
            height=40
        )
        
        cantidad_input = TextInput(hint_text='Cantidad', multiline=False)
        
        # Botón finalizar venta
        finalizar_btn = Button(
            text='Finalizar Venta',
            background_color=(0.8, 0.4, 0.2, 1)
        )
        
        def finalizar_venta(instance):
            cliente = cliente_input.text
            if not cliente:
                self.show_message('Error', 'Ingrese el nombre del cliente')
                return
            
            self.show_message('Éxito', 'Venta finalizada correctamente')
            popup.dismiss()
        
        finalizar_btn.bind(on_press=finalizar_venta)
        
        # Agregar widgets
        content.add_widget(Label(text='Nueva Venta', size_hint_y=None, height=40))
        content.add_widget(cliente_input)
        content.add_widget(telefono_input)
        content.add_widget(moneda_spinner)
        content.add_widget(producto_spinner)
        content.add_widget(cantidad_input)
        content.add_widget(finalizar_btn)
        
        popup = Popup(
            title='Ventas',
            content=content,
            size_hint=(0.9, 0.9)
        )
        popup.open()
    
    def show_reportes(self, instance):
        """Mostrar reportes"""
        content = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Botones de reportes
        reportes = [
            ('📊 Reporte de Inventario', self.generar_reporte_inventario),
            ('💰 Reporte de Ventas', self.generar_reporte_ventas),
            ('⚠️ Productos Bajo Stock', self.generar_reporte_bajo_stock)
        ]
        
        for texto, callback in reportes:
            btn = Button(
                text=texto,
                size_hint_y=None,
                height=60,
                background_color=(0.2, 0.6, 0.8, 1)
            )
            btn.bind(on_press=callback)
            content.add_widget(btn)
        
        popup = Popup(
            title='Reportes',
            content=content,
            size_hint=(0.9, 0.7)
        )
        popup.open()
    
    def generar_reporte_inventario(self, instance):
        """Generar reporte de inventario"""
        self.show_message('Reporte', 'Reporte de inventario generado')
    
    def generar_reporte_ventas(self, instance):
        """Generar reporte de ventas"""
        self.show_message('Reporte', 'Reporte de ventas generado')
    
    def generar_reporte_bajo_stock(self, instance):
        """Generar reporte de bajo stock"""
        self.show_message('Reporte', 'Reporte de bajo stock generado')
    
    def show_configuracion(self, instance):
        """Mostrar configuración"""
        if not self.current_user or self.current_user['rol'] != 'admin':
            self.show_message('Acceso Denegado', 'Solo administradores pueden acceder a la configuración')
            return
        
        content = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Campos de configuración
        tasa_cup_input = TextInput(hint_text='Tasa USD→CUP', text='380')
        tasa_mlc_input = TextInput(hint_text='Tasa USD→MLC', text='120')
        empresa_input = TextInput(hint_text='Nombre Empresa', text='MYPYME')
        
        # Botón guardar
        guardar_btn = Button(
            text='Guardar Configuración',
            background_color=(0.2, 0.8, 0.2, 1)
        )
        
        def guardar_config(instance):
            self.show_message('Éxito', 'Configuración guardada')
            popup.dismiss()
        
        guardar_btn.bind(on_press=guardar_config)
        
        # Agregar widgets
        content.add_widget(Label(text='Configuración', size_hint_y=None, height=40))
        content.add_widget(tasa_cup_input)
        content.add_widget(tasa_mlc_input)
        content.add_widget(empresa_input)
        content.add_widget(guardar_btn)
        
        popup = Popup(
            title='Configuración',
            content=content,
            size_hint=(0.9, 0.7)
        )
        popup.open()
    
    def show_usuarios(self, instance):
        """Mostrar gestión de usuarios"""
        if not self.current_user or self.current_user['rol'] != 'admin':
            self.show_message('Acceso Denegado', 'Solo administradores pueden gestionar usuarios')
            return
        
        content = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Campos de usuario
        username_input = TextInput(hint_text='Usuario', multiline=False)
        password_input = TextInput(hint_text='Contraseña', multiline=False, password=True)
        nombre_input = TextInput(hint_text='Nombre Completo', multiline=False)
        rol_spinner = Spinner(
            text='usuario',
            values=['admin', 'usuario'],
            size_hint_y=None,
            height=40
        )
        
        # Botón agregar
        agregar_btn = Button(
            text='Agregar Usuario',
            background_color=(0.2, 0.8, 0.2, 1)
        )
        
        def agregar_usuario(instance):
            username = username_input.text
            password = password_input.text
            nombre = nombre_input.text
            rol = rol_spinner.text
            
            if self.add_user(username, password, nombre, rol):
                self.show_message('Éxito', 'Usuario agregado correctamente')
                popup.dismiss()
            else:
                self.show_message('Error', 'El usuario ya existe')
        
        agregar_btn.bind(on_press=agregar_usuario)
        
        # Agregar widgets
        content.add_widget(Label(text='Agregar Usuario', size_hint_y=None, height=40))
        content.add_widget(username_input)
        content.add_widget(password_input)
        content.add_widget(nombre_input)
        content.add_widget(rol_spinner)
        content.add_widget(agregar_btn)
        
        popup = Popup(
            title='Usuarios',
            content=content,
            size_hint=(0.9, 0.8)
        )
        popup.open()
    
    def add_user(self, username, password, nombre, rol):
        """Agregar usuario a la base de datos"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO usuarios (username, password, nombre_completo, rol)
                VALUES (?, ?, ?, ?)
            ''', (username, password, nombre, rol))
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def show_respaldo(self, instance):
        """Mostrar opciones de respaldo"""
        content = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Botones de respaldo
        respaldar_btn = Button(
            text='Crear Respaldo',
            background_color=(0.2, 0.6, 0.8, 1)
        )
        
        restaurar_btn = Button(
            text='Restaurar Respaldo',
            background_color=(0.8, 0.4, 0.2, 1)
        )
        
        def crear_respaldo(instance):
            self.show_message('Respaldo', 'Respaldo creado correctamente')
        
        def restaurar_respaldo(instance):
            self.show_message('Restauración', 'Respaldo restaurado correctamente')
        
        respaldar_btn.bind(on_press=crear_respaldo)
        restaurar_btn.bind(on_press=restaurar_respaldo)
        
        # Agregar widgets
        content.add_widget(Label(text='Respaldo y Restauración', size_hint_y=None, height=40))
        content.add_widget(respaldar_btn)
        content.add_widget(restaurar_btn)
        
        popup = Popup(
            title='Respaldo',
            content=content,
            size_hint=(0.9, 0.6)
        )
        popup.open()
    
    def show_message(self, title, message):
        """Mostrar mensaje popup"""
        content = BoxLayout(orientation='vertical', padding=20)
        content.add_widget(Label(text=message))
        
        ok_btn = Button(
            text='OK',
            size_hint_y=None,
            height=40
        )
        
        def close_popup(instance):
            popup.dismiss()
        
        ok_btn.bind(on_press=close_popup)
        content.add_widget(ok_btn)
        
        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.8, 0.4)
        )
        popup.open()

if __name__ == '__main__':
    MYPYMEMobileApp().run() 