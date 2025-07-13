@echo off
echo ========================================
echo    GENERANDO APK MYPYME CON DOCKER
echo ========================================
echo.

echo Verificando Docker...
docker --version
if %errorlevel% neq 0 (
    echo ERROR: Docker no esta instalado o no esta corriendo
    echo Por favor instala Docker Desktop y asegurate de que este corriendo
    pause
    exit /b 1
)

echo.
echo Docker encontrado. Verificando que Docker Desktop este corriendo...
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker Desktop no esta corriendo
    echo Por favor abre Docker Desktop y espera a que este listo
    pause
    exit /b 1
)

echo.
echo Docker Desktop esta corriendo. Descargando imagen de Buildozer...

REM Intentar con imagen alternativa
docker pull kivy/buildozer:latest
if %errorlevel% neq 0 (
    echo.
    echo Intentando con imagen alternativa...
    docker pull kivy/buildozer:stable
    if %errorlevel% neq 0 (
        echo.
        echo ERROR: No se pudo descargar la imagen de Buildozer
        echo Intentando metodo alternativo...
        goto metodo_alternativo
    )
)

echo.
echo Imagen descargada exitosamente. Generando APK...
echo.

REM Ejecutar buildozer
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
    goto metodo_alternativo
)

goto fin

:metodo_alternativo
echo.
echo ========================================
echo    METODO ALTERNATIVO: GOOGLE COLAB
echo ========================================
echo.
echo Como Docker no funciono, usaremos Google Colab
echo.
echo 1. Ve a: https://colab.research.google.com
echo 2. Crea un nuevo notebook
echo 3. Ejecuta estos comandos uno por uno:
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

:fin
echo.
echo Presiona cualquier tecla para salir...
pause >nul 