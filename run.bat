@echo off
cd /d "%~dp0"
chcp 65001 >nul
set PYTHONUTF8=1
py -3 src/demo.py
pause
