from pathlib import Path


def export_record(path: Path, text: str) -> Path:
    path.write_text(text, encoding="utf-8")
    return path
