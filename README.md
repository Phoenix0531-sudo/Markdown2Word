# Markdown2Word

**Batch Markdown to Word/PDF converter: Pandoc engine with a PySide6 shell.**

[English](README.md) | [中文](README.zh-CN.md)

[![CI](https://github.com/Phoenix0531-sudo/Markdown2Word/actions/workflows/ci.yml/badge.svg)](https://github.com/Phoenix0531-sudo/Markdown2Word/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Folder in, tree preserved, Chinese PDF via XeLaTeX + YaHei.

## Preview

![Markdown2Word](docs/screenshots/preview.png)

## Features

- Batch convert directory trees of .md files
- DOCX / PDF outputs driven by Pandoc
- Nested folder structure preserved under the output root
- PDF path injects XeLaTeX + Microsoft YaHei variables
- CI tests mock Pandoc (no GUI required)

## Get started

### Install

```bash
git clone https://github.com/Phoenix0531-sudo/Markdown2Word.git
cd Markdown2Word
pip install -r requirements.txt
# Pandoc on PATH; Chinese PDF needs XeLaTeX + YaHei
```

### Usage

```bash
python main.py
```

```python
from converter.batch_converter import batch_convert
batch_convert("md_root", "out", fmt="docx")
```

## Project layout

```
main.py
converter/  ui/
tests/
```

## Notes

Not a WYSIWYG Markdown IDE and not a multi-user conversion API.

## License

MIT. Free for commercial use with attribution where applicable. See [LICENSE](LICENSE).
