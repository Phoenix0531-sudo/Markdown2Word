# Markdown2Word

**基于 Pandoc + PySide6 的 Markdown 批量转 Word/PDF 桌面工具。**

[English](README.md) | [中文](README.zh-CN.md)

[![CI](https://github.com/Phoenix0531-sudo/Markdown2Word/actions/workflows/ci.yml/badge.svg)](https://github.com/Phoenix0531-sudo/Markdown2Word/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)

基于 Pandoc + PySide6 的 Markdown 批量转 Word/PDF 桌面工具。

选文件夹 · 保留目录树 · 中文 PDF（XeLaTeX + 雅黑）。


## 功能

- 📂 批量转换目录树中的 `.md`
- 📄 Pandoc 驱动输出（常用 **docx** / **pdf**）
- 🌲 输出根下保留嵌套目录结构
- 🈶 PDF 路径注入 XeLaTeX + 微软雅黑变量
- 🧩 可选 Pandoc `--template`
- 🧪 CI 用 mock Pandoc 的纯测试 — 不需要 GUI

## 快速开始

### 安装

```bash
git clone https://github.com/Phoenix0531-sudo/Markdown2Word.git
cd Markdown2Word
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
# requires Pandoc on PATH; PDF needs XeLaTeX + YaHei for Chinese
```

### 使用

```bash
python main.py
```

```python
from converter.batch_converter import batch_convert
batch_convert("path/to/md_root", "path/to/out", fmt="docx")
```

## 项目结构

```
main.py
converter/   # pandoc_helper + batch_converter
ui/
tests/
```

## 说明

不是所见即所得 Markdown IDE，也不是多用户转换 API。

## 许可证

MIT。在注明出处的前提下可商业使用（以 LICENSE 为准）。详见 [LICENSE](LICENSE)。
