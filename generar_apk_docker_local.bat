@echo off
echo ========================================
echo    GENERADOR DE APK MYPYME - DOCKER
echo ========================================
echo.

echo Verificando Docker...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker no esta instalado
    echo.
    echo Para instalar Docker:
    echo 1. Ve a https://www.docker.com/products/docker-desktop/
    echo 2. Descarga Docker Desktop para Windows
    echo 3. Instala y reinicia tu PC
    echo 4. Asegurate de que Docker Desktop este corriendo
    echo.
    pause
    exit /b 1
)

echo Docker encontrado. Verificando que este corriendo...
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker Desktop no esta corriendo
    echo.
    echo Por favor:
    echo 1. Abre Docker Desktop
    echo 2. Espera a que este listo (icono verde)
    echo 3. Ejecuta este script nuevamente
    echo.
    pause
    exit /b 1
)

echo Docker Desktop esta corriendo.
echo.

echo Descargando imagen de buildozer...
docker pull kivy/buildozer:latest
if %errorlevel% neq 0 (
    echo ERROR: No se pudo descargar la imagen
    echo Intentando con imagen alternativa...
    docker pull kivy/buildozer:stable
    if %errorlevel% neq 0 (
        echo ERROR: No se pudo descargar ninguna imagen
        echo Verifica tu conexion a internet
        pause
        exit /b 1
    )
)

echo.
echo Generando APK con Docker...
echo ⏳ Esto puede tardar 10-15 minutos...
echo.

docker run --rm -v "%cd%:/home/user/hostcwd" kivy/buildozer:latest --workdir /home/user/hostcwd android debug

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo    APK GENERADO EXITOSAMENTE!
    echo ========================================
    echo.
    echo El archivo APK se encuentra en la carpeta: bin/
    echo.
    dir bin\*.apk
    echo.
    echo Puedes copiar el archivo .apk a tu dispositivo Android
    echo para instalarlo.
) else (
    echo.
    echo ERROR: No se pudo generar el APK
    echo Revisa los logs anteriores para ver el error
)

echo.
pause 