# 📱 MYPYME Sistema - Versión Móvil

## 🚀 Descripción

Esta es la versión móvil de tu sistema MYPYME, desarrollada con Kivy para funcionar en dispositivos Android. Mantiene todas las funcionalidades principales del sistema de escritorio pero adaptadas para pantallas táctiles.

## 📋 Funcionalidades Móviles

### 🔐 **Sistema de Login**
- Login seguro con usuario y contraseña
- Roles diferenciados (admin/usuario)
- Sesiones persistentes

### 📦 **Gestión de Productos**
- Agregar productos con información completa
- Códigos automáticos
- Categorización (Electrodomésticos, Útiles del Hogar, Vehículos)
- Precios de compra y venta

### 📊 **Control de Inventario**
- Ver stock en tiempo real
- Alertas visuales para stock bajo
- Actualización de cantidades
- Historial de movimientos

### 💰 **Sistema de Ventas**
- Crear ventas con múltiples productos
- Soporte para múltiples monedas (USD, CUP, MLC)
- Conversión automática de precios
- Generación de facturas

### 📈 **Reportes**
- Reportes de inventario
- Reportes de ventas
- Reportes de productos bajo stock
- Exportación de datos

### ⚙️ **Configuración**
- Tasas de cambio configurables
- Información de la empresa
- Alertas personalizables
- Configuración de usuarios

### 🔄 **Respaldo y Restauración**
- Crear respaldos de datos
- Restaurar desde respaldos
- Exportar información

## 📱 Características Móviles

### **Interfaz Adaptada**
- Botones grandes para pantallas táctiles
- Navegación intuitiva
- Colores para alertas visuales
- Diseño responsive

### **Optimización Móvil**
- Base de datos SQLite local
- Funcionamiento offline
- Sincronización de datos
- Bajo consumo de recursos

### **Seguridad**
- Login obligatorio
- Control de permisos por rol
- Auditoría de acciones
- Datos encriptados localmente

## 🛠️ Instalación

### **Requisitos Previos**
- Python 3.7+
- Buildozer
- Android SDK (opcional, se descarga automáticamente)

### **Pasos de Instalación**

1. **Instalar dependencias:**
   ```bash
   pip install kivy buildozer
   ```

2. **Generar APK:**
   ```bash
   buildozer android debug
   ```

3. **Instalar en dispositivo:**
   - Copiar el archivo `bin/mypyme-1.0-debug.apk` a tu dispositivo Android
   - Habilitar "Instalar aplicaciones de fuentes desconocidas"
   - Instalar el APK

### **Usando el Script Automático**
1. Ejecutar `generar_apk.bat`
2. Esperar a que se complete la generación
3. Instalar el APK generado

## 📱 Uso en Dispositivo

### **Primera Ejecución**
1. Abrir la aplicación
2. Iniciar sesión con:
   - Usuario: `admin`
   - Contraseña: `admin123`

### **Navegación**
- **Botones principales:** Acceso directo a funcionalidades
- **Popups:** Ventanas emergentes para formularios
- **Scroll:** Desplazamiento en listas largas
- **Tap:** Selección de elementos

### **Funcionalidades por Rol**

#### **Administrador**
- Acceso completo a todas las funciones
- Gestión de usuarios
- Configuración del sistema
- Auditoría completa

#### **Usuario Normal**
- Realizar ventas
- Ver inventario (solo lectura)
- Generar reportes básicos

## 🔧 Configuración

### **Tasas de Cambio**
- Configurar en la pestaña "Configuración"
- USD → CUP: 380 (por defecto)
- USD → MLC: 120 (por defecto)

### **Alertas de Stock**
- Configurar nivel mínimo de stock
- Notificaciones automáticas
- Colores de alerta en inventario

### **Usuarios**
- Crear usuarios nuevos
- Asignar roles
- Activar/desactivar usuarios

## 📊 Base de Datos

### **Estructura**
- SQLite local en el dispositivo
- Tablas: usuarios, productos, ventas, detalles_venta
- Datos persistentes entre sesiones

### **Respaldo**
- Crear respaldos automáticos
- Exportar datos a archivos
- Restaurar desde respaldos

## 🚨 Solución de Problemas

### **Error de Instalación**
- Verificar que el dispositivo permite instalación de fuentes desconocidas
- Comprobar espacio disponible en el dispositivo

### **Error de Login**
- Verificar credenciales
- Usar usuario admin por defecto: `admin` / `admin123`

### **Error de Base de Datos**
- Verificar permisos de escritura
- Reiniciar la aplicación
- Restaurar desde respaldo

### **Problemas de Rendimiento**
- Cerrar otras aplicaciones
- Reiniciar el dispositivo
- Limpiar caché de la aplicación

## 📞 Soporte

### **Logs de Error**
- Los errores se registran automáticamente
- Revisar logs en caso de problemas
- Contactar soporte técnico si es necesario

### **Actualizaciones**
- Verificar nuevas versiones
- Actualizar la aplicación cuando esté disponible
- Hacer respaldo antes de actualizar

## 🎯 Ventajas de la Versión Móvil

### **Portabilidad**
- Llevar tu negocio contigo
- Acceso desde cualquier lugar
- Funcionamiento offline

### **Facilidad de Uso**
- Interfaz táctil intuitiva
- Navegación rápida
- Acceso directo a funciones

### **Eficiencia**
- Ventas rápidas
- Consultas instantáneas
- Reportes en tiempo real

### **Seguridad**
- Datos locales seguros
- Control de acceso
- Auditoría completa

## 🔮 Próximas Funcionalidades

### **Sincronización en la Nube**
- Respaldo automático en la nube
- Sincronización entre dispositivos
- Acceso web complementario

### **Funcionalidades Avanzadas**
- Escáner de códigos de barras
- Impresión de tickets
- Integración con sistemas de pago

### **Mejoras de Interfaz**
- Temas personalizables
- Modo oscuro
- Iconos personalizados

---

**¡Tu sistema MYPYME ahora está disponible en tu dispositivo Android!** 📱✨ 