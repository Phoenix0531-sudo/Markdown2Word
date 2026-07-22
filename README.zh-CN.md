# Markdown2Word

**批量 Markdown 转 Word/PDF 桌面工具（PySide6 + Pandoc）**

[English](README.md) | [中文](README.zh-CN.md)

![CI](https://github.com/Phoenix0531-sudo/Markdown2Word/actions/workflows/ci.yml/badge.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)

Markdown2Word 是一个**桌面端批量转换工具**：选择含 `.md` 的目录、选定输出格式，底层用 **Pandoc**，界面用 PySide6。PDF 走 XeLaTeX，并优先使用**微软雅黑**以改善中文排版。

它是本地生产力工具，不是云服务，也不是完整 Markdown IDE。

## 为什么做这个

命令行 Pandoc 很强，但不适合“整夹批量、嵌套目录、中文 PDF”的日常操作。本工具把同一引擎包进小 GUI，做到「选目录 → 转换」。

## 功能

- 递归批量转换 Markdown
- 输出格式由 Pandoc 决定（常用 **docx** / **pdf**）
- 输出目录保留相对路径结构
- PDF 自动加 `--pdf-engine=xelatex` 与雅黑字体变量
- 可选 Pandoc `--template`

## 环境要求

- 建议 Python 3.10+
- 系统 `PATH` 中有 [Pandoc](https://pandoc.org/)
- 出 PDF 需要带 XeLaTeX 的 TeX 发行版；中文 PDF 需本机有雅黑等字体

## 安装

```bash
git clone https://github.com/Phoenix0531-sudo/Markdown2Word.git
cd Markdown2Word
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate
pip install -r requirements.txt
```

## 使用

图形界面：

```bash
python main.py
```

无界面批量：

```python
from converter.batch_converter import batch_convert

batch_convert("path/to/md_root", "path/to/out", fmt="docx")
```

单文件：

```python
from converter.pandoc_helper import convert_md_to_any

convert_md_to_any("note.md", "note.docx", "docx")
convert_md_to_any("note.md", "note.pdf", "pdf")
```

## 目录结构

```
main.py              # Qt 入口
converter/           # pandoc 封装与批量逻辑
ui/                  # 主窗口
tests/               # 业务测（批量发现、PDF 参数；mock pandoc）
```

## 明确不做

- 不是所见即所得编辑器
- 不是多用户转换服务
- PDF 效果仍取决于本机 TeX 与字体

## 许可证

MIT。可在署名前提下商用。见 [LICENSE](LICENSE)。
