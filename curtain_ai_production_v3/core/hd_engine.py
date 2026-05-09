from pathlib import Path
from PIL import Image, ImageFilter, ImageEnhance


def enhance_hd(image_path: Path, out_path: Path) -> Path:
    with Image.open(image_path) as im:
        img = im.convert("RGB")
        img = img.filter(ImageFilter.UnsharpMask(radius=1.5, percent=150, threshold=2))
        img = ImageEnhance.Contrast(img).enhance(1.08)
        img.save(out_path)
    return out_path
