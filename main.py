import sys
import os

# 设置pandoc.exe路径（无论源码还是打包后都能找到）
def get_pandoc_path():
    if getattr(sys, 'frozen', False):
        # PyInstaller打包后的临时目录
        base_path = sys._MEIPASS
    else:
        # 源码运行
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, 'resources', 'pandoc.exe')

# 设置pypandoc全局路径
import pypandoc
pypandoc.pandoc_path = get_pandoc_path()

from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())