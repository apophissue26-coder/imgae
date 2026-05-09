@echo off
chcp 65001 >nul
setlocal

if not exist .venv (
  py -m venv .venv
)

call .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt

pyinstaller --noconfirm --clean --onefile --windowed --name "窗帘竖向1-2生产图工具V2" gui.py

echo.
echo 打包完成: dist\窗帘竖向1-2生产图工具V2.exe
pause
