from __future__ import annotations

from pathlib import Path

from config import SUPPORTED_DPI, SUPPORTED_REPEAT
from vertical_repeat_engine import GenerateParams, generate_vertical_repeat


def validate_params(unit1: str, unit2: str, output_dir: str, dpi: int, repeat_count: int) -> GenerateParams:
    p1 = Path(unit1)
    p2 = Path(unit2)
    out = Path(output_dir)

    if not p1.exists():
        raise FileNotFoundError(f"单元一图片不存在: {p1}")
    if not p2.exists():
        raise FileNotFoundError(f"单元二图片不存在: {p2}")
    if dpi not in SUPPORTED_DPI:
        raise ValueError("DPI 只能是 150 或 300")
    if repeat_count not in SUPPORTED_REPEAT:
        raise ValueError("重复次数只能是 2、4、6、8、10")

    return GenerateParams(
        unit1_path=p1,
        unit2_path=p2,
        output_dir=out,
        dpi=dpi,
        repeat_count=repeat_count,
    )


def run_generate(unit1: str, unit2: str, output_dir: str, dpi: int, repeat_count: int):
    params = validate_params(unit1, unit2, output_dir, dpi, repeat_count)
    return generate_vertical_repeat(params)
