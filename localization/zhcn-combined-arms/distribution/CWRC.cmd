@echo off
setlocal
cd /d "%~dp0"
start "" "%~dp0@CWRC\client\PoseidonGame.exe" --add-mod @CWRC --voice English %*
