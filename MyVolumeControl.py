from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt6.QtGui import QPainter, QPolygon, QColor, QMouseEvent
from PyQt6.QtCore import Qt, QPoint
import sys
from PyQt6.QtCore import pyqtSignal


class TriangleVolumeControl(QWidget):
    # Signal to emit volume changes (0 to 100)
    valueChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(200, 100)
        self.volume = 0.5  # Default volume (50%)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw the right-angle triangle
        width = self.width()
        height = self.height()
        triangle = QPolygon([
            QPoint(0, height),
            QPoint(width, height),
            QPoint(width, 0)
        ])
        painter.setBrush(QColor(200, 200, 200))
        painter.drawPolygon(triangle)

        # Draw the volume level
        volume_width = int(self.volume * width)
        volume_triangle = QPolygon([
            QPoint(0, height),
            QPoint(volume_width, height-int(volume_width*height/width)),
            QPoint(volume_width, height),
        ])
        painter.setBrush(QColor(100, 150, 255))
        painter.drawPolygon(volume_triangle)

        # Draw the text value at the center
        painter.setPen(QColor(0, 0, 0))
        font = painter.font()
        font.setPointSize(12)
        painter.setFont(font)
        text = f"{int(self.volume * 100)}%"
        text_rect = painter.boundingRect(
            0, int(0.25*height), width, height, Qt.AlignmentFlag.AlignCenter, text)
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, text)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.update_volume(event.position().x())

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() & Qt.MouseButton.LeftButton:
            self.update_volume(event.position().x())

    def update_volume(self, x):
        width = self.width()
        self.volume = max(0, min(1, x / width))
        self.update()
        # Emit volume as percentage
        self.valueChanged.emit(int(self.volume*100))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QWidget()
    layout = QVBoxLayout(window)

    volume_control = TriangleVolumeControl()
    layout.addWidget(volume_control)

    window.setWindowTitle("Triangle Volume Control")
    window.resize(400, 200)
    window.show()
    sys.exit(app.exec())
