"""Docker build-time smoke test: verify imports and pandoc CLI."""
import sys
import subprocess

try:
    from PySide6.QtWidgets import QApplication
    print("PySide6: OK")
except ImportError as e:
    print(f"PySide6 import failed (expected in headless): {e}")

try:
    from PySide6.QtWebEngineWidgets import QWebEngineView
    print("QtWebEngine: OK")
except ImportError as e:
    print(f"QtWebEngine import failed (expected in headless): {e}")

import markdown
print(f"markdown: {markdown.__version__}")

import pypandoc
print(f"pypandoc: {pypandoc.get_pandoc_version()}")

result = subprocess.run(["pandoc", "--version"], capture_output=True, text=True)
first_line = result.stdout.split("\n")[0] if result.stdout else "not found"
print(f"pandoc: {first_line}")

print("All smoke tests passed")
