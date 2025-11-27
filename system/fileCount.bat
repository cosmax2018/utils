@echo off
setlocal disableDelayedExpansion
if "%~1"=="" (call :recurse ".") else call :recurse %1
exit /b

:recurse
setlocal
set fileCnt=0
for /d %%D in ("%~1\*") do call :recurse "%%~fD"
for /f %%A in ('dir /b /a-d "%~1\*" 2^>nul ^| find /v /c ""') do set /a fileCnt+=%%A
echo "%~f1"  %fileCnt%
( 
  endlocal
  set /a fileCnt+=%fileCnt%
)
exit /b
