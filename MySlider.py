import PyQt6.QtCore
from PyQt6.QtWidgets import QSlider
# from PyQt6 import QtGui
from PyQt6.QtCore import pyqtSignal

# derive QSlilder class to enable hovering to show timestamp


class MySlider(QSlider):
    """
    This class is used to derive the QSlider class to enable hovering to show timestamp.
    """
    showPreview = pyqtSignal(tuple)
# |-----------------------------------------------------------------------------|
# Constructor :-
# |-----------------------------------------------------------------------------|

    def __init__(self, *args, **kwargs):
        """
        This constructor is used to initialize the MySlider class.
        """
        super(MySlider, self).__init__(*args, **kwargs)
        self.setMouseTracking(True)
        self.setOrientation(PyQt6.QtCore.Qt.Orientation.Horizontal)
        self.setToolTip("0:00")
        self.duration = 0
        self.setTickPosition(QSlider.TickPosition.TicksBothSides)
        self.__inside = False
        # just setting some size aspects
        # self.setMinimumHeight(20)
        # self.setMinimumWidth(100)
        # self.setMaximumHeight(20)
        # self.__painter = QtGui.QPainter()

        # # for the on off font
        # self.__font = QtGui.QFont()
        # self.__font.setFamily("Arial")
        # self.__font.setPixelSize(12)
        # self.__font.setBold(True)

        # self.__bbrush = QtGui.QBrush(QtGui.QColor(50, 50, 255),
        #                              style=PyQt6.QtCore.Qt.BrushStyle.SolidPattern)
        # self.__gbrush = QtGui.QBrush(QtGui.QColor(50, 50, 50),
        #                              style=PyQt6.QtCore.Qt.BrushStyle.SolidPattern)
        # self.__wbrush = QtGui.QBrush(QtGui.QColor(255, 255, 255),
        #                              style=PyQt6.QtCore.Qt.BrushStyle.SolidPattern)


# |--------------------------End of Constructor--------------------------------|


    def mouseMoveEvent(self, event):
        posSec = int(self.duration*(event.pos().x()/self.width()))
        self.setToolTip(f"{posSec // 60}:{posSec % 60:02d}")
        if self.__inside:
            self.showPreview.emit((event.pos().x(), event.pos().y()))

    def enterEvent(self, event):
        self.__inside = True
        self.showPreview.emit((event.position().x(), event.position().y()))

    def leaveEvent(self, event):
        self.__inside = False
        self.showPreview.emit(())

# |-----------------------------------------------------------------------------|
# paintEvent
# |-----------------------------------------------------------------------------|
# def paintEvent(self, event):
#     if self.duration:
#         position = int(self.width()*(self.value()/self.maximum()))
#     else:
#         position = 0

#     self.__painter.begin(self)
#     self.__painter.setFont(self.__font)
#     self.__painter.setBrush(self.__bbrush)
#     # rounded rectangle as a whole
#     # smooth curves
#     self.__painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
#     if position:
#         self.__painter.drawRoundedRect(0, 0, position, self.height(),
#                                        self.height(), self.height())
#     # gray fill
#     self.__painter.setBrush(self.__gbrush)
#     # rounded rectangle as a whole
#     # smooth curves
#     self.__painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

#     self.__painter.drawRoundedRect(position, 0, self.width(), self.height()-2,
#                                    self.height()/3, self.height()/3)
#     # white circle/button instead of the tick but in different location
#     self.__painter.setBrush(self.__wbrush)
#     # smooth curves
#     self.__painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

#     self.__painter.drawEllipse(position, 0, self.height(), self.height())

#     posSec = int(self.duration*(position/self.width()))
#     # value text
#     # smooth curves
#     self.__painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

#     self.__painter.drawText(int(self.width()/2), int(self.height()/1.5),
#                             f"{posSec // 60}:{posSec % 60:02d}")
#     self.__painter.end()
