import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget,
                               QVBoxLayout, QHBoxLayout, QLabel,
                               QLineEdit, QPushButton, QFileDialog,
                               QMessageBox)
from PySide6.QtCore import Qt
import os # 引入 os 模块，用于处理路径

# 引入 pypandoc 库
import pypandoc # 确保你已经安装了 pypandoc (pip install pypandoc)
# 并且已经安装了 pandoc 可执行文件，并确保它在系统的 PATH 中
# pandoc 下载地址: https://pandoc.org/installing.html


def convert_markdown_to_word(markdown_path, word_path):
    """
    使用 pypandoc 将 Markdown 文件转换为 Word (.docx) 文件。
    需要安装 pandoc 可执行文件和 pypandoc Python 库。
    """
    # 确保输入文件存在
    if not os.path.exists(markdown_path):
        raise FileNotFoundError(f"输入文件不存在: {markdown_path}")

    # 确保输出目录存在
    output_dir = os.path.dirname(word_path)
    if output_dir and not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
            print(f"创建输出目录: {output_dir}")
        except Exception as e:
            raise IOError(f"无法创建输出目录: {output_dir}\n错误详情: {e}") from e


    try:
        # 使用 pypandoc 进行转换
        # convert_file(source, to, outputfile, extra_args)
        pypandoc.convert_file(markdown_path, 'docx', outputfile=word_path)

        print(f"成功转换: {markdown_path} -> {word_path}")
        return True

    except OSError as e:
         # 如果找不到 pandoc 可执行文件，pypandoc 会抛出 OSError
         error_message = f"转换失败: 找不到 pandoc 可执行文件。\n请确保已安装 pandoc (https://pandoc.org/installing.html) 并将其添加到系统 PATH。\n错误详情: {e}"
         print(error_message)
         raise Exception(error_message) from e
    except Exception as e:
        error_message = f"转换过程中发生错误:\n{e}"
        print(error_message)
        # 将其他异常也向上抛出，以便在 GUI 中捕获并显示
        raise Exception(error_message) from e


class MarkdownConverterGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Markdown 转 Word")
        # 可以设置窗口的初始大小
        self.setGeometry(100, 100, 500, 250) # (x, y, width, height)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20) # 设置边距
        main_layout.setSpacing(15) # 设置控件间的间距

        # 输入文件选择
        input_layout = QHBoxLayout()
        self_input_label = QLabel("选择 Markdown 文件:")
        # 调整标签宽度策略以防止挤压
        self_input_label.setFixedWidth(150)
        self.input_path_edit = QLineEdit()
        self.input_path_edit.setPlaceholderText("请选择待转换的 .md 文件")
        self.select_input_button = QPushButton("浏览...")
        self.select_input_button.clicked.connect(self.select_markdown_file)

        input_layout.addWidget(self_input_label)
        input_layout.addWidget(self.input_path_edit)
        input_layout.addWidget(self.select_input_button)

        # 输出文件位置选择
        output_layout = QHBoxLayout()
        output_label = QLabel("选择保存位置:")
        output_label.setFixedWidth(150)
        self.output_path_edit = QLineEdit()
        self.output_path_edit.setPlaceholderText("请选择保存 .docx 文件的位置")
        self.select_output_button = QPushButton("浏览...")
        self.select_output_button.clicked.connect(self.select_output_location)

        output_layout.addWidget(output_label)
        output_layout.addWidget(self.output_path_edit)
        output_layout.addWidget(self.select_output_button)

        # 转换按钮
        self.convert_button = QPushButton("开始转换")
        self.convert_button.clicked.connect(self.start_conversion)
        # 使转换按钮居中或靠右，这里使用 QHBoxLayout 和 stretch
        convert_button_layout = QHBoxLayout()
        convert_button_layout.addStretch() # 添加伸缩空间，将按钮推到右边
        convert_button_layout.addWidget(self.convert_button)


        # 将子布局添加到主布局
        main_layout.addLayout(input_layout)
        main_layout.addLayout(output_layout)
        main_layout.addStretch() # 添加伸缩空间，将按钮推到底部
        main_layout.addLayout(convert_button_layout)


    def select_markdown_file(self):
        """打开文件对话框选择 Markdown 文件，并自动填充输出文件名"""
        file_filter = "Markdown 文件 (*.md *.markdown);;所有文件 (*)"
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "选择 Markdown 文件",
            "",
            file_filter
        )
        if filepath:
            self.input_path_edit.setText(filepath)
            # 自动设置输出文件路径
            directory, filename = os.path.split(filepath)
            # 去掉原文件的扩展名
            base_name, _ = os.path.splitext(filename)
            default_output_path = os.path.join(directory, base_name + ".docx")
            self.output_path_edit.setText(default_output_path)

    def select_output_location(self):
        """打开文件对话框选择 Word 文件保存位置"""
        file_filter = "Word 文档 (*.docx);;所有文件 (*)"
         # QFileDialog.getSaveFileName 返回 (文件名, 选中的过滤器)
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "保存 Word 文档", # 对话框标题
            "", # 初始目录
            file_filter # 文件过滤器
        )
        if filepath: # 如果用户选择了文件
            # 确保文件扩展名是 .docx
            if not filepath.lower().endswith(".docx"):
                filepath += ".docx"
            self.output_path_edit.setText(filepath)

    def start_conversion(self):
        """开始执行转换过程"""
        input_file = self.input_path_edit.text()
        output_file = self.output_path_edit.text()

        if not input_file:
            QMessageBox.warning(self, "警告", "请选择要转换的 Markdown 文件。")
            return
        if not output_file:
            QMessageBox.warning(self, "警告", "请选择 Word 文档的保存位置。")
            return

        try:
            # 调用实际的转换函数
            convert_markdown_to_word(input_file, output_file)
            QMessageBox.information(self, "成功", f"文件已成功转换为:\n{output_file}")
        except FileNotFoundError as e:
             QMessageBox.warning(self, "文件未找到", str(e))
        except IOError as e:
             QMessageBox.critical(self, "文件操作错误", str(e))
        except Exception as e:
            # 捕获 convert_markdown_to_word 中抛出的其他异常
            QMessageBox.critical(self, "转换失败", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # PySide6 在 macOS 上默认就会有原生的外观，看起来像苹果风格。
    # 在其他系统上，它会使用对应系统的原生风格。
    # 如果需要在其他系统上模拟 macOS 风格，通常需要复杂的 QSS 样式表，
    # 或者使用如 QDarkStyleSheet 这样的第三方库并自定义，这超出了基本框架的范围。
    # 这里的代码在 macOS 上运行时就会是 macOS 风格。

    window = MarkdownConverterGUI()
    window.show()

    sys.exit(app.exec())