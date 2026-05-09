from pathlib import Path
from core.ai_provider import AIProvider


class VariationEngine:
    def __init__(self, provider: AIProvider):
        self.provider = provider

    def run(self, pattern_path: Path, output_dir: Path) -> list[Path]:
        return self.provider.generate_variations(pattern_path, output_dir)
