import shutil
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox

from config import DEFAULT_PRODUCTION_MODE, EFFECT_TYPES, INPUT_DIR, OUTPUT_DIR
from core.ai_provider import AIProvider
from core.design_analyzer import DesignAnalyzer
from core.effect_render_engine import EffectRenderEngine
from core.export_engine import ExportEngine
from core.hd_engine import HDEngine
from core.logger import get_logger
from core.pattern_extractor import PatternExtractor
from core.production_engine import ProductionEngine
from core.project_state import ProjectState
from core.reference_analyzer import ReferenceAnalyzer
from core.variation_engine import VariationEngine


class CurtainV3GUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("窗帘印花裂变生产系统 V3")
        self.state = ProjectState()
        self.provider = AIProvider()
        self.logger = get_logger()
        self.ref_analyzer = ReferenceAnalyzer(self.provider)
        self.pattern_extractor = PatternExtractor(self.provider)
        self.design_analyzer = DesignAnalyzer()
        self.variation_engine = VariationEngine(self.provider)
        self.effect_engine = EffectRenderEngine(self.provider)
        self.hd_engine = HDEngine(self.provider)
        self.production_engine = ProductionEngine()
        self.export_engine = ExportEngine()

        self.status = tk.StringVar(value="就绪")
        self.var_choice = tk.StringVar(value="0")
        self._build()

    def _build(self):
        tk.Label(self.root, text="流程：上传原图 ↓ 分析 ↓ 提取印花 ↓ 裂变 ↓ 效果图 ↓ 生产图 ↓ 导出", fg="blue").pack(pady=4)
        tk.Label(self.root, text=f"当前默认生产模式：{DEFAULT_PRODUCTION_MODE}", fg="green").pack(pady=4)

        actions = [
            ("1. 上传原始图", self.upload_image),
            ("2. 分析原图", self.analyze_image),
            ("3. 提取印花", self.extract_pattern),
            ("4. 三方向裂变", self.generate_variations),
            ("5. 生成效果图", self.render_effects),
            ("6. 选择方案", self.select_variation),
            ("7. 生成生产图", self.generate_production),
            ("8. 导出整套文件", self.export_all),
        ]
        for text, cmd in actions:
            tk.Button(self.root, text=text, command=cmd, width=30).pack(pady=2)

        tk.Entry(self.root, textvariable=self.var_choice, width=10).pack(pady=2)
        tk.Label(self.root, text="输入方案索引(0/1/2)后点击“选择方案”").pack()
        tk.Label(self.root, textvariable=self.status, fg="purple").pack(pady=8)

    def _safe(self, func):
        try:
            func()
        except Exception as e:
            self.logger.error(str(e), exc_info=True)
            messagebox.showerror("错误", str(e))

    def upload_image(self):
        self._safe(self._upload_image)

    def _upload_image(self):
        path = filedialog.askopenfilename(title="选择原始图")
        if not path:
            return
        src = Path(path)
        dst = INPUT_DIR / src.name
        shutil.copy2(src, dst)
        self.state.source_image = dst
        self.status.set(f"已上传：{dst.name}")

    def analyze_image(self):
        self._safe(self._analyze_image)

    def _analyze_image(self):
        analysis = self.ref_analyzer.run(self.state.source_image)
        report = OUTPUT_DIR / "analysis_report.txt"
        report.write_text(self.design_analyzer.summarize(analysis), encoding="utf-8")
        self.state.analysis_report = report
        self.state.params["analysis"] = analysis
        self.status.set("分析完成")

    def extract_pattern(self):
        self._safe(self._extract_pattern)

    def _extract_pattern(self):
        p = OUTPUT_DIR / "extracted_pattern.png"
        self.state.extracted_pattern = self.pattern_extractor.run(self.state.source_image, p)
        self.status.set("印花提取完成")

    def generate_variations(self):
        self._safe(self._generate_variations)

    def _generate_variations(self):
        out = OUTPUT_DIR / "variations"
        self.state.variations = self.variation_engine.run(self.state.extracted_pattern, out)
        self.status.set("三方向裂变完成")

    def render_effects(self):
        self._safe(self._render_effects)

    def _render_effects(self):
        target = self.state.selected_variation or self.state.variations[0]
        out = OUTPUT_DIR / "selected_effects"
        self.state.selected_effects = self.effect_engine.run(target, out)
        self.state.params["effect_types"] = EFFECT_TYPES
        self.status.set("展示图生成完成")

    def select_variation(self):
        self._safe(self._select_variation)

    def _select_variation(self):
        idx = int(self.var_choice.get())
        self.state.selected_variation = self.state.variations[idx]
        self.status.set(f"已选择方案：{self.state.selected_variation.name}")

    def generate_production(self):
        self._safe(self._generate_production)

    def _generate_production(self):
        out = OUTPUT_DIR / "production"
        preview = self.production_engine.run(self.state.selected_variation or self.state.variations[0], out)
        hd = out / "production_hd.png"
        self.state.production_preview = self.hd_engine.run(preview, hd)
        self.status.set("生产图完成")

    def export_all(self):
        self._safe(self._export_all)

    def _export_all(self):
        tif = OUTPUT_DIR / "production" / "final_production.tif"
        self.state.export_tif = self.export_engine.export_tif(self.state.production_preview, tif, dpi=300)
        self.state.params["production_mode"] = DEFAULT_PRODUCTION_MODE
        self.state.params["dpi"] = 300
        self.export_engine.export_params(OUTPUT_DIR / "export_params.txt", self.state.params)
        self.status.set("导出完成")


def launch():
    root = tk.Tk()
    root.geometry("640x520")
    CurtainV3GUI(root)
    root.mainloop()


if __name__ == "__main__":
    launch()
