@echo off
setlocal
cd /d "%~dp0"
"%~dp0@CWRC\prepare\cwrc-prepare.exe" "%~dp0." --if-needed
if errorlevel 1 (
    pause
    exit /b 1
)
start "" "%~dp0@CWRC\client\PoseidonGame.exe" --add-mod @CWRC --voice English %*
