from pathlib import Path
from PIL import Image
from .vertical_repeat_engine import vertical_repeat


def build_production(pattern: Path, output_dir: Path, dpi: int, repeat_count: int, width_cm: float, height_cm: float) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    with Image.open(pattern) as p:
        unit1 = p.convert("RGB")
        unit2 = unit1.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        long_img = vertical_repeat(unit1, unit2, repeat_count)
        out_tif = output_dir / "竖向1-2生产图.tif"
        long_img.save(out_tif, format="TIFF", compression="tiff_lzw", dpi=(dpi, dpi))
    return out_tif
