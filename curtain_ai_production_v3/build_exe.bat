@echo off
chcp 65001 >nul
cd /d %~dp0
if not exist .venv py -m venv .venv
call .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
pyinstaller --noconfirm --clean --onefile --windowed --name "窗帘印花裂变生产系统V3" gui.py
echo 完成: dist\窗帘印花裂变生产系统V3.exe
pause
