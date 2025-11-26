@echo off
REM ============================================
REM  Script per compilare uno script Python
REM  Uso: create_exe_from_py.bat nomefile.py
REM ============================================

:: Controllo parametro
if "%~1"=="" (
    echo ERRORE: Devi specificare un file .py
    echo Uso: %~nx0 script.py
    exit /b 1
)

:: Percorso e nome del file
set FILE=%~1
set EXT=%~x1

:: Controllo che l'estensione sia .py
if /I not "%EXT%"==".py" (
    echo ERRORE: Il file deve avere estensione .py
    exit /b 1
)

:: Controllo che il file esista
if not exist "%FILE%" (
    echo ERRORE: Il file "%FILE%" non esiste.
    exit /b 1
)

echo Compilazione di "%FILE%" in corso...
pyinstaller --onefile "%FILE%"

echo.
echo Operazione completata.
exit /b 0
