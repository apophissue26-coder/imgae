from pathlib import Path

PROJECT_NAME = "curtain_ai_production_system_v3"
PROJECT_NAME_CN = "窗帘印花裂变生产系统 V3"
DEFAULT_DPI = 150
SUPPORTED_DPI = (150, 300)
DEFAULT_LAYOUT_MODE = "竖向 1-2-1-2 生产排版模式"

BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"
LOG_DIR = BASE_DIR / "logs"

for p in (INPUT_DIR, OUTPUT_DIR, LOG_DIR):
    p.mkdir(parents=True, exist_ok=True)
