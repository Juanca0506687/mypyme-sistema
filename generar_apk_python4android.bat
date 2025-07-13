@echo off
echo ========================================
echo    GENERADOR DE APK MYPYME - PYTHON4ANDROID
echo ========================================
echo.

echo Instalando python-for-android...
pip install python-for-android

echo.
echo Verificando instalacion...
python -c "import p4a; print('python-for-android instalado correctamente')"
if %errorlevel% neq 0 (
    echo ERROR: No se pudo instalar python-for-android
    echo Intentando metodo alternativo...
    pip install --upgrade python-for-android
)

echo.
echo Generando APK con python-for-android...
echo ⏳ Esto puede tardar 5-10 minutos...
echo.

python -m p4a apk --private . --package=org.mypyme --name="MYPYME Sistema" --version=1.0 --bootstrap=sdl2 --requirements=python3,kivy --arch=arm64-v8a

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo    APK GENERADO EXITOSAMENTE!
    echo ========================================
    echo.
    echo El archivo APK se encuentra en la carpeta actual
    echo.
    dir *.apk
    echo.
    echo Puedes instalar este APK en tu dispositivo Android
) else (
    echo.
    echo ERROR: No se pudo generar el APK
    echo Revisa los logs anteriores para ver el error
)

echo.
pause 