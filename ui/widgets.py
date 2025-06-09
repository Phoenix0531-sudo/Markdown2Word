from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PySide6.QtCore import Signal, Qt

class MacTitleBar(QWidget):
    close_signal = Signal()
    minimize_signal = Signal()
    maximize_signal = Signal()
    drag_signal = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(40)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 8, 16, 0)
        layout.setSpacing(8)

        layout.addStretch()

        self.yellow_btn = QPushButton()
        self.yellow_btn.setObjectName("macYellowBtn")
        self.yellow_btn.setFixedSize(14, 14)
        self.yellow_btn.clicked.connect(self.minimize_signal.emit)

        self.green_btn = QPushButton()
        self.green_btn.setObjectName("macGreenBtn")
        self.green_btn.setFixedSize(14, 14)
        self.green_btn.clicked.connect(self.maximize_signal.emit)

        self.red_btn = QPushButton()
        self.red_btn.setObjectName("macRedBtn")
        self.red_btn.setFixedSize(14, 14)
        self.red_btn.clicked.connect(self.close_signal.emit)

        layout.addWidget(self.yellow_btn)
        layout.addWidget(self.green_btn)
        layout.addWidget(self.red_btn)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if hasattr(event, "globalPosition"):
                self._drag_pos = event.globalPosition().toPoint()
            else:
                self._drag_pos = event.globalPos()
            self._dragging = True

    def mouseMoveEvent(self, event):
        if getattr(self, "_dragging", False):
            if hasattr(event, "globalPosition"):
                new_pos = event.globalPosition().toPoint()
            else:
                new_pos = event.globalPos()
            delta = new_pos - self._drag_pos
            self._drag_pos = new_pos
            self.drag_signal.emit(delta)

    def mouseReleaseEvent(self, event):
        self._dragging = False