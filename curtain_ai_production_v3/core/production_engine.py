from pathlib import Path
from core.vertical_repeat_engine import VerticalRepeatEngine


class ProductionEngine:
    def __init__(self):
        self.repeater = VerticalRepeatEngine()

    def run(self, selected_variation: Path, output_dir: Path) -> Path:
        output_dir.mkdir(parents=True, exist_ok=True)
        preview = output_dir / "production_preview.png"
        return self.repeater.build_1212_vertical(selected_variation, selected_variation, preview, repeats=3)
