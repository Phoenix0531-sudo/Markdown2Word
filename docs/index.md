# Markdown2Word

<div align="center">

Batch Markdown to Word converter with Apple-style PySide6 GUI.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![PySide6](https://img.shields.io/badge/PySide-6.4%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

</div>

## Overview

A professional desktop application for batch converting Markdown files to Word (.docx), PDF, HTML, and RTF formats. Built with PySide6 and Pandoc.

## Requirements

- Python 3.8+
- Pandoc CLI (install separately or use Docker)

## Quick Start

```bash
pip install -r requirements.txt
python main.py
```

## Docker

```bash
docker build -t markdown2word .
docker run --rm markdown2word
```

*Docker is for build verification only; GUI requires a native display.*

## Repository

<https://github.com/Phoenix0531-sudo/Markdown2Word>

## License

MIT License
