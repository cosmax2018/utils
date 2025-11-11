@echo off
cls
echo.
echo ⏳ Avvio aggiornamento pacchetti...
echo ===============================

REM Aggiorna Chocolatey
echo.
echo 🔄 Aggiorno Chocolatey...
choco upgrade chocolatey -y

REM Aggiorna tutti i pacchetti Chocolatey
echo.
echo 📦 Aggiorno tutti i pacchetti installati con Chocolatey...
choco upgrade all -y

REM Aggiorna tutti i pacchetti Winget
echo.
echo 📦 Aggiorno tutti i pacchetti installati con Winget...
winget upgrade --all --silent --accept-package-agreements --accept-source-agreements

echo.
echo ✅ Aggiornamento completato!
pause
