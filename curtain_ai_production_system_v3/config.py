import sys
from pathlib import Path

PROJECT_NAME = "curtain_ai_production_system_v3"
PROJECT_NAME_CN = "窗帘印花裂变生产系统 V3"
DEFAULT_DPI = 150
SUPPORTED_DPI = (150, 300)
DEFAULT_LAYOUT_MODE = "竖向 1-2-1-2 生产排版模式"

BASE_DIR = Path(__file__).resolve().parent


def get_runtime_base_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return BASE_DIR


def get_runtime_output_dir() -> Path:
    return get_runtime_base_dir() / "output"


def get_runtime_log_dir() -> Path:
    return get_runtime_base_dir() / "logs"


INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = get_runtime_output_dir()
LOG_DIR = get_runtime_log_dir()

for p in (INPUT_DIR, OUTPUT_DIR, LOG_DIR):
    p.mkdir(parents=True, exist_ok=True)
