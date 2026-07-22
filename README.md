# Markdown2Word

**Batch Markdown → Word/PDF desktop app (PySide6 + Pandoc)**

[English](README.md) | [中文](README.zh-CN.md)

![CI](https://github.com/Phoenix0531-sudo/Markdown2Word/actions/workflows/ci.yml/badge.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)

Markdown2Word is a **desktop batch converter**: pick a folder of `.md` files, choose an output format, and convert with **Pandoc** under a simple PySide6 UI. PDF export uses XeLaTeX and prefers **Microsoft YaHei** for Chinese text.

It is a local productivity tool, not a cloud service and not a full Markdown IDE.

## Why this exists

Command-line Pandoc is powerful but awkward for non-technical batch jobs (nested folders, mixed docx/pdf, Chinese PDF fonts). This app wraps the same engine in a small GUI so “select folder → convert” works without memorizing flags.

## Features

- Batch convert a directory tree of Markdown files
- Output formats driven by Pandoc (commonly **docx** and **pdf**)
- Nested folder structure preserved under the output root
- PDF path injects `--pdf-engine=xelatex` and YaHei font variables
- Optional document template via Pandoc `--template`

## Requirements

- Python 3.10+ recommended
- [Pandoc](https://pandoc.org/) on `PATH`
- For PDF: a TeX engine with XeLaTeX (e.g. TeX Live / MiKTeX) and YaHei installed if you need Chinese PDF

## Install

```bash
git clone https://github.com/Phoenix0531-sudo/Markdown2Word.git
cd Markdown2Word
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

GUI:

```bash
python main.py
```

Programmatic batch (no GUI), from a small helper:

```python
from converter.batch_converter import batch_convert

batch_convert("path/to/md_root", "path/to/out", fmt="docx")
```

Single-file helper:

```python
from converter.pandoc_helper import convert_md_to_any

convert_md_to_any("note.md", "note.docx", "docx")
convert_md_to_any("note.md", "note.pdf", "pdf")  # xelatex + YaHei args
```

## Project layout

```
main.py              # Qt entry
converter/           # pandoc_helper + batch_converter
ui/                  # main window
tests/               # pure tests (batch discovery, PDF args; pandoc mocked)
```

## What this is not

- Not a WYSIWYG Markdown editor
- Not a server / multi-user conversion API
- PDF quality still depends on your local TeX + font setup

## License

MIT. Free for commercial use with attribution. See [LICENSE](LICENSE).
