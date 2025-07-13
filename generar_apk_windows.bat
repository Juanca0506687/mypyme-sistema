@echo off
echo ========================================
echo    GENERADOR DE APK MYPYME SISTEMA
echo    VERSION WINDOWS
echo ========================================
echo.

echo Instalando dependencias para Windows...
pip install kivy[base] kivy[full] buildozer

echo.
echo ========================================
echo    OPCIONES PARA GENERAR APK
echo ========================================
echo.
echo 1. Usar Google Colab (Recomendado)
echo 2. Usar WSL (Windows Subsystem for Linux)
echo 3. Usar Docker
echo 4. Usar servicio online
echo.
echo Selecciona una opcion (1-4):
set /p choice=

if "%choice%"=="1" goto colab
if "%choice%"=="2" goto wsl
if "%choice%"=="3" goto docker
if "%choice%"=="4" goto online
goto end

:colab
echo.
echo ========================================
echo    OPCION 1: GOOGLE COLAB
echo ========================================
echo.
echo 1. Ve a Google Colab: https://colab.research.google.com
echo 2. Crea un nuevo notebook
echo 3. Ejecuta estos comandos:
echo.
echo !pip install buildozer
echo !pip install cython
echo !git clone https://github.com/kivy/buildozer.git
echo !cd buildozer
echo !python setup.py build
echo !pip install -e .
echo.
echo 4. Sube tus archivos a Google Drive
echo 5. Ejecuta: buildozer android debug
echo.
echo El APK se generara en la carpeta bin/
echo.
pause
goto end

:wsl
echo.
echo ========================================
echo    OPCION 2: WSL (WINDOWS SUBSYSTEM FOR LINUX)
echo ========================================
echo.
echo 1. Instala WSL desde Microsoft Store
echo 2. Instala Ubuntu en WSL
echo 3. Abre Ubuntu y ejecuta:
echo.
echo sudo apt update
echo sudo apt install -y python3 python3-pip
echo sudo apt install -y git zip unzip openjdk-8-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
echo pip3 install buildozer
echo.
echo 4. Copia tus archivos a WSL
echo 5. Ejecuta: buildozer android debug
echo.
pause
goto end

:docker
echo.
echo ========================================
echo    OPCION 3: DOCKER
echo ========================================
echo.
echo 1. Instala Docker Desktop
echo 2. Ejecuta este comando:
echo.
echo docker run --volume "%cd%:/home/user/hostcwd" kivy/buildozer --workdir /home/user/hostcwd android debug
echo.
echo El APK se generara en la carpeta bin/
echo.
pause
goto end

:online
echo.
echo ========================================
echo    OPCION 4: SERVICIOS ONLINE
echo ========================================
echo.
echo Puedes usar estos servicios online:
echo.
echo 1. Google Colab (Gratis)
echo    https://colab.research.google.com
echo.
echo 2. Replit (Gratis)
echo    https://replit.com
echo.
echo 3. Gitpod (Gratis)
echo    https://gitpod.io
echo.
echo 4. GitHub Codespaces (Pago)
echo    https://github.com/features/codespaces
echo.
echo Instrucciones generales:
echo 1. Sube tus archivos al servicio
echo 2. Instala buildozer
echo 3. Ejecuta: buildozer android debug
echo 4. Descarga el APK generado
echo.
pause
goto end

:end
echo.
echo ========================================
echo    INFORMACION ADICIONAL
echo ========================================
echo.
echo Para probar la aplicacion en Windows:
echo python mypyme_mobile.py
echo.
echo Para desarrollo y pruebas:
echo - Usa la version de escritorio: python main.py
echo - Usa la version movil: python mypyme_mobile.py
echo.
echo El APK generado funcionara en dispositivos Android
echo con version 5.0 (API 21) o superior.
echo.
pause 