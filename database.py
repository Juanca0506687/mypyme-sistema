import sqlite3
import datetime
import random
import string
import hashlib
from typing import List, Tuple, Optional

class Database:
    def __init__(self, db_name: str = "mypyme.db"):
        self.db_name = db_name
        self.init_database()
    
    def generar_codigo_producto(self) -> str:
        """Generar código único para producto"""
        while True:
            # Formato: PRD-XXX123
            letras = ''.join(random.choices(string.ascii_uppercase, k=3))
            numeros = ''.join(random.choices(string.digits, k=3))
            codigo = f"PRD-{letras}{numeros}"
            
            # Verificar que no exista
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM productos WHERE codigo = ?', (codigo,))
            if cursor.fetchone()[0] == 0:
                conn.close()
                return codigo
            conn.close()
    
    def init_database(self):
        """Inicializar la base de datos con las tablas necesarias"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
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
                fecha_venta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                cliente_nombre TEXT,
                cliente_telefono TEXT,
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
        
        # Tabla de usuarios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                nombre_completo TEXT NOT NULL,
                rol TEXT NOT NULL CHECK (rol IN ('admin', 'usuario')),
                activo INTEGER DEFAULT 1,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla de movimientos de inventario
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS movimientos_inventario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                producto_id INTEGER,
                tipo_movimiento TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                fecha_movimiento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                descripcion TEXT,
                FOREIGN KEY (producto_id) REFERENCES productos (id)
            )
        ''')
        
        # Tabla de configuración
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS configuracion (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                clave TEXT UNIQUE NOT NULL,
                valor TEXT NOT NULL,
                descripcion TEXT
            )
        ''')
        
        # Tabla de auditoría
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS auditoria (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER,
                accion TEXT NOT NULL,
                tabla TEXT NOT NULL,
                registro_id INTEGER,
                detalles TEXT,
                fecha_accion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        
        # Crear usuario administrador por defecto si no existe
        self.crear_usuario_admin_default()
        
        # Inicializar configuración por defecto
        self.inicializar_configuracion()
    
    def crear_usuario_admin_default(self):
        """Crear usuario administrador por defecto"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Verificar si ya existe un admin
        cursor.execute('SELECT COUNT(*) FROM usuarios WHERE rol = "admin"')
        if cursor.fetchone()[0] == 0:
            # Crear admin por defecto: admin/admin123
            password_hash = hashlib.sha256("admin123".encode()).hexdigest()
            cursor.execute('''
                INSERT INTO usuarios (username, password, nombre_completo, rol)
                VALUES (?, ?, ?, ?)
            ''', ("admin", password_hash, "Administrador", "admin"))
            conn.commit()
        
        conn.close()
    
    def inicializar_configuracion(self):
        """Inicializar configuración por defecto"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Configuraciones por defecto
        configuraciones = [
            ("tasa_cambio_cup", "380", "Tasa de cambio USD a CUP"),
            ("tasa_cambio_mlc", "120", "Tasa de cambio USD a MLC"),
            ("monedas_disponibles", "USD,CUP,MLC", "Monedas disponibles en el sistema"),
            ("empresa_nombre", "MYPYME", "Nombre de la empresa"),
            ("empresa_direccion", "", "Dirección de la empresa"),
            ("empresa_telefono", "", "Teléfono de la empresa"),
            ("alerta_stock_bajo", "5", "Stock mínimo para alertas"),
            ("modo_oscuro", "false", "Modo oscuro activado"),
            ("backup_automatico", "true", "Backup automático activado")
        ]
        
        for clave, valor, descripcion in configuraciones:
            cursor.execute('''
                INSERT OR IGNORE INTO configuracion (clave, valor, descripcion)
                VALUES (?, ?, ?)
            ''', (clave, valor, descripcion))
        
        conn.commit()
        conn.close()
    
    def obtener_configuracion(self, clave: str, valor_por_defecto: str = "") -> str:
        """Obtener valor de configuración"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('SELECT valor FROM configuracion WHERE clave = ?', (clave,))
        resultado = cursor.fetchone()
        
        conn.close()
        return resultado[0] if resultado else valor_por_defecto
    
    def guardar_configuracion(self, clave: str, valor: str) -> bool:
        """Guardar valor de configuración"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO configuracion (clave, valor)
                VALUES (?, ?)
            ''', (clave, valor))
            
            conn.commit()
            conn.close()
            return True
        except:
            return False
    
    def registrar_auditoria(self, usuario_id: int, accion: str, tabla: str, registro_id: Optional[int] = None, detalles: str = ""):
        """Registrar acción en auditoría"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO auditoria (usuario_id, accion, tabla, registro_id, detalles)
                VALUES (?, ?, ?, ?, ?)
            ''', (usuario_id, accion, tabla, registro_id, detalles))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error al registrar auditoría: {e}")
    
    def obtener_auditoria(self, limite: int = 100) -> List[Tuple]:
        """Obtener registros de auditoría"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT a.fecha_accion, u.nombre_completo, a.accion, a.tabla, a.detalles
            FROM auditoria a
            LEFT JOIN usuarios u ON a.usuario_id = u.id
            ORDER BY a.fecha_accion DESC
            LIMIT ?
        ''', (limite,))
        
        auditoria = cursor.fetchall()
        conn.close()
        return auditoria
    
    def autenticar_usuario(self, username: str, password: str) -> Optional[Tuple]:
        """Autenticar usuario y retornar información del usuario"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        cursor.execute('''
            SELECT id, username, nombre_completo, rol, activo
            FROM usuarios
            WHERE username = ? AND password = ? AND activo = 1
        ''', (username, password_hash))
        
        usuario = cursor.fetchone()
        conn.close()
        return usuario
    
    def crear_usuario(self, username: str, password: str, nombre_completo: str, rol: str) -> bool:
        """Crear nuevo usuario"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            cursor.execute('''
                INSERT INTO usuarios (username, password, nombre_completo, rol)
                VALUES (?, ?, ?, ?)
            ''', (username, password_hash, nombre_completo, rol))
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def obtener_usuarios(self) -> List[Tuple]:
        """Obtener todos los usuarios"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, username, nombre_completo, rol, activo, fecha_creacion
            FROM usuarios
            ORDER BY username
        ''')
        
        usuarios = cursor.fetchall()
        conn.close()
        return usuarios
    
    def cambiar_estado_usuario(self, usuario_id: int, activo: bool) -> bool:
        """Activar/desactivar usuario"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute('UPDATE usuarios SET activo = ? WHERE id = ?', (1 if activo else 0, usuario_id))
            
            conn.commit()
            conn.close()
            return True
        except:
            return False
    
    def agregar_producto(self, codigo: str, nombre: str, categoria: str, descripcion: str,
                        precio_compra: float, precio_venta: float, stock: int, stock_minimo: int = 5, foto: Optional[str] = None) -> bool:
        """Agregar un nuevo producto"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO productos (codigo, nombre, categoria, descripcion, precio_compra, precio_venta, stock, stock_minimo, foto)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (codigo, nombre, categoria, descripcion, precio_compra, precio_venta, stock, stock_minimo, foto))
            
            # Registrar movimiento de inventario inicial
            producto_id = cursor.lastrowid
            cursor.execute('''
                INSERT INTO movimientos_inventario (producto_id, tipo_movimiento, cantidad, descripcion)
                VALUES (?, 'ENTRADA', ?, 'Stock inicial')
            ''', (producto_id, stock))
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def obtener_productos(self) -> List[Tuple]:
        """Obtener todos los productos"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, codigo, nombre, categoria, descripcion, precio_compra, precio_venta, stock, stock_minimo, foto
            FROM productos
            ORDER BY nombre
        ''')
        
        productos = cursor.fetchall()
        conn.close()
        return productos
    
    def obtener_producto_por_id(self, producto_id: int) -> Optional[Tuple]:
        """Obtener un producto por su ID"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, codigo, nombre, categoria, descripcion, precio_compra, precio_venta, stock, stock_minimo, foto
            FROM productos
            WHERE id = ?
        ''', (producto_id,))
        
        producto = cursor.fetchone()
        conn.close()
        return producto
    
    def actualizar_stock(self, producto_id: int, cantidad: int, tipo_movimiento: str, descripcion: str = ""):
        """Actualizar el stock de un producto"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Obtener stock actual
        cursor.execute('SELECT stock FROM productos WHERE id = ?', (producto_id,))
        stock_actual = cursor.fetchone()[0]
        
        # Calcular nuevo stock
        if tipo_movimiento == "ENTRADA":
            nuevo_stock = stock_actual + cantidad
        else:  # SALIDA
            nuevo_stock = stock_actual - cantidad
        
        # Actualizar stock
        cursor.execute('UPDATE productos SET stock = ? WHERE id = ?', (nuevo_stock, producto_id))
        
        # Registrar movimiento
        cursor.execute('''
            INSERT INTO movimientos_inventario (producto_id, tipo_movimiento, cantidad, descripcion)
            VALUES (?, ?, ?, ?)
        ''', (producto_id, tipo_movimiento, cantidad, descripcion))
        
        conn.commit()
        conn.close()
    
    def crear_venta(self, numero_factura: str, cliente_nombre: str, cliente_telefono: str, 
                    items: List[Tuple], metodo_pago: str = "Efectivo", moneda: str = "USD") -> bool:
        """Crear una nueva venta con sus detalles"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            # Calcular total (usar el subtotal de cada item)
            total = sum(item[3] for item in items)  # subtotal
            
            # Crear venta
            cursor.execute('''
                INSERT INTO ventas (numero_factura, cliente_nombre, cliente_telefono, total, moneda, metodo_pago)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (numero_factura, cliente_nombre, cliente_telefono, total, moneda, metodo_pago))
            
            venta_id = cursor.lastrowid
            
            # Crear detalles de venta
            for producto_id, cantidad, precio_unitario, subtotal in items:
                cursor.execute('''
                    INSERT INTO detalles_venta (venta_id, producto_id, cantidad, precio_unitario, subtotal)
                    VALUES (?, ?, ?, ?, ?)
                ''', (venta_id, producto_id, cantidad, precio_unitario, subtotal))
                
                # Actualizar stock
                self.actualizar_stock(producto_id, cantidad, "SALIDA", f"Venta {numero_factura}")
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al crear venta: {e}")
            return False
    
    def obtener_ventas(self) -> List[Tuple]:
        """Obtener todas las ventas"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, numero_factura, fecha_venta, cliente_nombre, cliente_telefono, total, moneda, metodo_pago
            FROM ventas
            ORDER BY fecha_venta DESC
        ''')
        
        ventas = cursor.fetchall()
        conn.close()
        return ventas
    
    def obtener_detalles_venta(self, venta_id: int) -> List[Tuple]:
        """Obtener detalles de una venta específica"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT p.nombre, dv.cantidad, dv.precio_unitario, dv.subtotal
            FROM detalles_venta dv
            JOIN productos p ON dv.producto_id = p.id
            WHERE dv.venta_id = ?
        ''', (venta_id,))
        
        detalles = cursor.fetchall()
        conn.close()
        return detalles
    
    def obtener_productos_bajo_stock(self) -> List[Tuple]:
        """Obtener productos con stock bajo el mínimo"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, codigo, nombre, categoria, stock, stock_minimo
            FROM productos
            WHERE stock <= stock_minimo
            ORDER BY stock ASC
        ''')
        
        productos = cursor.fetchall()
        conn.close()
        return productos
    
    def obtener_movimientos_inventario(self, producto_id: Optional[int] = None) -> List[Tuple]:
        """Obtener movimientos de inventario"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        if producto_id:
            cursor.execute('''
                SELECT mi.fecha_movimiento, mi.tipo_movimiento, mi.cantidad, mi.descripcion, p.nombre
                FROM movimientos_inventario mi
                JOIN productos p ON mi.producto_id = p.id
                WHERE mi.producto_id = ?
                ORDER BY mi.fecha_movimiento DESC
            ''', (producto_id,))
        else:
            cursor.execute('''
                SELECT mi.fecha_movimiento, mi.tipo_movimiento, mi.cantidad, mi.descripcion, p.nombre
                FROM movimientos_inventario mi
                JOIN productos p ON mi.producto_id = p.id
                ORDER BY mi.fecha_movimiento DESC
            ''')
        
        movimientos = cursor.fetchall()
        conn.close()
        return movimientos 