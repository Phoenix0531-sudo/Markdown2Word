# Markdown2Word

**Markdown 批量转 Word/PDF：Pandoc 引擎 + PySide6 外壳。**

[English](README.md) | [中文](README.zh-CN.md)

[![CI](https://github.com/Phoenix0531-sudo/Markdown2Word/actions/workflows/ci.yml/badge.svg)](https://github.com/Phoenix0531-sudo/Markdown2Word/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

选文件夹，保留目录树；中文 PDF 走 XeLaTeX + 雅黑。

## 预览

![Markdown2Word](docs/screenshots/preview.png)

## 功能

- 批量转换目录树中的 .md
- Pandoc 驱动 docx / pdf 输出
- 输出根下保留嵌套目录
- PDF 路径注入 XeLaTeX + 微软雅黑
- CI 用 mock Pandoc，不需要 GUI

## 快速开始

### 安装

```bash
git clone https://github.com/Phoenix0531-sudo/Markdown2Word.git
cd Markdown2Word
pip install -r requirements.txt
# Pandoc on PATH; Chinese PDF needs XeLaTeX + YaHei
```

### 使用

```bash
python main.py
```

```python
from converter.batch_converter import batch_convert
batch_convert("md_root", "out", fmt="docx")
```

## 项目结构

```
main.py
converter/  ui/
tests/
```

## 说明

不是所见即所得 Markdown IDE，也不是多用户转换 API。

## 许可证

MIT。在注明出处的前提下可商业使用（以 LICENSE 为准）。详见 [LICENSE](LICENSE)。
