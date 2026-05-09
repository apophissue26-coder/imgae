from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"
LOG_DIR = BASE_DIR / "logs"

DEFAULT_DPI = 300
DEFAULT_PRODUCTION_MODE = "竖向 1-2-1-2 生产排版模式"
EFFECT_TYPES = ["主效果图", "侧面效果图", "产品场景图", "局部特写", "面料展示", "真实尺寸预览"]

for p in [INPUT_DIR, OUTPUT_DIR, LOG_DIR]:
    p.mkdir(parents=True, exist_ok=True)
