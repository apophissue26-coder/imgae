from pathlib import Path
from PIL import Image, ImageEnhance, ImageOps, ImageFilter
from .project_state import VariationResult


def generate_three_directions(pattern: Path, output_dir: Path) -> list[VariationResult]:
    output_dir.mkdir(parents=True, exist_ok=True)
    with Image.open(pattern) as base:
        base = base.convert("RGB")

        v1_img = ImageEnhance.Color(base).enhance(1.6)
        v1 = output_dir / "variation_1_color.png"; v1_img.save(v1)

        v2_img = ImageOps.posterize(base, 4).filter(ImageFilter.DETAIL)
        v2 = output_dir / "variation_2_shape.png"; v2_img.save(v2)

        v3_img = ImageOps.autocontrast(base.filter(ImageFilter.SMOOTH_MORE))
        v3 = output_dir / "variation_3_recreate.png"; v3_img.save(v3)

    return [
        VariationResult("方案1", "方向1-改色不改形", "保持图形，增强暖色层次", pattern_image=v1),
        VariationResult("方案2", "方向2-改形不改色", "保持主色，调整元素层级", pattern_image=v2),
        VariationResult("方案3", "方向3-同风格重创", "保持风格，生成新纹理组织", pattern_image=v3),
    ]
