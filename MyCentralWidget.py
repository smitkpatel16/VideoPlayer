"""
MyCentralWidget.py - Central Widget Container for Video Player

This module provides the MyCentralWidget class, which serves as the main content
container for the video player application. It manages the layout and sizing of
child widgets (media player, controls, etc.) and handles responsive sizing.

Key Responsibilities:
- Manage vertical layout of application components
- Handle window resize events and adjust child widget sizes accordingly
- Provide event filtering for paint events to trigger dynamic resizing

The class uses event filtering to detect paint events and dynamically adjusts
widget dimensions based on the available window space.
"""

import PyQt6.QtWidgets


# ===============================================================================
# MyCentralWidget-
# ===============================================================================
class MyCentralWidget(PyQt6.QtWidgets.QWidget):
    """
    This class is used to create a central widget for the video player.
    """
# |-----------------------------------------------------------------------------|
# Constructor :-
# |-----------------------------------------------------------------------------|

    def __init__(self, *args, **kwargs):
        """
        This constructor is used to initialize the central widget.
        """
        super(MyCentralWidget, self).__init__(*args, **kwargs)
        self.mainLayout = PyQt6.QtWidgets.QVBoxLayout()
        self.setLayout(self.mainLayout)
        self.installEventFilter(self)
# |--------------------------End of Constructor---------------------------------|

    def eventFilter(self, obj, event):
        """
        Filters widget events to handle dynamic resizing.

        This method listens for paint events and calls adjustWidgetSizes()
        to dynamically resize child widgets based on the current window size.
        Child events are passed through without modification.

        Args:
            obj: The object that generated the event
            event: The event object

        Returns:
            bool: True if event was handled, False to pass to parent
        """
        if type(event) == PyQt6.QtCore.QChildEvent:
            # Allow child events to pass through normally
            return super().eventFilter(obj, event)
        if event.type() == PyQt6.QtCore.QEvent.Type.Paint:
            # On every paint event, recalculate and adjust widget sizes
            self.adjustWidgetSizes()
        return super().eventFilter(obj, event)
# |-----------------------------------------------------------------------------|
# addWidget :-
# |-----------------------------------------------------------------------------|

    def addWidget(self, widget):
        """
        Adds a widget to the main vertical layout.

        Args:
            widget: The PyQt6 widget to add to the layout

        This method is a convenience wrapper around the layout's addWidget method.
        """
        self.mainLayout.addWidget(widget)
# |--------------------------End of addWidget-----------------------------------|

# |-----------------------------------------------------------------------------|
# adjustWidgetSizes :-
# |-----------------------------------------------------------------------------|
    def adjustWidgetSizes(self):
        """
        Dynamically adjusts the size of child widgets based on window dimensions.

        Layout structure (3 items):
        - Item 0 (Media Player): 90% window width, height-250px
        - Item 1 (Controls): 80% window width, 120px minimum height
        - Item 2 (Additional): 90% window width, 100px minimum height

        This method is called on paint events to ensure responsive sizing.
        """
        # Adjust first widget (typically the video player)
        if self.mainLayout.itemAt(0):
            w = self.mainLayout.itemAt(0).widget()
            # Set width to 90% of container width
            w.setMinimumWidth(int(self.width()*0.9))
            # Set height to container height minus 250px (for controls and spacing)
            w.setMinimumHeight(self.height() - 250)

        # Adjust second widget (typically the media controls)
        if self.mainLayout.itemAt(1):
            w = self.mainLayout.itemAt(1).widget()
            # Set width to 80% of container width
            w.setMinimumWidth(int(self.width()*0.8))
            # Set height to 120px minimum
            w.setMinimumHeight(120)

        # Adjust third widget (typically additional controls or info)
        if self.mainLayout.itemAt(2):
            w = self.mainLayout.itemAt(2).widget()
            # Set width to 90% of container width
            w.setMinimumWidth(int(self.width()*0.9))
            # Set height to 100px minimum
            w.setMinimumHeight(100)
# |--------------------------End of adjustWidgetSizes---------------------------|
