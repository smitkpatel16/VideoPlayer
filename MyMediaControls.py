from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QSlider
from PyQt6.QtWidgets import QStyle
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtCore import pyqtSignal
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
        # Arrange the widgets in the layout
        self.__arrangeWidgets()
# |--------------------------End of Constructor--------------------------------|

# |-----------------------------------------------------------------------------|
# __addControls :-
# |-----------------------------------------------------------------------------|
    def __addControls(self):
        """
        This method is used to add media controls to the layout.
        """
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
        # Create a seek slider
        self.seekSlider = QSlider()
        # Set the orientation of the seek slider
        self.seekSlider.setOrientation(Qt.Orientation.Horizontal)
# |--------------------------End of __addControls--------------------------------|

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
# __arrangeWidgets :-
# |-----------------------------------------------------------------------------|
    def __arrangeWidgets(self):
        """
        This method is used to arrange the widgets in the layout.
        """
        # Create a local horizontal layout
        hlayout = QHBoxLayout()
        # Add play, pause, and stop buttons
        hlayout.addWidget(self.playButton)
        hlayout.addWidget(self.stopButton)
        # Create a vertical layout
        vlayout = QVBoxLayout()
        # Add seek slider to the vertical layout
        vlayout.addWidget(self.seekSlider)
        # Add the horizontal layout to the vertical layout
        vlayout.addLayout(hlayout)
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
        self.seekSlider.blockSignals(True)
        self.seekSlider.setValue(position)
        self.seekSlider.blockSignals(False)
# |--------------------------End of updateSlider--------------------------------|
