from pathlib import Path
from PIL import Image, ImageEnhance, ImageOps

from .ai_provider import AIProvider


def generate_variations(pattern_path: Path, output_dir: Path, provider: AIProvider):
    var_dir = output_dir / "variations"
    var_dir.mkdir(parents=True, exist_ok=True)
    provider.generate_variations(pattern_path)
    base = Image.open(pattern_path).convert("RGB")

    d1 = ImageEnhance.Color(base).enhance(1.5)
    d1.save(var_dir / "direction_1_color.png")

    d2 = ImageOps.posterize(base, bits=4)
    d2.save(var_dir / "direction_2_element.png")

    d3 = ImageOps.autocontrast(ImageOps.solarize(base, threshold=128))
    d3.save(var_dir / "direction_3_recreate.png")

    return [var_dir / "direction_1_color.png", var_dir / "direction_2_element.png", var_dir / "direction_3_recreate.png"]
