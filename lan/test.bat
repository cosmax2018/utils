REM Avvia lo script principale con bypass dei permessi
Set-ExecutionPolicy -Scope Process Bypass
powershell -NoProfile -ExecutionPolicy Bypass -File "lan_info.ps1"
