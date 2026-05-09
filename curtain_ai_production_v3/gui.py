import logging
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from app import run_pipeline, generate_outputs
from config import APP_NAME, OUTPUT_DIR, LOG_DIR, DPI_OPTIONS, DEFAULT_DPI, REPEAT_OPTIONS, DEFAULT_REPEAT, DEFAULT_WIDTH_CM, DEFAULT_HEIGHT_CM

class GUI:
    def __init__(self, root):
        self.root = root
        root.title(APP_NAME)
        root.geometry('920x620')
        self.state = None
        self.source = tk.StringVar()
        self.out = tk.StringVar(value=str(OUTPUT_DIR))
        self.dpi = tk.IntVar(value=DEFAULT_DPI)
        self.repeat = tk.IntVar(value=DEFAULT_REPEAT)
        self.wcm = tk.DoubleVar(value=DEFAULT_WIDTH_CM)
        self.hcm = tk.DoubleVar(value=DEFAULT_HEIGHT_CM)
        self._init_log(); self._ui()

    def _init_log(self):
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger('v3'); self.logger.setLevel(logging.ERROR)
        if not self.logger.handlers:
            fh = logging.FileHandler(LOG_DIR / 'error.log', encoding='utf-8')
            self.logger.addHandler(fh)

    def _ui(self):
        ttk.Entry(self.root, textvariable=self.source, width=80).grid(row=0, column=0, padx=8, pady=8)
        ttk.Button(self.root, text='上传原始图', command=self.pick_source).grid(row=0, column=1)
        ttk.Button(self.root, text='自动分析+裂变', command=self.analyze).grid(row=1, column=1)
        self.analysis_box = tk.Text(self.root, height=8, width=110); self.analysis_box.grid(row=2, column=0, columnspan=3, padx=8)

        self.listbox = tk.Listbox(self.root, width=50, height=6); self.listbox.grid(row=3, column=0, padx=8, pady=8)
        ttk.Button(self.root, text='选择方案', command=self.choose).grid(row=3, column=1)

        ttk.Label(self.root, text='DPI').grid(row=4, column=0, sticky='w', padx=8)
        ttk.Combobox(self.root, textvariable=self.dpi, values=DPI_OPTIONS, state='readonly').grid(row=4, column=0)
        ttk.Label(self.root, text='重复次数').grid(row=4, column=1)
        ttk.Combobox(self.root, textvariable=self.repeat, values=REPEAT_OPTIONS, state='readonly').grid(row=4, column=1, padx=70)
        ttk.Label(self.root, text='宽cm/高cm').grid(row=5, column=0, sticky='w', padx=8)
        ttk.Entry(self.root, textvariable=self.wcm, width=8).grid(row=5, column=0, padx=70, sticky='w')
        ttk.Entry(self.root, textvariable=self.hcm, width=8).grid(row=5, column=0, padx=140, sticky='w')

        ttk.Button(self.root, text='生成生产图/展示图并导出', command=self.generate).grid(row=6, column=0, pady=15)

    def pick_source(self):
        p = filedialog.askopenfilename(title='选择原始图')
        if p: self.source.set(p)

    def analyze(self):
        try:
            self.state = run_pipeline(Path(self.source.get()), Path(self.out.get()), self.dpi.get(), self.repeat.get(), self.wcm.get(), self.hcm.get())
            self.analysis_box.delete('1.0', tk.END)
            self.analysis_box.insert(tk.END, str(self.state.analysis))
            self.listbox.delete(0, tk.END)
            for i, v in enumerate(self.state.variations):
                self.listbox.insert(i, f"{v.name} | {v.direction} | {v.description}")
        except Exception as e:
            self.logger.exception('analyze error'); messagebox.showerror('错误', str(e))

    def choose(self):
        if not self.state: return
        idx = self.listbox.curselection()
        if not idx: return
        self.state.selected_variation = self.state.variations[idx[0]]
        messagebox.showinfo('已选择', self.state.selected_variation.name)

    def generate(self):
        try:
            effect, showcase, prod, record = generate_outputs(self.state, Path(self.out.get()), self.dpi.get(), self.repeat.get(), self.wcm.get(), self.hcm.get())
            messagebox.showinfo('完成', f'效果图: {effect}\n展示图数量: {len(showcase)}\n生产图: {prod}\n参数: {record}')
        except Exception as e:
            self.logger.exception('generate error'); messagebox.showerror('错误', str(e))


def main():
    r = tk.Tk(); GUI(r); r.mainloop()

if __name__ == '__main__':
    main()
