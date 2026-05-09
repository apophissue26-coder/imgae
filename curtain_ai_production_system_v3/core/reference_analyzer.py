from pathlib import Path

from .ai_provider import AIProvider


def analyze_reference(image_path: Path, output_dir: Path, provider: AIProvider) -> Path:
    result = provider.analyze_reference(image_path)
    report = output_dir / "analysis_report.txt"
    report.write_text(
        "原图分析结果\n"
        f"source={image_path}\n"
        f"type={result['image_type']}\n"
        f"style_dna={result['style_dna']}\n"
        f"risk={result['risk_tip']}\n",
        encoding="utf-8",
    )
    return report
