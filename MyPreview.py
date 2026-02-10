"""
MyPreview.py - Preview Display for Timeline Scrubbing

This module provides the MyPreview class for displaying frame previews when
the user hovers over the timeline seek slider.

Key Responsibilities:
- Display a preview frame from the video at the hovered timeline position
- Show timestamp of the preview frame
- Frameless dialog for clean overlay appearance
- Automatic positioning based on cursor location

The preview is displayed as a small frameless dialog with:
- Graphics view showing the preview frame image
- Label displaying the timestamp

Dependencies:
- PyQt6: GUI components (QDialog, QGraphicsView, QGraphicsScene, QLabel, QVBoxLayout)
"""

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
        """
        Displays a preview frame and timestamp.

        Args:
            qImg (QImage): The frame image to display
            pos (str): Timestamp string (MM:SS format)

        Clears the previous content and displays the new frame and timestamp.
        """
        # Clear previous preview
        self.display.clear()
        # Convert QImage to QPixmap for display
        pm = QPixmap.fromImage(qImg)
        # Add the pixmap to the graphics scene
        pmi = self.display.addPixmap(pm)
        # Position the pixmap at the origin
        pmi.setPos(0, 0)
        # Display the timestamp below the preview
        self.position.setText(str(pos))
