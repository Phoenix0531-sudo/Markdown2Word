# Markdown2Word

**Markdown 批量转 Word/PDF 桌面工具：递归目录树、Pandoc 引擎、PySide6 外壳。**

[English](README.md) | [中文](README.zh-CN.md)

[![CI](https://github.com/Phoenix0531-sudo/Markdown2Word/actions/workflows/ci.yml/badge.svg)](https://github.com/Phoenix0531-sudo/Markdown2Word/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

选择含 `.md` 的输入目录，输出 `docx` 或 `pdf`，在输出根下**保留相对目录结构**。转换交给 **Pandoc**（`pypandoc` / helper），本仓库是批量与 UI 壳，不是重写 Pandoc。

## 预览

![Markdown2Word](docs/screenshots/preview.png)

## 核心路径

`converter/batch_converter.py`：`**/*.md` 递归枚举 → 镜像输出路径 → `convert_md_to_any(...)`；可选 `progress_callback`。

PDF 中文路径在 helper 中注入 XeLaTeX + 微软雅黑等变量（需本机 TeX 环境）。

## 安装运行

```bash
git clone https://github.com/Phoenix0531-sudo/Markdown2Word.git
cd Markdown2Word
pip install -r requirements.txt   # 需 PATH 上有 pandoc
python main.py
pytest tests/                     # mock Pandoc，无 GUI
```

Python **>= 3.10**。

## 范围

- **做：** 批量转换、保结构、桌面交互、可选 template  
- **不做：** 云协作编辑器、任意 HTML 的完美排版、多用户 API  

## 许可证

MIT。详见 [LICENSE](LICENSE)。
