from pathlib import Path
from PIL import Image


def extract_pattern(source: Path, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    with Image.open(source) as im:
        w, h = im.size
        crop = im.crop((w * 0.2, h * 0.15, w * 0.8, h * 0.85)).convert("RGB")
        out = output_dir / "extracted_pattern.png"
        crop.save(out)
    return out
