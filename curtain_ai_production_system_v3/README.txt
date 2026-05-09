窗帘印花裂变生产系统 V3（curtain_ai_production_system_v3）

1) 这是 V3 框架版。
2) 这不是拼接工具。
3) 核心流程：原始图 → 印花提取 → 三方向裂变 → 效果图 → 生产线/展示线。
4) 当前 AI 部分是 mock 占位。
5) 生产排版默认是：竖向 1-2-1-2 生产排版模式。
6) 不默认使用中线裁切（旧逻辑，当前默认不使用）。

运行源码：
python gui.py

打包：
双击 build_exe.bat

EXE 输出位置：
dist/窗帘印花裂变生产系统V3.exe

导出路径说明：
- 所有导出文件统一写入 EXE 同目录下的 output 文件夹。
- 源码运行时写入项目目录下 output 文件夹。

输出目录关键文件：
- output/analysis_report.txt
- output/extracted_pattern.png
- output/variations/
- output/selected_effects/
- output/production/
- output/export_params.txt
