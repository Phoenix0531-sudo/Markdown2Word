# Markdown2Word —— 专业级批量 Markdown 转 Word 桌面应用

## 项目简介

**Markdown2Word** 是一款基于 PySide6 + Pandoc 的高保真、极简苹果风格的批量 Markdown 转 Word 工具。  
支持单文件、多文件、文件夹批量转换，支持 Word（.docx）、PDF、HTML、RTF 多格式导出，支持自定义模板、实时预览、日志导出、配置持久化、异常处理等。界面极简美观，交互流畅，适合技术文档、学术论文、报告等场景。

---

## 主要特性

- **高保真批量转换**：支持单文件、多文件、文件夹递归批量转换，底层调用 Pandoc，兼容主流 Markdown 语法。
- **多格式导出**：支持 Word（.docx）、PDF、HTML、RTF 等多种格式。
- **自定义模板**：支持 Word 模板（.docx），可自定义样式，模板可预览。
- **极简苹果风深色 GUI**：全局深色主题，主色#181C23，内容区#23272E，分割线#2C313A，主高亮#34C759，圆角卡片风格。
- **三色按钮右上角**：苹果风三色按钮（黄-最小化，绿-最大化/还原，红-关闭）位于右上角，色彩统一，交互自然。
- **批量管理与拖放**：支持拖放文件/文件夹，自动识别 Markdown 文件，文件列表支持多选、批量移除、右键菜单。
- **实时预览**：内置 QWebEngineView 实时渲染 Markdown，支持字体缩放，预览区圆角美化。
- **进度与状态提示**：美化进度条，状态栏实时提示，转换完成可自动打开输出目录。
- **日志系统**：外置控制台日志窗口，深色终端风格，支持 info/warning/error 分级，日志可导出 txt。
- **配置持久化**：自动保存/恢复输入/输出目录、导出格式等。
- **异常处理**：所有操作均有异常捕获与友好提示，日志记录详细。
- **控件圆角/间距/字体统一**：所有按钮、输入框、列表、进度条等圆角、间距、字体风格高度统一。
- **窗口拖动优化**：自定义标题栏区域可拖动，体验流畅。
- **其它细节**：窗口四周留白，内容区圆角，分割线细腻，支持多平台。

---

## 目录结构

```
Markdown2Word/
├── main.py # 程序入口
├── config/
│ └── settings.py # 用户设置持久化
├── converter/
│ ├── batch_converter.py # 批量转换逻辑
│ └── pandoc_helper.py # Pandoc 调用封装
├── resources/
│ └── templates/ # Word模板及预览图
├── ui/
│ ├── main_window.py # 主窗口与界面逻辑
│ ├── widgets.py # 自定义控件（标题栏等）
│ └── style.qss # 深色主题 QSS
├── utils/
│ └── logger.py # 日志系统
├── requirements.txt # 依赖列表
└── README.md # 项目说明

---

## 主要文件说明

- **main.py**：程序入口，创建 QApplication 实例并加载主窗口。
- **config/settings.py**：用户设置的持久化与加载（如上次使用的目录、导出格式等）。
- **converter/pandoc_helper.py**：封装 Pandoc 的 Python 调用，支持自定义模板、参数扩展。
- **converter/batch_converter.py**：遍历文件夹、批量调用转换，支持进度回调。
- **ui/main_window.py**：主界面逻辑，包含三色按钮、文件选择、拖放、右键菜单、进度条、日志、批量转换等。
- **ui/widgets.py**：自定义苹果风格标题栏（右上角三色按钮、拖动信号）。
- **ui/style.qss**：深色主题 QSS，统一控件圆角、字体、间距、进度条美化、输入框高亮等。
- **utils/logger.py**：日志系统，支持分级与导出。

---

## 安装与运行

1. **安装 Pandoc**  
   [下载 Pandoc](https://pandoc.org/installing.html) 并配置到系统 PATH。

2. **安装 Python 依赖**  
   ```bash
   pip install -r requirements.txt
   ```

3. **运行主程序**  
   ```bash
   python main.py
   ```

---

## 典型使用流程

1. 启动程序，选择单个/多个 Markdown 文件或整个文件夹（支持拖放）。
2. 右键文件列表可打开文件夹、移除、清空。
3. 选择输出文件夹、导出格式、Word模板（可自定义）。
4. 点击"开始转换"，实时查看进度与状态。
5. 转换完成后可一键打开输出目录，日志可导出。

---

## 依赖环境

- Python 3.8+
- PySide6
- PySide6-WebEngine
- pypandoc
- Pandoc（需单独安装）
- markdown

---

## 常见问题

- **PDF 导出失败**：需安装 LaTeX（如 MiKTeX/TeX Live）。
- **依赖安装慢/失败**：建议使用国内镜像。
- **转换报错**：请检查 Pandoc 是否安装并配置到 PATH，或查看日志窗口详细信息。

---

## 特色亮点

- 极简苹果风深色主题，三色按钮右上角，控件圆角/间距/字体高度统一。
- 控制台深色终端风格，批量高保真转换，支持多格式导出与模板。
- 拖放、右键、日志导出、配置持久化等现代桌面体验。
- 代码结构清晰，易于维护和扩展。

---

## 后续可扩展方向

- Word 样式与模板高级定制
- CLI/命令行批量转换
- 文件/目录监控与自动转换
- 云端/团队协作、国际化、插件机制等

---

## 致谢

- [Pandoc](https://pandoc.org/)
- [PySide6](https://doc.qt.io/qtforpython/)
- [pypandoc](https://pypi.org/project/pypandoc/)

---

如需定制或遇到问题，欢迎提交 issue！