from pathlib import Path
from PIL import Image


class ExportEngine:
    def export_tif(self, input_image: Path, output_tif: Path, dpi: int = 300) -> Path:
        img = Image.open(input_image).convert("RGB")
        img.save(output_tif, format="TIFF", dpi=(dpi, dpi))
        return output_tif

    def export_params(self, output_file: Path, params: dict) -> Path:
        lines = [f"{k}: {v}" for k, v in params.items()]
        output_file.write_text("\n".join(lines), encoding="utf-8")
        return output_file
