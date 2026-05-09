from pathlib import Path
from core.ai_provider import AIProvider


class ReferenceAnalyzer:
    def __init__(self, provider: AIProvider):
        self.provider = provider

    def run(self, image_path: Path) -> dict:
        return self.provider.analyze_reference(image_path)
