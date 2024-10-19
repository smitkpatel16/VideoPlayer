from PyQt6.QtWidgets import QGraphicsView
from PyQt6.QtWidgets import QGraphicsScene
from PyQt6.QtWidgets import QGraphicsItem
from PyQt6.QtWidgets import QDialog
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtGui import QPen
from PyQt6.QtGui import QBrush
from processTools import SelectionLine


# ===============================================================================
# MyThubnailDisplay-
# ===============================================================================
class MyThumbnailDisplay(QGraphicsView):
    """
    Create a qgraphicsview widget to display reel of images array.
    """

# |-----------------------------------------------------------------------------|
# Constructor :-
# |-----------------------------------------------------------------------------|
    def __init__(self, parent=None):
        """
        This constructor is used to initialize the thumbnail display.
        """
        super(MyThumbnailDisplay, self).__init__(parent=parent)
        self.display = QGraphicsScene()
        self.setScene(self.display)
        self.clearDisplay()
        self.__pen = QPen(Qt.GlobalColor.green, 3)
# |--------------------------End of Constructor---------------------------------|

    def clearDisplay(self):
        # to clear out when a new video is opened (only 1 supported currently)
        self.__count = 0
        self.__totalW = 0
        self.__duration = 0
        self.display.clear()

    def addImage(self, qImg, pos):
        pm = QPixmap.fromImage(qImg)
        pmi = self.display.addPixmap(pm)
        pmi.setPos(pos * pm.width(), 0)
        self.__count += 1
        self.__totalW = 100*pm.width()

    def setDuration(self, duration):
        self.__duration = duration*1000
        self.__r = self.display.addLine(
            0, 0, 0, 80, self.__pen)
        self.__r.setZValue(5000)

    def setPosition(self, pos):
        if self.__duration:
            p = round(pos/self.__duration, 6)
            p = p*self.__totalW
            self.centerOn(p, 0)
            self.__r.setPos(p, 0)
