from pathlib import Path

APP_NAME = "窗帘竖向1-2生产图工具 V2"
OUTPUT_TIFF_NAME = "竖向1-2生产图.tif"
OUTPUT_PREVIEW_NAME = "预览图.png"
OUTPUT_PARAM_NAME = "参数记录.txt"
LOG_DIR_NAME = "logs"
ERROR_LOG_NAME = "error.log"
SUPPORTED_DPI = (150, 300)
SUPPORTED_REPEAT = (2, 4, 6, 8, 10)
SUPPORTED_IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff"}


def ensure_log_dir(base: Path) -> Path:
    log_dir = base / LOG_DIR_NAME
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir
