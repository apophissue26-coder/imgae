窗帘印花裂变生产系统 V3（框架版）

1) 这是 V3 框架版。
2) 这不是拼接工具。
3) 核心流程：原始图 → 印花提取 → 三方向裂变 → 效果图 → 生产线/展示线。
4) 当前 AI 部分为 mock 占位。
5) 默认生产排版模式：竖向 1-2-1-2 生产排版模式。
6) 当前默认不使用中线裁切。
7) 运行源码：python gui.py
8) 打包方式：双击 build_exe.bat
9) EXE 输出：dist/窗帘印花裂变生产系统V3.exe

历史错误说明（仅用于纠错记录）：
- “一块布=左右两片窗帘”是旧错误逻辑，当前默认不使用。

后续真实 AI 接入位置：
- core/ai_provider.py
  - analyze_reference
  - extract_pattern
  - generate_variations
  - render_effect_images
  - enhance_hd
