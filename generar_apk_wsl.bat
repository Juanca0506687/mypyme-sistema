@echo off
echo ========================================
echo    GENERADOR DE APK MYPYME - WSL
echo ========================================
echo.

echo Verificando WSL...
wsl --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: WSL no esta instalado
    echo.
    echo Para instalar WSL:
    echo 1. Abre PowerShell como administrador
    echo 2. Ejecuta: wsl --install
    echo 3. Reinicia tu PC
    echo 4. Instala Ubuntu desde Microsoft Store
    echo.
    pause
    exit /b 1
)

echo WSL encontrado. Verificando Ubuntu...
wsl -d Ubuntu -e ls >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Ubuntu no esta instalado en WSL
    echo.
    echo Para instalar Ubuntu:
    echo 1. Abre Microsoft Store
    echo 2. Busca "Ubuntu"
    echo 3. Instala Ubuntu
    echo 4. Configura tu usuario y contraseña
    echo.
    pause
    exit /b 1
)

echo Ubuntu encontrado. Preparando entorno...
echo.

echo Instalando dependencias en WSL...
wsl -d Ubuntu -e bash -c "
echo 'Actualizando paquetes...'
sudo apt update
echo 'Instalando dependencias...'
sudo apt install -y python3 python3-pip git zip unzip openjdk-8-jdk
sudo apt install -y autoconf libtool pkg-config zlib1g-dev libncurses5-dev
sudo apt install -y libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
echo 'Instalando buildozer...'
pip3 install buildozer
echo 'Dependencias instaladas correctamente'
"

echo.
echo Copiando archivos a WSL...
wsl -d Ubuntu -e bash -c "
mkdir -p ~/mypyme_apk
cd ~/mypyme_apk
"

echo Copiando main.py...
wsl -d Ubuntu -e bash -c "cat > ~/mypyme_apk/main.py" < main.py

echo Copiando buildozer.spec...
wsl -d Ubuntu -e bash -c "cat > ~/mypyme_apk/buildozer.spec" < buildozer.spec

echo.
echo Generando APK en WSL...
wsl -d Ubuntu -e bash -c "
cd ~/mypyme_apk
echo 'Generando APK...'
buildozer android debug
echo 'APK generado correctamente'
"

echo.
echo Copiando APK a Windows...
wsl -d Ubuntu -e bash -c "
if [ -f ~/mypyme_apk/bin/*.apk ]; then
    cp ~/mypyme_apk/bin/*.apk /mnt/c/Users/juanc/Documents/New\ folder\ \(3\)/
    echo 'APK copiado a Windows'
else
    echo 'No se encontro el archivo APK'
fi
"

echo.
echo ========================================
echo    VERIFICACION FINAL
echo ========================================
echo.
dir *.apk
if exist *.apk (
    echo.
    echo ✅ APK generado exitosamente!
    echo 📱 Archivo: %cd%\*.apk
    echo.
    echo Puedes instalar este APK en tu dispositivo Android
) else (
    echo.
    echo ❌ No se encontro el archivo APK
    echo Revisa los logs de WSL para ver el error
)

echo.
pause 