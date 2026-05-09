from pathlib import Path
from PIL import Image


def export_tif_and_params(production_preview: Path, output_dir: Path, dpi: int = 150) -> tuple[Path, Path]:
    prod_dir = output_dir / "production"
    tif_path = prod_dir / "production_output.tif"
    Image.open(production_preview).save(tif_path, dpi=(dpi, dpi), compression="tiff_deflate")

    params = output_dir / "export_params.txt"
    params.write_text(
        "export configuration\n"
        f"dpi={dpi}\n"
        "unit=cm\n"
        "layout=竖向 1-2-1-2 生产排版模式\n",
        encoding="utf-8",
    )
    return tif_path, params
