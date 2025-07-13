# 📱 Instrucciones para Generar APK - Sistema MYPYME

## 🚀 Opción 1: Google Colab (Recomendado - Gratis)

### Paso 1: Preparar Archivos
1. Asegúrate de tener estos archivos en tu proyecto:
   - `mypyme_mobile.py`
   - `buildozer.spec`
   - `database.py`
   - `login.py`

### Paso 2: Usar Google Colab
1. Ve a [Google Colab](https://colab.research.google.com)
2. Crea un nuevo notebook
3. Copia y pega el contenido de `colab_buildozer.ipynb`
4. Ejecuta las celdas en orden

### Paso 3: Subir Archivos
1. En la celda "upload_files", sube todos los archivos del proyecto
2. Espera a que se complete la carga

### Paso 4: Generar APK
1. Ejecuta la celda "generate_apk"
2. Espera 10-15 minutos para la compilación
3. El APK se generará en la carpeta `bin/`

### Paso 5: Descargar APK
1. Ejecuta la celda "download_apk"
2. El archivo se descargará automáticamente

## 🐧 Opción 2: WSL (Windows Subsystem for Linux)

### Paso 1: Instalar WSL
```bash
# En PowerShell como administrador
wsl --install
```

### Paso 2: Instalar Ubuntu
1. Reinicia tu computadora
2. Se instalará Ubuntu automáticamente
3. Crea un usuario y contraseña

### Paso 3: Instalar Dependencias
```bash
sudo apt update
sudo apt install -y python3 python3-pip
sudo apt install -y git zip unzip openjdk-8-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
pip3 install buildozer
```

### Paso 4: Copiar Archivos
```bash
# Desde Windows, copia tus archivos a WSL
cp /mnt/c/Users/juanc/Documents/New\ folder\ \(3\)/* /home/tu_usuario/mypyme/
```

### Paso 5: Generar APK
```bash
cd /home/tu_usuario/mypyme/
buildozer android debug
```

## 🐳 Opción 3: Docker

### Paso 1: Instalar Docker Desktop
1. Descarga Docker Desktop desde [docker.com](https://docker.com)
2. Instálalo y reinicia tu computadora

### Paso 2: Ejecutar Comando
```bash
docker run --volume "%cd%:/home/user/hostcwd" kivy/buildozer --workdir /home/user/hostcwd android debug
```

## 🌐 Opción 4: Servicios Online

### Replit (Gratis)
1. Ve a [replit.com](https://replit.com)
2. Crea un nuevo proyecto Python
3. Sube tus archivos
4. Ejecuta: `pip install buildozer && buildozer android debug`

### Gitpod (Gratis)
1. Ve a [gitpod.io](https://gitpod.io)
2. Crea un nuevo workspace
3. Sube tus archivos
4. Ejecuta los comandos de instalación y buildozer

## 📱 Instalación en Dispositivo Android

### Paso 1: Habilitar Fuentes Desconocidas
1. Ve a Configuración > Seguridad
2. Activa "Fuentes desconocidas" o "Instalar aplicaciones de fuentes desconocidas"

### Paso 2: Instalar APK
1. Copia el archivo APK a tu dispositivo
2. Abre el archivo APK
3. Confirma la instalación

### Paso 3: Usar la Aplicación
1. Abre la aplicación MYPYME
2. Inicia sesión con:
   - Usuario: `admin`
   - Contraseña: `admin123`

## 🔧 Solución de Problemas

### Error: "Unknown command/target android"
- **Solución**: Buildozer no funciona directamente en Windows
- **Alternativa**: Usa Google Colab, WSL o Docker

### Error: "Permission denied"
- **Solución**: Ejecuta como administrador o usa `sudo`

### Error: "Java not found"
- **Solución**: Instala Java JDK 8 o superior

### Error: "SDK not found"
- **Solución**: Buildozer descarga automáticamente el SDK

### APK muy grande
- **Solución**: Usa `buildozer android debug` para versión de desarrollo
- **Alternativa**: Usa `buildozer android release` para versión optimizada

## 📊 Información del APK

### Características del APK Generado
- **Nombre**: `mypyme-1.0-debug.apk`
- **Tamaño**: ~50-100 MB
- **Versión Android**: 5.0+ (API 21+)
- **Arquitecturas**: ARM64, ARMv7

### Funcionalidades Incluidas
✅ Sistema de login
✅ Gestión de productos
✅ Control de inventario
✅ Sistema de ventas
✅ Reportes básicos
✅ Configuración
✅ Gestión de usuarios
✅ Respaldo y restauración

## 🎯 Recomendaciones

### Para Desarrollo
- Usa Google Colab para generar APKs rápidamente
- Prueba la aplicación en Windows con `python mypyme_mobile.py`
- Usa la versión de escritorio para desarrollo completo

### Para Producción
- Usa WSL para builds más rápidos
- Configura un entorno de desarrollo estable
- Mantén respaldos de tus archivos

### Para Distribución
- Firma el APK para distribución oficial
- Optimiza el tamaño del APK
- Prueba en múltiples dispositivos

## 📞 Soporte

### Si tienes problemas:
1. Verifica que todos los archivos estén presentes
2. Asegúrate de tener conexión a internet
3. Revisa los logs de error
4. Intenta con Google Colab (más estable)

### Archivos necesarios:
- `mypyme_mobile.py` (aplicación principal)
- `buildozer.spec` (configuración)
- `database.py` (base de datos)
- `login.py` (sistema de login)

¡Tu APK estará listo en 10-15 minutos! 📱✨ 1