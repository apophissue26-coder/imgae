# curtain-image-generator-v1

一个可在 Windows 上运行的简单图片生成工具（Streamlit Web 界面）。

## 功能

- Python + Streamlit
- 支持上传参考图：`jpg / png / webp`
- 支持输入中文提示词
- 调用 OpenAI Images API（默认 `gpt-image-1`）
- 支持生成 `1 / 2 / 4` 张
- 支持比例：`1024x1024`、`1024x1536`、`1536x1024`
- 支持质量：`auto`、`high`、`medium`、`low`
- 自动保存到 `outputs` 文件夹
- 自动命名：`生成时间_序号.png`（示例：`20260509_083000_1.png`）
- 页面显示生成结果并提供下载按钮

> 本项目仅用于高清视觉效果图生成，不包含生产图、TIF、无缝检测、DPI 等流程。

---

## 1) 环境准备（Windows）

建议 Python 3.10+。

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

---

## 2) 设置 OPENAI_API_KEY

### 方式 A：临时设置（当前终端有效）

```bat
set OPENAI_API_KEY=你的密钥
```

### 方式 B：永久设置（推荐）

```bat
setx OPENAI_API_KEY "你的密钥"
```

设置后请重新打开终端。

---

## 3) 运行项目

### 方法 1：命令行

```bash
streamlit run app.py
```

### 方法 2：双击 `run.bat`

`run.bat` 会自动创建虚拟环境（如不存在）、安装依赖并启动 Streamlit。

---

## 4) 使用说明

1. 输入 `OPENAI_API_KEY`（或先在系统环境变量设置）。
2. 上传参考图片（jpg/png/webp）。
3. 输入中文提示词。
4. 选择生成张数、比例、质量。
5. 点击“开始生成”。
6. 结果会显示在页面中，并保存到 `outputs/`，每张图可单独下载。

