import logging
from config import LOG_DIR


def get_logger(name: str = "curtain_v3") -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler(LOG_DIR / "error.log", encoding="utf-8")
    fh.setLevel(logging.ERROR)
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger
