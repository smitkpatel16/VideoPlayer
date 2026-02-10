"""
MyThumbnailDisplay.py - Thumbnail Strip Display for Timeline

This module provides the MyThumbnailDisplay class for displaying a horizontal strip
of thumbnail images from the video timeline. It includes a playhead indicator showing
the current playback position.

Key Responsibilities:
- Display multiple thumbnail images in a horizontal scrollable view
- Show current playback position with a vertical line indicator
- Automatically center the view on the current playback position
- Support dynamic duration and position updates

The class uses QGraphicsView and QGraphicsScene for efficient image display
and includes a green vertical line as the playhead indicator.

Dependencies:
- PyQt6: QGraphicsView, QGraphicsScene, QPixmap, QPen
"""

from PyQt6.QtWidgets import QGraphicsView
from PyQt6.QtWidgets import QGraphicsScene
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPen


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
        """
        Resets the thumbnail display and playhead to initial state.

        Called when a new video is opened to clear old thumbnails.
        """
        # Reset thumbnail count
        self.__count = 0
        # Reset total width of all thumbnails
        self.__totalW = 0
        # Reset stored duration
        self.__duration = 0
        # Clear all graphics items from the scene
        self.display.clear()

    def addImage(self, qImg, pos):
        """
        Adds a thumbnail image to the timeline strip.

        Args:
            qImg (QImage): The thumbnail frame image
            pos (int): Sequential position/index of the thumbnail

        Thumbnails are arranged horizontally with each at position (pos * width).
        """
        # Convert QImage to QPixmap for display
        pm = QPixmap.fromImage(qImg)
        # Add the pixmap to the graphics scene
        pmi = self.display.addPixmap(pm)
        # Position horizontally based on thumbnail width
        pmi.setPos(pos * pm.width(), 0)
        # Increment thumbnail counter
        self.__count += 1
        # Calculate total width (100 thumbnails max)
        self.__totalW = 100*pm.width()

    def setDuration(self, duration):
        """
        Sets the total video duration for timeline calculation.

        Args:
            duration (int): Total duration in seconds

        Creates a vertical green line (playhead) for the timeline view.
        """
        # Store duration in milliseconds
        self.__duration = duration*1000
        # Create a vertical line at the beginning as playhead indicator
        self.__r = self.display.addLine(
            0, 0, 0, 80, self.__pen)  # Green pen defined in constructor
        # Set high Z-value so line appears on top of images
        self.__r.setZValue(5000)

    def setPosition(self, pos):
        """
        Updates the playhead position based on current playback position.

        Args:
            pos (int): Current playback position in milliseconds

        Calculates the corresponding position in the thumbnail strip and
        centers the view to keep the playhead visible.
        """
        if self.__duration:
            # Calculate progress ratio (0.0 to 1.0)
            p = round(pos/self.__duration, 6)
            # Convert to position in thumbnail strip
            p = p*self.__totalW
            # Center the view on the playhead position
            self.centerOn(p, 0)
            # Move the playhead line to the current position
            self.__r.setPos(p, 0)
