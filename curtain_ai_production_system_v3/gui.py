import traceback
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

from config import DEFAULT_DPI, DEFAULT_LAYOUT_MODE, OUTPUT_DIR, LOG_DIR, PROJECT_NAME_CN, SUPPORTED_DPI
from core.ai_provider import AIProvider
from core.effect_render_engine import render_effect_images
from core.export_engine import export_tif_and_params
from core.logger import get_logger
from core.pattern_extractor import extract_pattern
from core.production_engine import generate_production
from core.project_state import ProjectState
from core.reference_analyzer import analyze_reference
from core.variation_engine import generate_variations


class AppGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(PROJECT_NAME_CN)
        self.state = ProjectState()
        self.ai = AIProvider()
        self.logger = get_logger(LOG_DIR / "error.log")
        self.dpi_var = tk.IntVar(value=DEFAULT_DPI)

        self.status = tk.StringVar(value="请先上传原始图")
        self.flow = "上传原图 ↓ 分析 ↓ 提取印花 ↓ 裂变 ↓ 效果图 ↓ 生产图 ↓ 导出"
        self._build()

    def _build(self):
        tk.Label(self.root, text=PROJECT_NAME_CN, font=("Microsoft YaHei", 16, "bold")).pack(pady=8)
        tk.Label(self.root, text=f"当前默认生产模式：{DEFAULT_LAYOUT_MODE}", fg="blue").pack()
        tk.Label(self.root, text=f"流程：{self.flow}").pack(pady=4)
        tk.Label(self.root, textvariable=self.status, fg="green").pack(pady=4)

        for text, cmd in [
            ("1. 上传原始图", self.upload_source),
            ("2. 分析原图", self.analyze),
            ("3. 提取印花", self.extract),
            ("4. 三方向裂变", self.variation),
            ("5. 生成效果图", self.effects),
            ("6. 选择方案", self.select_plan),
            ("7. 生成生产图", self.production),
            ("8. 导出整套文件", self.export_all),
        ]:
            tk.Button(self.root, text=text, width=30, command=cmd).pack(pady=2)

        tk.OptionMenu(self.root, self.dpi_var, *SUPPORTED_DPI).pack(pady=4)

    def _safe(self, fn):
        try:
            fn()
        except Exception:
            self.logger.error(traceback.format_exc())
            messagebox.showerror("错误", "执行失败，详情见 logs/error.log")

    def upload_source(self):
        self._safe(lambda: self._upload_source())
    def _upload_source(self):
        p = filedialog.askopenfilename(filetypes=[("Image", "*.png *.jpg *.jpeg *.bmp *.webp")])
        if p:
            self.state.source_image = Path(p)
            self.status.set(f"已上传：{self.state.source_image.name}")
    def analyze(self): self._safe(lambda: self._analyze())
    def _analyze(self):
        self.state.analysis_report = analyze_reference(self.state.source_image, OUTPUT_DIR, self.ai)
        self.status.set("原图分析完成")
    def extract(self): self._safe(lambda: self._extract())
    def _extract(self):
        self.state.extracted_pattern = extract_pattern(self.state.source_image, OUTPUT_DIR, self.ai)
        self.status.set("印花提取完成")
    def variation(self): self._safe(lambda: self._variation())
    def _variation(self):
        self.state.variations = generate_variations(self.state.extracted_pattern, OUTPUT_DIR, self.ai)
        self.status.set("三方向裂变完成")
    def effects(self): self._safe(lambda: self._effects())
    def _effects(self):
        self.state.selected_variation = self.state.selected_variation or self.state.variations[0]
        self.state.selected_effects_dir = render_effect_images(self.state.selected_variation, OUTPUT_DIR)
        self.status.set("展示线6张效果图已生成")
    def select_plan(self): self._safe(lambda: self._select_plan())
    def _select_plan(self):
        if not self.state.variations:
            raise ValueError("请先裂变")
        self.state.selected_variation = self.state.variations[0]
        self.status.set(f"已选择方案：{self.state.selected_variation.name}")
    def production(self): self._safe(lambda: self._production())
    def _production(self):
        self.state.production_preview = generate_production(self.state.variations[0], self.state.variations[1], OUTPUT_DIR)
        self.status.set("生产预览已生成（竖向1-2-1-2）")
    def export_all(self): self._safe(lambda: self._export_all())
    def _export_all(self):
        self.state.exported_tif, params = export_tif_and_params(self.state.production_preview, OUTPUT_DIR, self.dpi_var.get())
        self.status.set(f"导出完成：{self.state.exported_tif.name} / {params.name}")


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("460x620")
    AppGUI(root)
    root.mainloop()
