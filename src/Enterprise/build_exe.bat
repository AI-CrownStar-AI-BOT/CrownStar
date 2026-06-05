@echo off
cd /d "%~dp0"
pip install -r requirements.txt
pip install pyinstaller
pyinstaller CrownStar_Enterprise.spec
pause
