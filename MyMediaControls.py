"""
MyMediaControls.py - Media Control UI Components

This module provides the MyMediaControls class, which creates the playback control
interface including play/pause, stop, skip buttons, seek slider, and volume control.

Key Responsibilities:
- Create and manage playback control buttons (play, pause, stop, skip)
- Manage seek slider for timeline navigation with preview support
- Manage volume dial for audio level adjustment
- Display current time and total duration
- Emit signals for playback control (play, pause, next, previous)
- Update UI based on media player state

The controls are arranged in a vertical layout with:
- Top: Current time slider, seek slider, duration time
- Bottom: Navigation buttons (prev, play, stop, next) and volume dial

Dependencies:
- PyQt6: GUI components and signals
- Custom: MySlider (enhanced slider with preview)
"""

from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QStyle
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QDial
from PyQt6.QtCore import pyqtSignal
from MySlider import MySlider


# create a horizontal layout using QtWidgets
# for the media controls
# it should help play, pause, stop, and seek the video
# ===============================================================================
# MyMediaControls-
# ===============================================================================
class MyMediaControls(QWidget):
    """
    This class is used to create media controls using PyQt6.
    """
    # control signals
    playMedia = pyqtSignal()
    pauseMedia = pyqtSignal()
    prev = pyqtSignal()
    next = pyqtSignal()

# |-----------------------------------------------------------------------------|
# Constructor :-
# |-----------------------------------------------------------------------------|
    def __init__(self, *args, **kwargs):
        """
        This constructor is used to initialize the media controls.
        """
        super(MyMediaControls, self).__init__(*args, **kwargs)
        # Add Seek slider, play, pause, and stop buttons
        self.__addControls()
        # Add label to showcase total play time
        self.__addLabels()
        # Arrange the widgets in the layout
        self.__arrangeWidgets()
# |--------------------------End of Constructor---------------------------------|

# |-----------------------------------------------------------------------------|
# __addControls :-
# |-----------------------------------------------------------------------------|
    def __addControls(self):
        """
        This method is used to add media controls to the layout.
        """
        #
        self.prevBtn = QPushButton()
        self.prevBtn.setIcon(self.style().standardIcon(
            QStyle.StandardPixmap.SP_MediaSkipBackward))
        self.prevBtn.clicked.connect(self.__setPrev)
        # Create a play/pause toggle button
        self.playButton = QPushButton()
        # converting to toggle button
        self.playButton.setCheckable(True)
        # connect the state change of playbutton to the playpause method
        self.playButton.clicked.connect(self.__playPauseChange)
        self.playButton.setIcon(self.style().standardIcon(
            QStyle.StandardPixmap.SP_MediaPause))
        # Create a stop button
        self.stopButton = QPushButton()
        self.stopButton.setIcon(self.style().standardIcon(
            QStyle.StandardPixmap.SP_MediaStop))
        self.nextBtn = QPushButton()
        self.nextBtn.setIcon(self.style().standardIcon(
            QStyle.StandardPixmap.SP_MediaSkipForward))
        self.nextBtn.clicked.connect(self.__setNext)
        # Create a seek slider
        self.seekSlider = MySlider()
        # Volume Dail
        self.volumeDial = QDial()
        self.volumeDial.setMinimum(0)
        self.volumeDial.setMaximum(100)
        self.volumeDial.setNotchesVisible(True)
# |--------------------------End of __addControls-------------------------------|

# |-----------------------------------------------------------------------------|
# __addLabels :-
# |-----------------------------------------------------------------------------|
    def __addLabels(self):
        """
        Add display label and some notifiers
        """
        self.durationLabel = QLabel(self)
        self.currentLabel = QLabel(self)
# |--------------------------End of __addLabels---------------------------------|

# |-----------------------------------------------------------------------------|
# __playPauseChange :-
# |-----------------------------------------------------------------------------|
    def __playPauseChange(self):
        """
        This method is used to change the play/pause button icon.
        """
        # If the play button is checked
        if self.playButton.isChecked():
            # Set the icon of the play button to pause
            self.playButton.setIcon(self.style().standardIcon(
                QStyle.StandardPixmap.SP_MediaPause))
            # emit the play signal
            self.playMedia.emit()
        else:
            # Set the icon of the play button to play
            self.playButton.setIcon(self.style().standardIcon(
                QStyle.StandardPixmap.SP_MediaPlay))
            # emit the pause signal
            self.pauseMedia.emit()
# |--------------------------End of __playPauseChange---------------------------|


# |-----------------------------------------------------------------------------|
# __setPrev :-
# |-----------------------------------------------------------------------------|


    def __setPrev(self):
        self.prev.emit()
# |----------------------------End of __setPrev--------------------------------|

# |-----------------------------------------------------------------------------|
# __setNext :-
# |-----------------------------------------------------------------------------|
    def __setNext(self):
        self.next.emit()
# |----------------------------End of __setNext--------------------------------|

# |-----------------------------------------------------------------------------|
# __arrangeWidgets :-
# |-----------------------------------------------------------------------------|
    def __arrangeWidgets(self):
        """
        This method is used to arrange the widgets in the layout.
        """
        # Create a local horizontal layout
        hlayout1 = QHBoxLayout()
        # Add play, pause, and stop buttons
        hlayout1.addWidget(self.prevBtn)
        hlayout1.addWidget(self.playButton)
        hlayout1.addWidget(self.stopButton)
        hlayout1.addWidget(self.nextBtn)
        hlayout1.addWidget(self.volumeDial)
        hlayout2 = QHBoxLayout()
        hlayout2.addWidget(self.currentLabel)
        hlayout2.addWidget(self.seekSlider)
        hlayout2.addWidget(self.durationLabel)
        # Create a vertical layout
        vlayout = QVBoxLayout()
        # Add seek slider to the vertical layout
        vlayout.addLayout(hlayout2)
        # Add the horizontal layout to the vertical layout
        vlayout.addLayout(hlayout1)
        # Set the layout of the media controls
        self.setLayout(vlayout)
# |--------------------------End of __arrangeWidgets----------------------------|

# |-----------------------------------------------------------------------------|
# updateSlider :-
# |-----------------------------------------------------------------------------|
    def updateSlider(self, position):
        """
        This method is used to update the slider position.
        """
        # blocking the signals to avoid reverse callback to set the position
        self.seekSlider.blockSignals(True)
        self.seekSlider.setValue(position)
        position = int(position / 1000)
        self.currentLabel.setText(f"{position // 60}:{position % 60:02d}")
        self.seekSlider.blockSignals(False)
# |--------------------------End of updateSlider--------------------------------|
