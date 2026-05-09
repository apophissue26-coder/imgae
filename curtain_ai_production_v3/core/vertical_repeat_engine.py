from pathlib import Path
from PIL import Image


class VerticalRepeatEngine:
    def build_1212_vertical(self, unit_1: Path, unit_2: Path, output_path: Path, repeats: int = 4) -> Path:
        a = Image.open(unit_1).convert("RGB")
        b = Image.open(unit_2).convert("RGB")
        w = max(a.width, b.width)
        h = (a.height + b.height) * repeats
        canvas = Image.new("RGB", (w, h), (245, 245, 245))
        y = 0
        for _ in range(repeats):
            for unit in (a, b):
                canvas.paste(unit.resize((w, unit.height)), (0, y))
                y += unit.height
        canvas.save(output_path)
        return output_path
