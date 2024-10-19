# Inherit and create a new class MyMediaPlayer from QVideoWidget
# that can encompass the media player functionality.
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtMultimedia import QAudioOutput
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtMultimedia import QMediaDevices
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtCore import QUrl
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget


class VideoPlayer(QMediaPlayer):
    stopped = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)


class AudioPlayer(QMediaPlayer):
    stopped = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)


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
        self.videoPlayer = VideoPlayer(self)
        self.audioPlayer = AudioPlayer(self)
        self.__meidaDevices = QMediaDevices(self)
        self.__videoWidget = QVideoWidget(self)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.__videoWidget)
        self.__audio = QAudioOutput(self)
        self.videoPlayer.setVideoOutput(self.__videoWidget)
        self.audioPlayer.setAudioOutput(self.__audio)
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
        self.videoPlayer.setSource(QUrl.fromLocalFile(filePath))
        self.audioPlayer.setSource(QUrl.fromLocalFile(filePath))
        # publish the status of media file
# |--------------------------End of playMediaFile-------------------------------|
