from pathlib import Path

APP_NAME = "窗帘印花裂变生产系统 V3"
BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"
LOG_DIR = BASE_DIR / "logs"

DPI_OPTIONS = (150, 300)
DEFAULT_DPI = 150
REPEAT_OPTIONS = (2, 4, 6, 8, 10)
DEFAULT_REPEAT = 4

DEFAULT_WIDTH_CM = 140.0
DEFAULT_HEIGHT_CM = 250.0

OPEN_ENDPOINTS = {
    "openai": None,
    "comfyui": None,
    "local_model": None,
}
