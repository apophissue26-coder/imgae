from pathlib import Path

from config import OUTPUT_DIR
from core.ai_provider import AIProvider
from core.effect_render_engine import render_effect_images
from core.export_engine import export_tif_and_params
from core.pattern_extractor import extract_pattern
from core.production_engine import generate_production
from core.reference_analyzer import analyze_reference
from core.variation_engine import generate_variations


def run_pipeline(source_image: Path, dpi: int = 150) -> dict:
    provider = AIProvider()
    report = analyze_reference(source_image, OUTPUT_DIR, provider)
    pattern = extract_pattern(source_image, OUTPUT_DIR, provider)
    variations = generate_variations(pattern, OUTPUT_DIR, provider)
    effects = render_effect_images(variations[0], OUTPUT_DIR)
    preview = generate_production(variations[0], variations[1], OUTPUT_DIR)
    tif, params = export_tif_and_params(preview, OUTPUT_DIR, dpi=dpi)
    return {
        "analysis_report": report,
        "extracted_pattern": pattern,
        "variations": variations,
        "selected_effects": effects,
        "production_preview": preview,
        "tif": tif,
        "params": params,
    }
