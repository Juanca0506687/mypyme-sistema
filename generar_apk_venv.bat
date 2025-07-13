@echo off
echo ========================================
echo    GENERADOR DE APK MYPYME - ENTORNO VIRTUAL
echo ========================================
echo.

echo Paso 1: Creando entorno virtual en WSL...
wsl -d Ubuntu -e bash -c "python3 -m venv ~/mypyme_env"

echo.
echo Paso 2: Activando entorno virtual e instalando buildozer...
wsl -d Ubuntu -e bash -c "source ~/mypyme_env/bin/activate && pip install buildozer"

echo.
echo Paso 3: Creando directorio de trabajo...
wsl -d Ubuntu -e bash -c "mkdir -p ~/mypyme_apk"

echo.
echo Paso 4: Copiando archivos...
copy main.py \\wsl$\Ubuntu\home\juanc\mypyme_apk\
copy buildozer.spec \\wsl$\Ubuntu\home\juanc\mypyme_apk\

echo.
echo Paso 5: Generando APK con entorno virtual...
echo ⏳ Esto puede tardar 10-15 minutos...
echo.

wsl -d Ubuntu -e bash -c "source ~/mypyme_env/bin/activate && cd ~/mypyme_apk && buildozer android debug"

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