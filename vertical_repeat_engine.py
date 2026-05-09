from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image

from config import OUTPUT_PARAM_NAME, OUTPUT_PREVIEW_NAME, OUTPUT_TIFF_NAME


@dataclass
class GenerateParams:
    unit1_path: Path
    unit2_path: Path
    output_dir: Path
    dpi: int
    repeat_count: int


def _load_rgb(path: Path) -> Image.Image:
    img = Image.open(path)
    try:
        return img.convert("RGB")
    finally:
        img.close()


def generate_vertical_repeat(params: GenerateParams) -> tuple[Path, Path, Path]:
    params.output_dir.mkdir(parents=True, exist_ok=True)

    unit1 = _load_rgb(params.unit1_path)
    unit2 = _load_rgb(params.unit2_path)

    target_width = max(unit1.width, unit2.width)
    if unit1.width != target_width:
        unit1 = unit1.resize((target_width, int(unit1.height * target_width / unit1.width)), Image.Resampling.LANCZOS)
    if unit2.width != target_width:
        unit2 = unit2.resize((target_width, int(unit2.height * target_width / unit2.width)), Image.Resampling.LANCZOS)

    sequence = []
    for i in range(params.repeat_count):
        sequence.append(unit1.copy() if i % 2 == 0 else unit2.copy())  # 1→2→1→2 from top to bottom

    total_height = sum(x.height for x in sequence)
    canvas = Image.new("RGB", (target_width, total_height), color=(255, 255, 255))

    y = 0
    for img in sequence:
        canvas.paste(img, (0, y))
        y += img.height

    tiff_path = params.output_dir / OUTPUT_TIFF_NAME
    preview_path = params.output_dir / OUTPUT_PREVIEW_NAME
    param_path = params.output_dir / OUTPUT_PARAM_NAME

    canvas.save(tiff_path, format="TIFF", compression="tiff_lzw", dpi=(params.dpi, params.dpi))
    preview = canvas.copy()
    preview.thumbnail((1000, 4000), Image.Resampling.LANCZOS)
    preview.save(preview_path, format="PNG")

    param_text = (
        "项目名称: 窗帘竖向1-2生产图工具 V2\n"
        f"单元一: {params.unit1_path}\n"
        f"单元二: {params.unit2_path}\n"
        f"输出目录: {params.output_dir}\n"
        f"DPI: {params.dpi}\n"
        f"重复次数: {params.repeat_count}\n"
        "排列规则: 单元一→单元二→单元一→单元二，严格竖向从上到下。\n"
        "禁止规则: 不允许左右并排；不允许中线竖向裁切；每层仅一个完整单元图。\n"
    )
    param_path.write_text(param_text, encoding="utf-8")

    return tiff_path, preview_path, param_path
