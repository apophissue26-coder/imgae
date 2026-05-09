@echo off
chcp 65001 >nul
setlocal

if not exist venv (
  python -m venv venv
)
call venv\Scripts\activate
if errorlevel 1 goto :fail

python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller

pyinstaller --noconfirm --onefile --windowed --name "窗帘印花裂变生产系统V3" gui.py
if errorlevel 1 goto :fail

echo 打包完成：dist\窗帘印花裂变生产系统V3.exe
pause
exit /b 0

:fail
echo 打包失败，请检查错误信息。
pause
exit /b 1
