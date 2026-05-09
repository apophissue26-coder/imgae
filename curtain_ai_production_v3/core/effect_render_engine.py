from pathlib import Path
from core.ai_provider import AIProvider
from config import EFFECT_TYPES


class EffectRenderEngine:
    def __init__(self, provider: AIProvider):
        self.provider = provider

    def run(self, variation_path: Path, output_dir: Path) -> list[Path]:
        return self.provider.render_effect_images(variation_path, output_dir, EFFECT_TYPES)
