import logging
from pathlib import Path


def get_logger(log_path: Path) -> logging.Logger:
    logger = logging.getLogger("curtain_ai_v3")
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)

    fh = logging.FileHandler(log_path, encoding="utf-8")
    fh.setLevel(logging.ERROR)
    fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))

    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)
    sh.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))

    logger.addHandler(fh)
    logger.addHandler(sh)
    return logger
