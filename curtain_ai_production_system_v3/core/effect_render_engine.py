from pathlib import Path
from PIL import Image, ImageDraw

VIEWS = ["01_main", "02_side", "03_scene", "04_closeup", "05_fabric", "06_real_size"]


def render_effect_images(variation_path: Path, output_dir: Path) -> Path:
    effects_dir = output_dir / "selected_effects"
    effects_dir.mkdir(parents=True, exist_ok=True)
    src = Image.open(variation_path).convert("RGB").resize((960, 1280))
    for name in VIEWS:
        canvas = src.copy()
        d = ImageDraw.Draw(canvas)
        d.rectangle((20, 20, 940, 120), fill=(255, 245, 230))
        d.text((40, 60), f"{name} | mock 家装效果图", fill=(60, 60, 60))
        canvas.save(effects_dir / f"{name}.png")
    return effects_dir
