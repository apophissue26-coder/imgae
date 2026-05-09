from pathlib import Path

from .vertical_repeat_engine import vertical_1212


def generate_production(variation1: Path, variation2: Path, output_dir: Path) -> Path:
    prod = output_dir / "production"
    prod.mkdir(parents=True, exist_ok=True)
    preview = prod / "production_preview.png"
    return vertical_1212(variation1, variation2, preview)
