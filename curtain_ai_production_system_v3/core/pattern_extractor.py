from pathlib import Path
from PIL import Image, ImageFilter

from .ai_provider import AIProvider


def extract_pattern(image_path: Path, output_dir: Path, provider: AIProvider) -> Path:
    provider.extract_pattern(image_path)
    dst = output_dir / "extracted_pattern.png"
    img = Image.open(image_path).convert("RGB").filter(ImageFilter.DETAIL)
    img.save(dst)
    return dst
