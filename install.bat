@echo off
echo ========================================
echo    INSTALADOR SISTEMA MYPYME
echo ========================================
echo.

echo Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no está instalado o no está en el PATH
    echo Por favor instala Python 3.7 o superior
    pause
    exit /b 1
)

echo Python encontrado. Instalando dependencias...
pip install -r requirements.txt

if errorlevel 1 (
    echo ERROR: No se pudieron instalar las dependencias
    pause
    exit /b 1
)

echo.
echo ========================================
echo    INSTALACIÓN COMPLETADA
echo ========================================
echo.
echo Para ejecutar el sistema:
echo   python main.py
echo.
echo Usuario por defecto: admin
echo Contraseña por defecto: admin123
echo.
pause 