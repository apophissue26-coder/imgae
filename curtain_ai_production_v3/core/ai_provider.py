from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance, ImageDraw


class AIProvider:
    """Mock AI provider. Replace methods with OpenAI/ComfyUI/local model integrations."""

    def analyze_reference(self, image_path: Path) -> dict:
        return {
            "image_type": "mock_detected_reference",
            "style_dna": "warm, bright, home-decoration friendly",
            "risk_tips": ["检查花型边缘精度", "确认面料纹理是否适合大幅输出"],
        }

    def extract_pattern(self, image_path: Path, output_path: Path) -> Path:
        img = Image.open(image_path).convert("RGB")
        pattern = ImageOps.autocontrast(img)
        pattern.save(output_path)
        return output_path

    def generate_variations(self, pattern_path: Path, output_dir: Path) -> list[Path]:
        output_dir.mkdir(parents=True, exist_ok=True)
        base = Image.open(pattern_path).convert("RGB")
        vars = []
        v1 = ImageEnhance.Color(base).enhance(1.8)
        p1 = output_dir / "variation_direction_1_color.png"
        v1.save(p1)
        vars.append(p1)
        v2 = base.transpose(Image.FLIP_LEFT_RIGHT)
        p2 = output_dir / "variation_direction_2_elements.png"
        v2.save(p2)
        vars.append(p2)
        v3 = ImageEnhance.Brightness(base).enhance(1.1)
        draw = ImageDraw.Draw(v3)
        draw.text((20, 20), "Style DNA Recreation", fill=(255, 120, 60))
        p3 = output_dir / "variation_direction_3_recreate.png"
        v3.save(p3)
        vars.append(p3)
        return vars

    def render_effect_images(self, variation_path: Path, output_dir: Path, effect_types: list[str]) -> list[Path]:
        output_dir.mkdir(parents=True, exist_ok=True)
        base = Image.open(variation_path).convert("RGB")
        files = []
        for i, effect in enumerate(effect_types, start=1):
            canvas = base.copy()
            draw = ImageDraw.Draw(canvas)
            draw.rectangle((10, 10, 420, 70), outline=(255, 255, 255), width=2)
            draw.text((20, 30), f"{i}. {effect}", fill=(255, 255, 255))
            p = output_dir / f"effect_{i}_{effect}.png"
            canvas.save(p)
            files.append(p)
        return files

    def enhance_hd(self, image_path: Path, output_path: Path) -> Path:
        img = Image.open(image_path).convert("RGB")
        img = ImageEnhance.Sharpness(img).enhance(1.6)
        img.save(output_path)
        return output_path
