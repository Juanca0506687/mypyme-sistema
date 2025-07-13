@echo off
echo ========================================
echo    GENERADOR DE APK MYPYME - SIMPLE
echo ========================================
echo.

echo Paso 1: Verificando WSL...
wsl --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: WSL no esta instalado
    pause
    exit /b 1
)

echo WSL encontrado.
echo.

echo Paso 2: Instalando buildozer en WSL...
wsl -d Ubuntu -e bash -c "pip3 install buildozer"

echo.
echo Paso 3: Creando directorio de trabajo...
wsl -d Ubuntu -e bash -c "mkdir -p ~/mypyme_apk"

echo.
echo Paso 4: Copiando archivos...
copy main.py \\wsl$\Ubuntu\home\juanc\mypyme_apk\
copy buildozer.spec \\wsl$\Ubuntu\home\juanc\mypyme_apk\

echo.
echo Paso 5: Generando APK...
echo ⏳ Esto puede tardar 10-15 minutos...
echo.

wsl -d Ubuntu -e bash -c "cd ~/mypyme_apk && buildozer android debug"

echo.
echo Paso 6: Copiando APK a Windows...
if exist \\wsl$\Ubuntu\home\juanc\mypyme_apk\bin\*.apk (
    copy \\wsl$\Ubuntu\home\juanc\mypyme_apk\bin\*.apk .
    echo ✅ APK copiado exitosamente!
) else (
    echo ❌ No se encontro el archivo APK
)

echo.
echo ========================================
echo    VERIFICACION FINAL
echo ========================================
dir *.apk
if exist *.apk (
    echo.
    echo ✅ ¡APK GENERADO EXITOSAMENTE!
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