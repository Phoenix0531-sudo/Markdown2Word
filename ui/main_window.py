from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QSplitter, QListWidget, QPushButton, QLabel,
    QFileDialog, QProgressBar, QHBoxLayout, QMenu, QStatusBar, QComboBox, QTextEdit, QDockWidget, QMessageBox, QSizePolicy
)
from PySide6.QtGui import QAction, QPixmap, QIcon
from PySide6.QtCore import Qt, QThreadPool, QRunnable, Signal, QObject, QPoint, QSize
from converter.batch_converter import batch_convert
from .widgets import MacTitleBar
import os
from PySide6.QtWebEngineWidgets import QWebEngineView
import markdown

# ========== 新增：信号对象 ==========
class WorkerSignals(QObject):
    progress = Signal(int, int, str)
    error = Signal(str)
    finished = Signal()
    batch_finished = Signal()
    stopped = Signal()

# ========== 新增：转换任务 ==========
class ConvertTask(QRunnable):
    def __init__(self, idx, total, md_file, output_dir, template, out_fmt, ext, signals, stop_flag):
        super().__init__()
        self.idx = idx
        self.total = total
        self.md_file = md_file
        self.output_dir = output_dir
        self.template = template
        self.out_fmt = out_fmt
        self.ext = ext
        self.signals = signals
        self.stop_flag = stop_flag

    def run(self):
        if self.stop_flag["stop"]:
            self.signals.stopped.emit()
            return
        try:
            import os
            from converter.pandoc_helper import convert_md_to_any
            base = os.path.basename(self.md_file)
            out_path = os.path.join(self.output_dir, os.path.splitext(base)[0] + self.ext)
            convert_md_to_any(self.md_file, out_path, self.out_fmt, self.template)
            self.signals.progress.emit(self.idx, self.total, self.md_file)
        except Exception as e:
            self.signals.error.emit(f"{self.md_file} 转换失败: {e}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Markdown 批量转 Word")
        self.setGeometry(100, 100, 1200, 800)
        self.is_dark = False
        self.setStyleSheet(open("ui/style.qss", encoding="utf-8").read())
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAcceptDrops(True)
        self.setMinimumSize(900, 600)

        # 把 theme_btn 作为参数传给 MacTitleBar
        self.title_bar = MacTitleBar(self)
        self.title_bar.close_signal.connect(self.close)
        self.title_bar.minimize_signal.connect(self.showMinimized)
        self.title_bar.maximize_signal.connect(self.toggle_max_restore)
        self.title_bar.drag_signal.connect(self.move_window)

        # 主体
        central = QWidget()
        central.setObjectName("centralwidget")
        vbox = QVBoxLayout(central)
        vbox.setContentsMargins(0,0,0,0)
        vbox.setSpacing(0)
        vbox.addWidget(self.title_bar)

        splitter = QSplitter(Qt.Orientation.Horizontal)

        # 左侧：文件选择与文件列表
        left = QWidget()
        left_layout = QVBoxLayout(left)
        left_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.input_file_btn = QPushButton("选择单个Markdown文件")
        self.input_file_btn.setFixedWidth(260)
        self.input_file_btn.setStyleSheet("margin-top: 12px; font-size: 15px; padding: 8px 16px; font-family: 'San Francisco', '微软雅黑', Arial;")
        self.input_file_btn.clicked.connect(self.choose_single_file)
        self.input_files_btn = QPushButton("选择多个Markdown文件")
        self.input_files_btn.setFixedWidth(260)
        self.input_files_btn.setStyleSheet("font-size: 15px; padding: 8px 16px; font-family: 'San Francisco', '微软雅黑', Arial;")
        self.input_files_btn.clicked.connect(self.choose_multi_files)
        self.input_dir_btn = QPushButton("选择Markdown文件夹")
        self.input_dir_btn.setFixedWidth(260)
        self.input_dir_btn.setStyleSheet("font-size: 15px; padding: 8px 16px; font-family: 'San Francisco', '微软雅黑', Arial;")
        self.input_dir_btn.clicked.connect(self.choose_input_dir)
        self.file_list = QListWidget()
        self.file_list.setMinimumWidth(180)
        self.file_list.setMaximumWidth(320)
        self.file_list.setStyleSheet("margin-top: 8px;")
        self.file_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.file_list.customContextMenuRequested.connect(self.show_file_list_menu)
        self.file_list.currentItemChanged.connect(self.update_preview)
        left_layout.addWidget(self.input_file_btn, alignment=Qt.AlignmentFlag.AlignHCenter)
        left_layout.addWidget(self.input_files_btn, alignment=Qt.AlignmentFlag.AlignHCenter)
        left_layout.addWidget(self.input_dir_btn, alignment=Qt.AlignmentFlag.AlignHCenter)
        left_layout.addWidget(self.file_list)

        # 中间：导出设置与进度
        center = QWidget()
        center_layout = QVBoxLayout(center)
        center_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.output_btn = QPushButton("选择输出文件夹")
        self.output_btn.setFixedWidth(220)
        self.output_btn.clicked.connect(self.choose_output)
        self.export_btn = QPushButton("开始转换")
        self.export_btn.setFixedWidth(220)
        self.export_btn.clicked.connect(self.start_convert)
        self.cancel_btn = QPushButton("取消转换")
        self.cancel_btn.setFixedWidth(220)
        self.cancel_btn.setFixedHeight(32)
        self.cancel_btn.setEnabled(False)
        self.cancel_btn.clicked.connect(self.cancel_convert)
        self.progress = QProgressBar()
        self.progress.setFixedWidth(220)
        self.status = QLabel("")
        self.status.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.format_box = QComboBox()
        self.format_box.setFixedWidth(220)
        self.format_box.addItems(["Word (.docx)", "PDF (.pdf)", "HTML (.html)", "富文本 (.rtf)"])
        self.template_box = QComboBox()
        self.template_box.setFixedWidth(220)
        self.load_templates()
        self.template_box.currentIndexChanged.connect(self.on_template_changed)
        center_layout.addWidget(self.output_btn, alignment=Qt.AlignmentFlag.AlignHCenter)
        center_layout.addWidget(self.export_btn, alignment=Qt.AlignmentFlag.AlignHCenter)
        center_layout.addWidget(self.cancel_btn, alignment=Qt.AlignmentFlag.AlignHCenter)
        center_layout.addWidget(self.progress, alignment=Qt.AlignmentFlag.AlignHCenter)
        center_layout.addWidget(self.status, alignment=Qt.AlignmentFlag.AlignHCenter)
        center_layout.addWidget(self.format_box, alignment=Qt.AlignmentFlag.AlignHCenter)
        center_layout.addWidget(QLabel("Word模板"), alignment=Qt.AlignmentFlag.AlignHCenter)
        center_layout.addWidget(self.template_box, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.template_preview = QLabel()
        self.template_preview.setFixedHeight(60)
        center_layout.addWidget(self.template_preview, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.add_template_btn = QPushButton("添加自定义模板")
        self.add_template_btn.setFixedWidth(220)
        self.add_template_btn.clicked.connect(self.add_template)
        center_layout.addWidget(self.add_template_btn, alignment=Qt.AlignmentFlag.AlignHCenter)
        center_layout.addStretch()

        # 右侧：实时预览
        right = QWidget()
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(8, 8, 8, 8)
        right_layout.setSpacing(8)

        # 先创建字体调节按钮
        self.font_size = 15
        self.font_increase_btn = QPushButton("A+")
        self.font_decrease_btn = QPushButton("A-")
        self.font_increase_btn.clicked.connect(self.increase_font)
        self.font_decrease_btn.clicked.connect(self.decrease_font)

        # 预览区
        self.preview = QWebEngineView()
        self.preview.setMinimumWidth(320)
        self.preview.setMaximumWidth(600)
        self.preview.setStyleSheet("border-radius: 16px; background: #fff;")
        right_layout.addWidget(self.preview, stretch=1)

        # 只保留字体调节
        toolbar = QHBoxLayout()
        toolbar.addWidget(self.font_decrease_btn)
        toolbar.addWidget(self.font_increase_btn)
        toolbar.addStretch()
        right_layout.addLayout(toolbar)

        splitter.addWidget(left)
        splitter.addWidget(center)
        splitter.addWidget(right)
        splitter.setSizes([200, 320, 400])  # 可根据实际调整初始宽度
        vbox.addWidget(splitter)
        self.setCentralWidget(central)

        # 控制台圆角美化
        self.console_status = QLabel("")
        self.console_status.setStyleSheet("""
            background: #fff;
            color: #888;
            font-size: 14px;
            padding: 0 8px 0 8px;
            margin: 0;
        """)
        self.console_status.setContentsMargins(0,0,0,0)
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setObjectName("consoleEdit")
        self.console.setContentsMargins(0,0,0,0)
        console_widget = QWidget()
        console_layout = QVBoxLayout(console_widget)
        console_layout.setContentsMargins(0, 0, 0, 0)
        console_layout.setSpacing(0)
        console_layout.addWidget(self.console_status)
        console_layout.addWidget(self.console)
        dock = QDockWidget("控制台输出", self)
        dock.setWidget(console_widget)
        dock.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable | QDockWidget.DockWidgetFeature.DockWidgetFloatable)
        dock.setStyleSheet("""
            QDockWidget {
                border-radius: 12px;
                background: #fff;
                border: 1px solid #e0e0e0;
            }
            QDockWidget::title {
                padding: 4px 8px;
                border-radius: 12px 12px 0 0;
                background: #fff;
                color: #222;
                font-weight: bold;
                font-size: 14px;
            }
        """)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, dock)

        self.output_dir = ""
        self.template = None

        self.thread_pool = QThreadPool()
        self.max_concurrent = 4  # 可根据机器性能调整
        self.thread_pool.setMaxThreadCount(self.max_concurrent)
        self._stop_flag = {"stop": False}

    # 拖放支持
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        md_files = set()
        for f in files:
            if os.path.isdir(f):
                for root, _, fs in os.walk(f):
                    for file in fs:
                        if file.lower().endswith('.md'):
                            md_files.add(os.path.join(root, file))
            elif f.lower().endswith('.md'):
                md_files.add(f)
        md_files = sorted(md_files)
        if md_files:
            self.file_list.clear()
            self.file_list.addItems(md_files)
            self.console_status.setText(f"已加载 {len(md_files)} 个 Markdown 文件")
            # 自动选中并预览
            self.file_list.setCurrentRow(0)
            self.update_preview()
        else:
            self.console_status.setText("未检测到 Markdown 文件")

    # 文件列表右键菜单
    def show_file_list_menu(self, pos):
        items = self.file_list.selectedItems()
        menu = QMenu(self)
        if items:
            open_action = QAction("打开所在文件夹", self)
            open_action.triggered.connect(lambda: self.open_in_explorer(items[0].text()))
            remove_action = QAction("移除所选", self)
            remove_action.triggered.connect(self.remove_selected_files)
            menu.addAction(open_action)
            menu.addAction(remove_action)
        else:
            clear_action = QAction("清空列表", self)
            clear_action.triggered.connect(self.file_list.clear)
            menu.addAction(clear_action)
        menu.exec(self.file_list.mapToGlobal(pos))

    def remove_selected_files(self):
        for item in self.file_list.selectedItems():
            self.file_list.takeItem(self.file_list.row(item))

    def open_in_explorer(self, path):
        folder = os.path.dirname(path)
        if os.name == 'nt':
            os.startfile(folder)
        else:
            import subprocess
            subprocess.Popen(['open', folder])

    # 单/多/文件夹选择
    def choose_single_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "选择Markdown文件", "", "Markdown Files (*.md)")
        if file:
            self.file_list.clear()
            self.file_list.addItem(file)
            self.console_status.setText(f"已选择文件：{file}")
            # 自动选中并预览
            self.file_list.setCurrentRow(0)
            self.update_preview()

    def choose_multi_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "选择多个Markdown文件", "", "Markdown Files (*.md)")
        if files:
            self.file_list.clear()
            self.file_list.addItems(files)
            self.console_status.setText(f"已选择 {len(files)} 个文件")
            # 自动选中并预览
            self.file_list.setCurrentRow(0)
            self.update_preview()

    def choose_input_dir(self):
        d = QFileDialog.getExistingDirectory(self, "选择Markdown文件夹")
        if d:
            import glob
            files = glob.glob(os.path.join(d, "**/*.md"), recursive=True)
            self.file_list.clear()
            self.file_list.addItems(files)
            self.console_status.setText(f"已加载 {len(files)} 个 Markdown 文件")
            # 自动选中并预览
            if files:
                self.file_list.setCurrentRow(0)
                self.update_preview()

    def choose_output(self):
        d = QFileDialog.getExistingDirectory(self, "选择输出文件夹")
        if d:
            self.output_dir = d
            self.console_status.setText(f"输出文件夹：{d}")

    def start_convert(self):
        files = [self.file_list.item(i).text() for i in range(self.file_list.count())]
        if not files:
            self.status.setText("请先选择输入文件")
            self.console_status.setText("请先选择输入文件")
            return
        if not self.output_dir:
            self.output_dir = os.path.dirname(files[0])
            self.console_status.setText(f"未选择输出文件夹，已自动使用：{self.output_dir}")
        self.export_btn.setEnabled(False)
        self.progress.setValue(0)
        self.status.setText("开始转换...")
        self.console_status.setText("开始转换...")
        fmt = self.format_box.currentText()
        if "Word" in fmt:
            self.out_fmt = "docx"
            self.ext = ".docx"
        elif "PDF" in fmt:
            self.out_fmt = "pdf"
            self.ext = ".pdf"
        elif "HTML" in fmt:
            self.out_fmt = "html"
            self.ext = ".html"
        else:
            self.out_fmt = "rtf"
            self.ext = ".rtf"

        # ========== 分批处理 ==========
        self._all_files = files
        self._total_count = len(files)
        self._finished_count = 0
        self._batch_size = 100  # 每批最大文件数
        self._current_batch = 0
        self._stop_flag["stop"] = False

        self.signals = WorkerSignals()
        self.signals.progress.connect(self.on_progress)
        self.signals.error.connect(self.on_error)
        self.signals.finished.connect(self.on_finished)
        self.signals.stopped.connect(self.on_cancelled)
        self.signals.batch_finished.connect(self._convert_next_batch)

        self.cancel_btn.setEnabled(True)
        self._convert_next_batch()  # 启动第一批

    def _convert_next_batch(self):
        if self._stop_flag["stop"]:
            self.signals.stopped.emit()
            return
        start = self._current_batch * self._batch_size
        end = min(start + self._batch_size, self._total_count)
        batch_files = self._all_files[start:end]
        if not batch_files:
            self.signals.finished.emit()
            return
        self._current_batch += 1
        self._batch_finished_count = 0
        for idx, md_file in enumerate(batch_files, start + 1):
            task = ConvertTask(idx, self._total_count, md_file, self.output_dir, self.template,
                               self.out_fmt, self.ext, self.signals, self._stop_flag)
            self.thread_pool.start(task)

    def on_progress(self, idx, total, fname):
        self.progress.setMaximum(total)
        self.progress.setValue(idx)
        percent = int(idx / total * 100)
        self.progress.setFormat(f"{percent}%")
        self.status.setText(f"正在转换第{idx}/{total}个: {os.path.basename(fname)}")
        self.console_status.setText(f"正在转换第{idx}/{total}个: {os.path.basename(fname)}")
        self.log(f"正在转换: {fname}")
        self._finished_count += 1
        # 判断本批是否完成
        if self._finished_count % self._batch_size == 0 or self._finished_count == self._total_count:
            self.signals.batch_finished.emit()

    def on_error(self, msg):
        self.log(f"错误: {msg}")

    def on_finished(self):
        self.status.setText("全部转换完成！")
        self.console_status.setText("全部转换完成！")
        self.log("全部转换完成！")
        self.export_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)
        self.open_output_dir_dialog()

    def on_cancelled(self):
        self.status.setText("已取消转换")
        self.console_status.setText("已取消转换")
        self.log("用户取消了转换")
        self.export_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)

    def cancel_convert(self):
        self._stop_flag["stop"] = True
        self.cancel_btn.setEnabled(False)

    def open_output_dir_dialog(self):
        ret = QMessageBox.question(self, "转换完成", "全部转换完成，是否打开输出文件夹？",
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if ret == QMessageBox.StandardButton.Yes:
            self.open_in_explorer(self.output_dir)

    def toggle_max_restore(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def move_window(self, delta):
        self.move(self.x() + delta.x(), self.y() + delta.y())

    def update_preview(self):
        item = self.file_list.currentItem()
        if item:
            with open(item.text(), "r", encoding="utf-8") as f:
                md_text = f.read()
            html = markdown.markdown(md_text, extensions=['fenced_code', 'tables', 'codehilite'])
            html = f"""
            <html>
            <head>
            <style>
            body {{ font-family: 'San Francisco', Arial, '微软雅黑'; font-size: {self.font_size}px; background: #fff; color: #222; }}
            pre, code {{ background: #f5f5f7; border-radius: 6px; padding: 4px; }}
            table {{ border-collapse: collapse; }}
            th, td {{ border: 1px solid #ccc; padding: 4px 8px; }}
            </style>
            </head>
            <body>{html}</body>
            </html>
            """
            self.preview.setHtml(html)
        else:
            self.preview.setHtml("<div style='color:#888;text-align:center;margin-top:40px;'>请选择文件以预览</div>")

    def log(self, msg):
        self.console.append(msg)

    def load_templates(self):
        import glob
        tpl_dir = "resources/templates"
        if not os.path.exists(tpl_dir):
            os.makedirs(tpl_dir)
        tpl_files = glob.glob(os.path.join(tpl_dir, "*.docx"))
        self.template_box.clear()
        for f in tpl_files:
            self.template_box.addItem(os.path.basename(f), f)
        self.template_box.addItem("无模板", None)

    def on_template_changed(self, idx):
        path = self.template_box.currentData()
        self.template = path if path else None
        # 可选：显示模板预览图（如有同名png）
        if path:
            img_path = os.path.splitext(path)[0] + ".png"
            if os.path.exists(img_path):
                pix = QPixmap(img_path)
                self.template_preview.setPixmap(pix.scaledToHeight(60))
            else:
                self.template_preview.clear()
        else:
            self.template_preview.clear()

    def add_template(self):
        file, _ = QFileDialog.getOpenFileName(self, "选择Word模板", "", "Word模板 (*.docx)")
        if file:
            import shutil
            tpl_dir = "resources/templates"
            if not os.path.exists(tpl_dir):
                os.makedirs(tpl_dir)
            dst = os.path.join(tpl_dir, os.path.basename(file))
            shutil.copy(file, dst)
            self.load_templates()

    def increase_font(self):
        self.font_size = min(self.font_size + 2, 36)
        self.update_preview()

    def decrease_font(self):
        self.font_size = max(self.font_size - 2, 8)
        self.update_preview()