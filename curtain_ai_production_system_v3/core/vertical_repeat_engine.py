from pathlib import Path
from PIL import Image


def vertical_1212(unit1: Path, unit2: Path, output_path: Path, repeats: int = 6) -> Path:
    img1 = Image.open(unit1).convert("RGB")
    img2 = Image.open(unit2).convert("RGB").resize(img1.size)
    w, h = img1.size
    canvas = Image.new("RGB", (w, h * repeats))
    for i in range(repeats):
        canvas.paste(img1 if i % 2 == 0 else img2, (0, i * h))
    canvas.save(output_path)
    return output_path
