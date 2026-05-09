from pathlib import Path
from core.ai_provider import AIProvider


class PatternExtractor:
    def __init__(self, provider: AIProvider):
        self.provider = provider

    def run(self, image_path: Path, output_path: Path) -> Path:
        return self.provider.extract_pattern(image_path, output_path)
