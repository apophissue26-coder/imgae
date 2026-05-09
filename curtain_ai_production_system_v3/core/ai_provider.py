from pathlib import Path
from typing import Dict, List


class AIProvider:
    def analyze_reference(self, image_path: Path) -> Dict[str, str]:
        return {
            "image_type": "mock_detected_reference",
            "style_dna": "warm_bright_clean_home_decor",
            "risk_tip": "mock: 请在生产前用真实模型二次校验",
        }

    def extract_pattern(self, image_path: Path) -> Dict[str, str]:
        return {"status": "mock_extracted", "note": "pattern extraction placeholder"}

    def generate_variations(self, pattern_path: Path) -> List[Dict[str, str]]:
        return [
            {"id": "direction_1", "name": "方向1_色彩裂变"},
            {"id": "direction_2", "name": "方向2_元素裂变"},
            {"id": "direction_3", "name": "方向3_风格同源新创"},
        ]

    def render_effect_images(self, variation_path: Path) -> Dict[str, str]:
        return {"status": "mock_rendered", "home_attr": "bright_warm_clean"}

    def enhance_hd(self, image_path: Path) -> Dict[str, str]:
        return {"status": "mock_hd_done", "next": "connect real-esrgan/comfyui/openai api"}
