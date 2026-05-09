import base64
from datetime import datetime
from pathlib import Path
from typing import List

import streamlit as st
from openai import OpenAI


OUTPUT_DIR = Path(__file__).parent / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

SUPPORTED_SIZES = ["1024x1024", "1024x1536", "1536x1024"]
SUPPORTED_QUALITY = ["auto", "high", "medium", "low"]
SUPPORTED_COUNTS = [1, 2, 4]


def save_images(base64_images: List[str]) -> List[Path]:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    saved_files: List[Path] = []

    for idx, img_b64 in enumerate(base64_images, start=1):
        file_name = f"{timestamp}_{idx}.png"
        file_path = OUTPUT_DIR / file_name
        file_path.write_bytes(base64.b64decode(img_b64))
        saved_files.append(file_path)

    return saved_files


def main() -> None:
    st.set_page_config(page_title="curtain-image-generator-v1", layout="wide")
    st.title("curtain-image-generator-v1")
    st.caption("基于 OpenAI Images API 的高清视觉效果图生成工具")

    api_key = st.text_input("OPENAI_API_KEY", type="password", help="建议配置为系统环境变量")

    uploaded_file = st.file_uploader(
        "上传参考图片 (jpg/png/webp)",
        type=["jpg", "jpeg", "png", "webp"],
        accept_multiple_files=False,
    )

    prompt = st.text_area("中文提示词", placeholder="例如：现代客厅落地窗，浅灰色纱帘，清晨自然光，真实摄影风格")

    col1, col2, col3 = st.columns(3)
    with col1:
        image_count = st.selectbox("生成张数", SUPPORTED_COUNTS, index=0)
    with col2:
        size = st.selectbox("图片比例", SUPPORTED_SIZES, index=0)
    with col3:
        quality = st.selectbox("质量", SUPPORTED_QUALITY, index=0)

    model = st.selectbox("图片模型", ["gpt-image-1"], index=0, help="后续可替换为 OpenAI 可用的最新图片模型")

    if st.button("开始生成", type="primary", use_container_width=True):
        if not api_key:
            st.error("请先输入 OPENAI_API_KEY。")
            return
        if not uploaded_file:
            st.error("请上传参考图片。")
            return
        if not prompt.strip():
            st.error("请输入中文提示词。")
            return

        st.info("正在调用 OpenAI Images API 生成图片，请稍候...")
        try:
            client = OpenAI(api_key=api_key)
            uploaded_file.seek(0)
            response = client.images.edit(
                model=model,
                image=uploaded_file,
                prompt=prompt.strip(),
                size=size,
                quality=quality,
                n=image_count,
            )

            b64_list = [item.b64_json for item in response.data if getattr(item, "b64_json", None)]
            if not b64_list:
                st.error("未收到可用图片数据，请重试。")
                return

            saved_files = save_images(b64_list)
            st.success(f"生成完成，共 {len(saved_files)} 张，已保存到: {OUTPUT_DIR}")

            for i, file_path in enumerate(saved_files, start=1):
                image_bytes = file_path.read_bytes()
                st.image(image_bytes, caption=file_path.name, use_container_width=True)
                st.download_button(
                    label=f"下载第 {i} 张",
                    data=image_bytes,
                    file_name=file_path.name,
                    mime="image/png",
                    key=f"download_{file_path.name}",
                )

        except Exception as exc:
            st.error(f"生成失败: {exc}")


if __name__ == "__main__":
    main()
