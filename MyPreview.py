from PyQt6.QtWidgets import QDialog
from PyQt6.QtWidgets import QGraphicsView
from PyQt6.QtWidgets import QGraphicsScene
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt


class MyPreview(QDialog):
    """
    This class is used to derive the QDialog class to enable hovering preview.
    """

# |-----------------------------------------------------------------------------|
# Constructor :-
# |-----------------------------------------------------------------------------|
    def __init__(self, *args, **kwargs):
        """
        This constructor is used to initialize the MyPreview class.
        """
        super(MyPreview, self).__init__(*args, **kwargs)
        self.setModal(False)
        self.resize(202, 108)
        self.view = QGraphicsView(self)
        self.display = QGraphicsScene()
        self.position = QLabel(self)
        self.view.setScene(self.display)
        self.display.clear()
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.view)
        self.mainLayout.addWidget(self.position)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

    def showImage(self, qImg, pos):
        self.display.clear()
        pm = QPixmap.fromImage(qImg)
        pmi = self.display.addPixmap(pm)
        pmi.setPos(0, 0)
        self.position.setText(str(pos))
