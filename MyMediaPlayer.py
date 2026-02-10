"""
MyMediaPlayer.py - Media Playback Engine

This module provides the MyMediaPlayer class, which wraps PyQt6's media player functionality
to provide video playback with audio output control.

Key Responsibilities:
- Initialize and manage QMediaPlayer for playback
- Manage QVideoWidget for video display
- Configure audio output and device selection
- Provide volume control with logarithmic scaling
- Toggle fullscreen mode for video display
- Handle keyboard events (Escape to exit fullscreen)

The class encapsulates the PyQt6 multimedia components and provides a simplified interface
for the video player application.

Dependencies:
- PyQt6.QtMultimediaWidgets: QVideoWidget
- PyQt6.QtMultimedia: QMediaPlayer, QAudioOutput, QMediaDevices
- math: For logarithmic volume scaling
"""

# Inherit and create a new class MyMediaPlayer from QVideoWidget
# that can encompass the media player functionality.
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtMultimedia import QAudioOutput
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtMultimedia import QMediaDevices
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import QWidget
import math
import PyQt6.QtCore


# ===============================================================================
# MyMediaPlayer-
# ===============================================================================
class MyMediaPlayer(QWidget):
    """
    This class is used to create a media player using PyQt6.
    """
# |-----------------------------------------------------------------------------|
# Constructor :-
# |-----------------------------------------------------------------------------|

    def __init__(self, *args, **kwargs):
        """
        This constructor is used to initialize the media player.
        """
        super(MyMediaPlayer, self).__init__(*args, **kwargs)
        self.mediaPlayer = QMediaPlayer(self)
        self.__meidaDevices = QMediaDevices(self)
        self.__videoWidget = QVideoWidget(self)
        self.__videoWidget.installEventFilter(self)
        self.__videoWidget.setMouseTracking(True)
        self.__fullScreen = False
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.__videoWidget)
        self.__audio = QAudioOutput(self)
        self.mediaPlayer.setVideoOutput(self.__videoWidget)
        self.mediaPlayer.setAudioOutput(self.__audio)
        self.__updateAudioOutputs()
        self.__meidaDevices.audioOutputsChanged.connect(
            self.__updateAudioOutputs)

    def __updateAudioOutputs(self):
        """
        Updates the audio output device to the system default.

        Called automatically when:
        1. Media player is initialized
        2. System audio devices change

        This ensures the application uses the current default audio device,
        adapting to device changes like speaker/headphone switching.
        """
        # Get the system's default audio output device
        ao = self.__meidaDevices.defaultAudioOutput()
        # Set this device as the output for the audio
        self.__audio.setDevice(ao)

    def videoWidget(self):
        """
        Returns the underlying QVideoWidget used for rendering video.

        Returns:
            QVideoWidget: The video display widget

        This widget can be used to:
        - Apply event filters
        - Get geometry information
        - Set fullscreen mode
        """
        return self.__videoWidget

# |--------------------------End of Constructor--------------------------------|

# |-----------------------------------------------------------------------------|
# playMediaFile :-
# |-----------------------------------------------------------------------------|
    def setMediaFile(self, filePath):
        """
        Sets a media file to be played.

        Args:
            filePath (str): Absolute file path to the media file

        The file is converted to a URL and loaded into the media player.
        This prepares the file for playback but doesn't start playing it.
        Call QMediaPlayer.play() to start playback.
        """
        # Convert file path to QUrl and set as media source
        self.mediaPlayer.setSource(QUrl.fromLocalFile(filePath))
# |--------------------------End of playMediaFile-------------------------------|

    def adjustVolume(self, volume):
        """
        Adjusts the volume using logarithmic scaling.

        Args:
            volume (int): Linear volume level (0-100)

        The method converts linear volume to logarithmic scale for more natural
        volume perception. This provides better control at lower volumes.

        Formula: scale = log(volume) / log(100) for volume > 0, else 0
        """
        if volume > 0:
            # Convert linear volume (0-100) to logarithmic scale (0-1)
            # This provides more perceptually uniform volume changes
            scale = math.log(volume)/math.log(100)
        else:
            # Mute when volume is 0
            scale = 0
        # Apply the scaled volume to audio output
        self.__audio.setVolume(scale)

# |-----------------------------------------------------------------------------|
# toggleFullScreen :-
# |-----------------------------------------------------------------------------|
    def toggleFullScreen(self):
        """
        Toggles the fullscreen state of the video display.

        When fullscreen is enabled:
        - Video expands to cover the entire display
        - Aspect ratio is maintained

        When fullscreen is disabled:
        - Video returns to windowed display within the application
        """
        if not self.__fullScreen:
            # Enter fullscreen mode
            self.__videoWidget.setFullScreen(True)
            self.__fullScreen = True
        else:
            # Exit fullscreen mode
            self.__videoWidget.setFullScreen(False)
            self.__fullScreen = False

    def isFullScreen(self):
        """
        Returns the current fullscreen state.

        Returns:
            bool: True if video is in fullscreen mode, False otherwise
        """
        return self.__fullScreen

    def eventFilter(self, source, event):
        """
        Handles keyboard events for the video widget.

        Currently handles:
        - Escape key: Exits fullscreen mode

        Args:
            source: The object that generated the event
            event: The event object

        Returns:
            bool: True if event was handled and consumed, False otherwise
        """
        if event.type() == PyQt6.QtCore.QEvent.Type.KeyPress:
            if event.key() == PyQt6.QtCore.Qt.Key.Key_Escape:
                # Exit fullscreen when Escape is pressed
                if self.isFullScreen():
                    self.toggleFullScreen()
                    return True  # Consume the event
            # Forward other keys to parent (Main) if needed, or let them propagate
            # Only consume Esc if fullscreen
        return super().eventFilter(source, event)

# |--------------------------End of toggleFullScreen----------------------------|
