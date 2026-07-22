# Markdown2Word

**Batch Markdown → Word/PDF desktop converter powered by Pandoc + PySide6.**

[English](README.md) | [中文](README.zh-CN.md)

[![CI](https://github.com/Phoenix0531-sudo/Markdown2Word/actions/workflows/ci.yml/badge.svg)](https://github.com/Phoenix0531-sudo/Markdown2Word/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)

Batch Markdown → Word/PDF desktop converter powered by Pandoc + PySide6.

Select folder. Convert tree. Chinese PDF via XeLaTeX + YaHei.


## Features

- 📂 Batch convert a directory tree of `.md` files
- 📄 Output formats driven by Pandoc (commonly **docx** / **pdf**)
- 🌲 Nested folder structure preserved under the output root
- 🈶 PDF path injects XeLaTeX + Microsoft YaHei variables
- 🧩 Optional Pandoc `--template`
- 🧪 Pure tests with Pandoc mocked — no GUI required on CI

## Get started

### Install

```bash
git clone https://github.com/Phoenix0531-sudo/Markdown2Word.git
cd Markdown2Word
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
# requires Pandoc on PATH; PDF needs XeLaTeX + YaHei for Chinese
```

### Usage

```bash
python main.py
```

```python
from converter.batch_converter import batch_convert
batch_convert("path/to/md_root", "path/to/out", fmt="docx")
```

## Project layout

```
main.py
converter/   # pandoc_helper + batch_converter
ui/
tests/
```

## Notes

Not a WYSIWYG Markdown IDE and not a multi-user conversion API.

## License

MIT. Free for commercial use with attribution where applicable. See [LICENSE](LICENSE).
