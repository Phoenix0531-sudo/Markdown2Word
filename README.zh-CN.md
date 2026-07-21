# Markdown2Word

**基于 PySide6 与 Pandoc 的 Markdown 批量转 Word**

[English](README.md) | [中文](README.zh-CN.md)

![CI](https://github.com/Phoenix0531-sudo/Markdown2Word/actions/workflows/ci.yml/badge.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)

基于 PySide6 与 Pandoc 的 Markdown 批量转 Word。

> 作者：[Phoenix0531-sudo](https://github.com/Phoenix0531-sudo) · 欢迎学习、二次开发与**商业使用**，请保留本仓库署名与许可证声明。

## 技术栈

Python · PySide6 · Pandoc

## 功能特性

- 批量转换
- 桌面 GUI
- Pandoc 管道

## 快速开始

```bash
git clone https://github.com/Phoenix0531-sudo/Markdown2Word.git
cd Markdown2Word
```

```bash
pip install -r requirements.txt
python main.py
```

更完整的英文说明见 [README.md](README.md)。

## 仓库结构（摘要）

```
Markdown2Word/
├─ .github/
├─ config/
├─ converter/
├─ docs/
├─ scripts/
├─ ui/
├─ utils/
├─ CHANGELOG.md
├─ Dockerfile
├─ LICENSE
├─ main.py
├─ README.md
├─ README.zh-CN.md
├─ requirements.txt
```

## 测试

```bash
pip install pytest
pytest -q
```

仓库内 `tests/` 至少包含 smoke 测试；有完整测试套件时以 CI 为准。

## CI

GitHub Actions（`push` / `pull_request`）会：

- 安装依赖（requirements / pyproject）
- 运行 `pytest`（**硬失败**）
- 尽力做语法/结构检查

## 许可证

[MIT](LICENSE) — 可自由使用、修改、分发与**商用**，需保留版权与许可声明（提及本仓库 / 作者即可）。

## 关于

维护者：[Phoenix0531-sudo](https://github.com/Phoenix0531-sudo)
