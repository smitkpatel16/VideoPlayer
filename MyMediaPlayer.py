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
        ao = self.__meidaDevices.defaultAudioOutput()
        self.__audio.setDevice(ao)

# |--------------------------End of Constructor--------------------------------|

# |-----------------------------------------------------------------------------|
# playMediaFile :-
# |-----------------------------------------------------------------------------|
    def setMediaFile(self, filePath):
        """
        This method is used to play a media file.
        """
        self.mediaPlayer.setSource(QUrl.fromLocalFile(filePath))
        # publish the status of media file
# |--------------------------End of playMediaFile-------------------------------|

    def adjustVolume(self, volume):
        if volume > 0:
            scale = math.log(volume)/math.log(100)
        else:
            scale = 0
        self.__audio.setVolume(scale)

# |-----------------------------------------------------------------------------|
# toggleFullScreen :-
# |-----------------------------------------------------------------------------|
    def toggleFullScreen(self):
        """
        This method is used to toggle full screen mode.
        """
        if not self.__fullScreen:
            self.__videoWidget.setFullScreen(True)
            self.__fullScreen = True
        else:
            self.__videoWidget.setFullScreen(False)
            self.__fullScreen = False

    def isFullScreen(self):
        return self.__fullScreen

    def eventFilter(self, source, event):
        if event.type() == PyQt6.QtCore.QEvent.Type.KeyPress:
            if event.key() == PyQt6.QtCore.Qt.Key.Key_Escape:
                if self.isFullScreen():
                    self.toggleFullScreen()
                    return True
            # Forward other keys to parent (Main) if needed, or let them propagate
            # Only consume Esc if fullscreen
        return super().eventFilter(source, event)

# |--------------------------End of toggleFullScreen----------------------------|
