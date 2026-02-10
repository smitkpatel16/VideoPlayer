"""
MySlider.py - Custom Slider with Timeline Preview

This module provides an enhanced slider widget that emits preview signals
when the user hovers over the timeline, allowing frame-accurate preview.

Key Responsibilities:
- Detect mouse movements over the slider
- Calculate timeline position from mouse coordinates
- Emit preview signals with position and timestamp information
- Throttle preview updates to avoid excessive processing (50ms intervals)
- Track mouse entry/exit for efficient preview generation

Custom Signals:
- showPreview(tuple): Emits (x, y, milliseconds) for preview display
- enterPreview(): Emitted when mouse enters slider
- exitPreview(): Emitted when mouse leaves slider

Dependencies:
- PyQt6: QSlider widget and signals
"""

import time
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
    enterPreview = pyqtSignal()
    exitPreview = pyqtSignal()
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
        self.duration = 0
        # self.setTickPosition(QSlider.TickPosition.TicksBothSides)
        self.__inside = False
        self.__sentStamp = time.time()
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
        """
        Handles mouse movement over the slider for preview generation.

        Calculates the timeline position based on mouse coordinates and
        emits preview signals with throttling (50ms minimum between updates).

        Args:
            event (QMouseEvent): The mouse movement event
        """
        # Get cursor position relative to slider
        x, y = event.pos().x(), event.pos().y()
        # Calculate corresponding position in media (in seconds)
        loc = self.duration*(x/self.width())

        # Only emit if inside slider and throttle is satisfied (50ms minimum)
        if self.__inside and time.time()-self.__sentStamp > 0.05:
            # Convert local coordinates to global screen coordinates
            global_pos = self.mapToGlobal(event.pos())
            # Emit preview signal with position and milliseconds
            self.showPreview.emit((global_pos.x(), global_pos.y(), loc*1000))
            # Update timestamp to throttle further updates
            self.__sentStamp = time.time()
        return super().mouseMoveEvent(event)

    def enterEvent(self, event):
        """
        Handles mouse entering the slider area.

        Signals the start of preview generation and initializes throttling.
        """
        # Emit signal that preview should start
        self.enterPreview.emit()
        # Set flag to indicate mouse is inside slider
        self.__inside = True
        # Initialize throttle timestamp
        self.__sentStamp = time.time()

    def leaveEvent(self, event):
        """
        Handles mouse leaving the slider area.

        Signals the end of preview generation by emitting an empty tuple.
        """
        # Set flag to indicate mouse is outside slider
        self.__inside = False
        # Emit signal that preview should stop
        self.exitPreview.emit()
        # Emit empty preview to hide the preview window
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
