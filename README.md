<div align="center">

# Markdown2Word

**专业级批量 Markdown 转 Word 桌面应用 | Batch Markdown to Word Converter**

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![PySide6](https://img.shields.io/badge/PySide-6.4%2B-green)
![QtWebEngine](https://img.shields.io/badge/QtWebEngine-6.4%2B-orange)
![Pandoc](https://img.shields.io/badge/Pandoc-3.0%2B-red)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)

</div>

基于 PySide6 和 Pandoc 的高保真批量 Markdown 转 Word 桌面工具，支持多格式导出、实时预览、自定义模板和深色主题。

> A professional desktop application for batch converting Markdown files to Word, PDF, HTML, and RTF formats. Built with PySide6 and Pandoc, featuring a dark Apple-style GUI, real-time preview, and custom template support.

---

## 技术特性 | Features

| 中文特性 | English Feature | 说明 / Description |
|---------|----------------|-------------------|
| 批量转换 | Batch Conversion | 支持单文件、多文件、文件夹递归批量转换 |
| 多格式导出 | Multi-Format Export | Word (.docx), PDF, HTML, RTF |
| 自定义模板 | Custom Templates | 支持 Word 模板 (.docx) 自定义样式 |
| Markdown 预览 | Live Preview | 内置 QtWebEngine 实时渲染 Markdown |
| 深色主题 | Dark Theme | 极简苹果风深色 GUI，统一圆角卡片风格 |
| 拖放支持 | Drag-and-Drop | 拖放文件/文件夹自动识别 Markdown 文件 |
| 进度提示 | Progress Tracking | 进度条、状态栏实时提示、完成后打开输出目录 |
| 日志系统 | Logging | 深色终端风格控制台日志，支持分级与导出 |
| 配置持久化 | Config Persistence | 自动保存/恢复输入输出目录、导出格式等 |
| 异常处理 | Error Handling | 所有操作异常捕获与友好提示 |

---

## 目录 | Table of Contents

- [数据准备 | Data Preparation](#数据准备--data-preparation)
- [核心原理 | Core Method](#核心原理--core-method)
- [模块文档 | Module Reference](#模块文档--module-reference)
- [快速开始 | Quick Start](#快速开始--quick-start)
- [输出说明 | Output](#输出说明--output)
- [安装与运行 | Installation](#安装与运行--installation)
- [Docker 使用 | Docker Usage](#docker-使用--docker-usage)
- [项目结构 | Project Structure](#项目结构--project-structure)
- [引用 | Citation](#引用--citation)
- [许可证 | License](#许可证--license)

---

## 数据准备 | Data Preparation

本工具需要输入 Markdown (.md) 文件。无需特定格式约束，兼容主流 Markdown 语法（GFM 标准）。

Pandoc CLI 是运行时必要依赖，需预先安装。可选的 Word 模板文件 (.docx) 可用于自定义输出样式。

> This tool requires Markdown (.md) files as input. It is compatible with standard GFM syntax. Pandoc CLI must be pre-installed as a runtime dependency. Optional Word templates (.docx) can customize output styles.

---

## 核心原理 | Core Method

Markdown2Word 底层基于 Pandoc 实现文档格式转换。Pandoc 是一个通用文档转换工具，支持 Markdown、Word、HTML、LaTeX、PDF 等多种格式之间的相互转换。

工作流程：

1. 用户选择输入文件（单个/多个/文件夹）
2. 工具遍历 Markdown 文件并调用 pandoc 进行转换
3. 转换结果输出到指定目录
4. PySide6 提供实时进度反馈和内置 Markdown 预览

> Markdown2Word uses Pandoc as its conversion engine. Pandoc is a universal document converter supporting Markdown, Word, HTML, LaTeX, PDF, and many other formats.

---

## 模块文档 | Module Reference

| 模块 | 功能 |
|------|------|
| `main.py` | 应用入口，初始化 QApplication 和主窗口 |
| `ui/main_window.py` | 主界面逻辑，文件选择、拖放、进度条、日志 |
| `ui/widgets.py` | 自定义控件，苹果风标题栏（三色按钮） |
| `ui/style.qss` | 深色主题 QSS 样式表 |
| `converter/pandoc_helper.py` | Pandoc 调用封装，支持自定义模板和参数 |
| `converter/batch_converter.py` | 批量转换逻辑，支持进度回调 |
| `config/settings.py` | 用户设置持久化（输入/输出目录、格式等） |
| `utils/logger.py` | 日志系统，支持分级和导出 |

---

## 快速开始 | Quick Start

### 前置条件

1. 安装 Pandoc CLI：https://pandoc.org/installing.html
2. 确认 pandoc 已加入系统 PATH

### 启动

```bash
pip install -r requirements.txt
python main.py
```

### 使用流程

1. 启动程序，选择单个/多个 Markdown 文件或文件夹（支持拖放）
2. 在右侧选择输出格式和输出目录
3. 可选：挂载自定义 Word 模板
4. 点击"开始转换"，实时查看进度
5. 转换完成后可一键打开输出目录

---

## 输出说明 | Output

支持以下输出格式：

| 格式 | 文件后缀 | 说明 |
|------|---------|------|
| Word | .docx | 默认格式，支持自定义模板 |
| PDF | .pdf | 需要系统安装 LaTeX (MiKTeX/TeX Live) |
| HTML | .html | 独立网页文件 |
| RTF | .rtf | 富文本格式 |

---

## 安装与运行 | Installation

### 系统要求

- Python 3.8 或更高版本
- PySide6 6.4+
- Pandoc CLI（必须单独安装）
- Windows 7+ / Linux / macOS

### 依赖安装

```bash
pip install -r requirements.txt
```

### Pandoc 安装

- Windows：从 https://pandoc.org/installing.html 下载安装包
- macOS：`brew install pandoc`
- Linux：`sudo apt install pandoc`

### 运行

```bash
python main.py
```

---

## Docker 使用 | Docker Usage

Markdown2Word 是 PySide6 桌面 GUI 应用，Docker 环境主要用于**构建验证和依赖安装测试**，不适合作为主要的 GUI 运行方式。Docker 镜像包含 pandoc CLI，但 QtWebEngine 渲染在容器中不可用。

> Markdown2Word is a PySide6 desktop GUI application. The Docker environment is intended for **build verification and dependency testing only**. The image includes pandoc CLI, but QtWebEngine rendering is unavailable in the container.

```bash
# 构建镜像
docker build -t markdown2word .

# 验证导入和 pandoc 版本
docker run --rm markdown2word
```

---

## 项目结构 | Project Structure

```
Markdown2Word/
├── main.py                  # 应用入口
├── requirements.txt         # Python 依赖
├── Dockerfile               # Docker 构建文件
├── LICENSE                  # MIT 许可证
├── .gitignore               # Git 忽略规则
├── .editorconfig            # 编辑器配置
├── CHANGELOG.md             # 变更日志
├── README.md                # 项目说明
├── scripts/
│   └── docker_smoke_test.py # Docker 导入验证脚本
├── docs/
│   └── index.md             # GitHub Pages 入口
├── config/
│   └── settings.py          # 用户设置持久化
├── converter/
│   ├── pandoc_helper.py     # Pandoc 封装
│   └── batch_converter.py   # 批量转换逻辑
├── ui/
│   ├── main_window.py       # 主窗口
│   ├── widgets.py           # 自定义控件
│   └── style.qss            # 深色主题样式
├── utils/
│   └── logger.py            # 日志系统
└── main.spec                # PyInstaller 打包配置
```

---

## 引用 | Citation

```bibtex
@software{markdown2word2026,
  title = {Markdown2Word: Batch Markdown to Word Converter},
  year = {2026},
  url = {https://github.com/Phoenix0531-sudo/Markdown2Word}
}
```

---

## 许可证 | License

本项目基于 MIT 许可证开源。详见 [LICENSE](LICENSE) 文件。

> This project is open-sourced under the MIT License. See the [LICENSE](LICENSE) file for details.

---

<div align="center"><strong>Made for the technical writing and academic community</strong></div>
