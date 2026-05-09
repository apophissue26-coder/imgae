from pathlib import Path
from core.ai_provider import AIProvider


class HDEngine:
    def __init__(self, provider: AIProvider):
        self.provider = provider

    def run(self, image_path: Path, output_path: Path) -> Path:
        return self.provider.enhance_hd(image_path, output_path)
