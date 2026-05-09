from pathlib import Path
from PIL import Image


def analyze_reference(image_path: Path) -> dict:
    with Image.open(image_path) as im:
        w, h = im.size
        mode = im.mode
    src_type = "实拍/场景图" if h != 0 and w / h > 0.7 else "竖版窗帘图"
    return {
        "source_type": src_type,
        "size": f"{w}x{h}",
        "mode": mode,
        "summary": "已完成基础分析，可接入 OpenAI API / ComfyUI / 本地模型做深度识别。",
    }
