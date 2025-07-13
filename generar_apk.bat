@echo off
echo ========================================
echo    GENERADOR DE APK MYPYME SISTEMA
echo ========================================
echo.

echo Instalando dependencias...
pip install buildozer

echo.
echo Configurando entorno para Android...
echo.

echo Generando APK...
buildozer android debug

echo.
echo ========================================
echo    APK GENERADO EXITOSAMENTE
echo ========================================
echo.
echo El archivo APK se encuentra en:
echo bin/mypyme-1.0-debug.apk
echo.
echo Puedes instalar este APK en tu dispositivo Android
echo.
pause 