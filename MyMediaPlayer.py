# Inherit and create a new class MyMediaPlayer from QVideoWidget
# that can encompass the media player functionality.
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtCore import QUrl


# ===============================================================================
# MyMediaPlayer-
# ===============================================================================
class MyMediaPlayer(QVideoWidget):
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
        self.player = QMediaPlayer()
        self.player.setVideoOutput(self)
# |--------------------------End of Constructor--------------------------------|

# |-----------------------------------------------------------------------------|
# playMediaFile :-
# |-----------------------------------------------------------------------------|
    def playMediaFile(self, filePath):
        """
        This method is used to play a media file.
        """
        self.player.setSource(QUrl.fromLocalFile(filePath))
        self.player.play()
# |--------------------------End of playMediaFile-------------------------------|
