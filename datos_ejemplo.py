#!/usr/bin/env python3
"""
Script para cargar datos de ejemplo en la base de datos
Útil para probar la aplicación con datos realistas
"""

from database import Database
import datetime

def cargar_datos_ejemplo():
    """Cargar datos de ejemplo en la base de datos"""
    db = Database()
    
    print("📦 Cargando datos de ejemplo...")
    
    # Productos de ejemplo
    productos_ejemplo = [
        # Electrodomésticos
        ("ELEC001", "Refrigerador Samsung", "Electrodomésticos", "Refrigerador de 2 puertas, 350L", 800.00, 1200.00, 5, 3),
        ("ELEC002", "Lavadora LG", "Electrodomésticos", "Lavadora automática 12kg", 600.00, 900.00, 3, 2),
        ("ELEC003", "Microondas Panasonic", "Electrodomésticos", "Microondas 20L con grill", 150.00, 250.00, 8, 4),
        ("ELEC004", "Televisor Sony 55\"", "Electrodomésticos", "Smart TV 4K 55 pulgadas", 1200.00, 1800.00, 2, 1),
        ("ELEC005", "Aire Acondicionado", "Electrodomésticos", "Split 12000 BTU", 400.00, 650.00, 0, 2),
        
        # Útiles del Hogar
        ("UTIL001", "Juego de Ollas", "Útiles del Hogar", "Set de 5 ollas antiadherentes", 80.00, 120.00, 10, 5),
        ("UTIL002", "Vajilla Completa", "Útiles del Hogar", "Vajilla para 6 personas", 120.00, 180.00, 7, 4),
        ("UTIL003", "Cubiertos de Acero", "Útiles del Hogar", "Set de cubiertos 24 piezas", 60.00, 90.00, 15, 8),
        ("UTIL004", "Sartén Antiadherente", "Útiles del Hogar", "Sartén 24cm con tapa", 25.00, 40.00, 20, 10),
        ("UTIL005", "Batidora Manual", "Útiles del Hogar", "Batidora de mano 300W", 35.00, 55.00, 0, 5),
        
        # Vehículos
        ("VEH001", "Bicicleta de Montaña", "Vehículos", "Bicicleta 21 velocidades", 200.00, 350.00, 4, 2),
        ("VEH002", "Scooter Eléctrico", "Vehículos", "Scooter eléctrico 500W", 800.00, 1200.00, 1, 1),
        ("VEH003", "Casco de Bicicleta", "Vehículos", "Casco ajustable con ventilación", 30.00, 50.00, 12, 6),
        ("VEH004", "Luces LED Bicicleta", "Vehículos", "Set de luces LED recargables", 15.00, 25.00, 25, 10),
        ("VEH005", "Candado para Bicicleta", "Vehículos", "Candado de acero reforzado", 20.00, 35.00, 0, 8)
    ]
    
    # Agregar productos
    productos_agregados = 0
    for producto in productos_ejemplo:
        if db.agregar_producto(*producto):
            productos_agregados += 1
            print(f"✅ Agregado: {producto[1]}")
        else:
            print(f"⚠️  Ya existe: {producto[1]}")
    
    print(f"\n📊 Total de productos agregados: {productos_agregados}")
    
    # Crear algunas ventas de ejemplo
    print("\n💰 Creando ventas de ejemplo...")
    
    # Venta 1
    items_venta1 = [
        (1, 1, 1200.00, 1200.00),  # Refrigerador
        (6, 2, 120.00, 240.00),    # Juego de Ollas
        (11, 1, 350.00, 350.00)    # Bicicleta
    ]
    db.crear_venta("FAC-20241201001", "María González", "555-0101", items_venta1, "Efectivo")
    print("✅ Venta 1: María González - $1,790.00")
    
    # Venta 2
    items_venta2 = [
        (2, 1, 900.00, 900.00),    # Lavadora
        (3, 1, 250.00, 250.00),    # Microondas
        (7, 1, 180.00, 180.00),    # Vajilla
        (13, 1, 50.00, 50.00)      # Casco
    ]
    db.crear_venta("FAC-20241201002", "Carlos Rodríguez", "555-0202", items_venta2, "Tarjeta")
    print("✅ Venta 2: Carlos Rodríguez - $1,380.00")
    
    # Venta 3
    items_venta3 = [
        (4, 1, 1800.00, 1800.00),  # Televisor
        (8, 2, 90.00, 180.00),     # Cubiertos
        (9, 3, 40.00, 120.00),     # Sartén
        (14, 2, 25.00, 50.00)      # Luces LED
    ]
    db.crear_venta("FAC-20241201003", "Ana Martínez", "555-0303", items_venta3, "Efectivo")
    print("✅ Venta 3: Ana Martínez - $2,150.00")
    
    print("\n🎉 Datos de ejemplo cargados exitosamente!")
    print("\n📋 Resumen:")
    print(f"   - Productos: {productos_agregados}")
    print(f"   - Ventas: 3")
    print(f"   - Productos con stock 0: 2 (en rojo)")
    print(f"   - Productos bajo stock: varios (en naranja)")
    
    print("\n🚀 Ahora puedes ejecutar la aplicación:")
    print("   python main.py")

if __name__ == "__main__":
    cargar_datos_ejemplo() 