from pathlib import Path
from PIL import Image, ImageEnhance


def render_effect(pattern: Path, out_path: Path) -> Path:
    with Image.open(pattern) as im:
        img = im.convert("RGB").resize((900, 1400), Image.Resampling.LANCZOS)
        img = ImageEnhance.Brightness(img).enhance(1.08)
        img = ImageEnhance.Color(img).enhance(1.12)
        img.save(out_path)
    return out_path


def render_showcase_set(effect_image: Path, output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    names = ["主效果图", "侧面效果图", "产品场景图", "局部特写", "面料展示", "真实尺寸预览"]
    out = []
    with Image.open(effect_image) as im:
        base = im.convert("RGB")
        for idx, n in enumerate(names, start=1):
            clone = base.copy()
            clone = ImageEnhance.Brightness(clone).enhance(1 + idx * 0.01)
            p = output_dir / f"{idx:02d}_{n}.png"
            clone.save(p)
            out.append(p)
    return out
