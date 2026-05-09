from __future__ import annotations

import logging
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from app import run_generate
from config import APP_NAME, ERROR_LOG_NAME, SUPPORTED_DPI, SUPPORTED_REPEAT, ensure_log_dir


class AppGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(APP_NAME)
        self.root.geometry("720x360")

        self.unit1_var = tk.StringVar()
        self.unit2_var = tk.StringVar()
        self.out_var = tk.StringVar(value=str(Path.cwd() / "output"))
        self.dpi_var = tk.IntVar(value=300)
        self.repeat_var = tk.IntVar(value=2)

        self._setup_logging()
        self._build_ui()

    def _setup_logging(self):
        log_dir = ensure_log_dir(Path.cwd())
        self.logger = logging.getLogger("curtain_tool")
        self.logger.setLevel(logging.ERROR)
        if not self.logger.handlers:
            fh = logging.FileHandler(log_dir / ERROR_LOG_NAME, encoding="utf-8")
            fh.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
            self.logger.addHandler(fh)

    def _pick_file(self, var: tk.StringVar):
        p = filedialog.askopenfilename(title="选择图片文件")
        if p:
            var.set(p)

    def _pick_dir(self):
        p = filedialog.askdirectory(title="选择输出文件夹")
        if p:
            self.out_var.set(p)

    def _build_ui(self):
        pad = {"padx": 8, "pady": 8}
        ttk.Label(self.root, text="单元一图片").grid(row=0, column=0, sticky="w", **pad)
        ttk.Entry(self.root, textvariable=self.unit1_var, width=60).grid(row=0, column=1, **pad)
        ttk.Button(self.root, text="选择", command=lambda: self._pick_file(self.unit1_var)).grid(row=0, column=2, **pad)

        ttk.Label(self.root, text="单元二图片").grid(row=1, column=0, sticky="w", **pad)
        ttk.Entry(self.root, textvariable=self.unit2_var, width=60).grid(row=1, column=1, **pad)
        ttk.Button(self.root, text="选择", command=lambda: self._pick_file(self.unit2_var)).grid(row=1, column=2, **pad)

        ttk.Label(self.root, text="输出文件夹").grid(row=2, column=0, sticky="w", **pad)
        ttk.Entry(self.root, textvariable=self.out_var, width=60).grid(row=2, column=1, **pad)
        ttk.Button(self.root, text="选择", command=self._pick_dir).grid(row=2, column=2, **pad)

        ttk.Label(self.root, text="DPI").grid(row=3, column=0, sticky="w", **pad)
        ttk.Combobox(self.root, textvariable=self.dpi_var, values=list(SUPPORTED_DPI), state="readonly", width=12).grid(row=3, column=1, sticky="w", **pad)

        ttk.Label(self.root, text="重复次数").grid(row=4, column=0, sticky="w", **pad)
        ttk.Combobox(self.root, textvariable=self.repeat_var, values=list(SUPPORTED_REPEAT), state="readonly", width=12).grid(row=4, column=1, sticky="w", **pad)

        ttk.Button(self.root, text="生成生产图", command=self._generate).grid(row=5, column=1, pady=24)

    def _generate(self):
        try:
            tiff, preview, params = run_generate(
                self.unit1_var.get(),
                self.unit2_var.get(),
                self.out_var.get(),
                self.dpi_var.get(),
                self.repeat_var.get(),
            )
            messagebox.showinfo("成功", f"生成完成:\n{tiff}\n{preview}\n{params}")
        except Exception as e:
            self.logger.exception("generate failed")
            messagebox.showerror("错误", str(e))


def main():
    root = tk.Tk()
    AppGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
