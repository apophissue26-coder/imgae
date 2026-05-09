from pathlib import Path
from core.reference_analyzer import analyze_reference
from core.pattern_extractor import extract_pattern
from core.variation_engine import generate_three_directions
from core.effect_render_engine import render_effect, render_showcase_set
from core.hd_engine import enhance_hd
from core.production_engine import build_production
from core.export_engine import export_record
from core.project_state import ProjectState


def run_pipeline(source: Path, out_dir: Path, dpi: int, repeat: int, width_cm: float, height_cm: float) -> ProjectState:
    state = ProjectState(source_image=source)
    state.analysis = analyze_reference(source)
    state.extracted_pattern = extract_pattern(source, out_dir / "analysis")
    state.variations = generate_three_directions(state.extracted_pattern, out_dir / "variations")
    return state


def generate_outputs(state: ProjectState, out_dir: Path, dpi: int, repeat: int, width_cm: float, height_cm: float):
    if not state.selected_variation:
        raise ValueError("请先选择一个裂变方案")

    v = state.selected_variation
    effect = render_effect(v.pattern_image, out_dir / "effect_main.png")
    showcase = render_showcase_set(effect, out_dir / "showcase")

    hd_pattern = enhance_hd(v.pattern_image, out_dir / "hd_pattern.png")
    prod_tif = build_production(hd_pattern, out_dir / "production", dpi, repeat, width_cm, height_cm)

    record = export_record(out_dir / "参数记录.txt", f"""项目: 窗帘印花裂变生产系统 V3
源图: {state.source_image}
分析: {state.analysis}
选中方案: {v.name} / {v.direction}
DPI: {dpi}
尺寸(cm): {width_cm} x {height_cm}
重复: {repeat}
生产规则: 仅竖向 1→2→1→2；每层完整单元；禁止左右并排；禁止中线裁切。
可扩展接口: OpenAI API / ComfyUI / 本地模型（当前为预留占位）。
""")
    return effect, showcase, prod_tif, record
