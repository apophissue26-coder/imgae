@echo off
chcp 65001 >nul
cd /d %~dp0

echo [1/4] 检查 Python...
python --version >nul 2>nul
if errorlevel 1 (
    echo 未检测到 Python，请先安装 Python 3.10+
    pause
    exit /b 1
)

echo [2/4] 创建虚拟环境（如不存在）...
if not exist .venv (
    python -m venv .venv
)

echo [3/4] 安装依赖...
call .venv\Scripts\activate
pip install -r requirements.txt

echo [4/4] 启动应用...
streamlit run app.py
