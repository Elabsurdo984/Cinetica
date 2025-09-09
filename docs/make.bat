@ECHO OFF

pushd %~dp0

REM Check if sphinx-build is available
where sphinx-build >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo sphinx-build no se encuentra en el PATH. Por favor, instala Sphinx con:
    echo pip install sphinx sphinx-rtd-theme
    exit /b 1
)

if "%1" == "" goto help
if "%1" == "help" (
    :help
    echo Uso: make ^<comando^>
    echo.
    echo Comandos disponibles:
    echo   html    Crea la documentación en HTML
    echo   clean   Limpia los archivos generados
    echo   help    Muestra esta ayuda
    goto :eof
)

if "%1" == "clean" (
    rmdir /s /q _build
    echo Documentación limpiada.
    goto :eof
)

if "%1" == "html" (
    sphinx-build -b html . _build\html
    if %ERRORLEVEL% EQU 0 (
        echo.
        echo La documentación HTML se ha generado en _build\html\index.html
    )
    goto :eof
)

echo Comando desconocido: %1
goto help
