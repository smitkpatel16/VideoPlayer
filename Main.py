import PyQt6.QtCore
import PyQt6.QtWidgets
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtGui import QAction
from MyMediaPlayer import MyMediaPlayer
from MyMediaControls import MyMediaControls
from MyCentralWidget import MyCentralWidget
from MyThumbnailDisplay import MyThumbnailDisplay
from processTools import ExtractImages
from processTools import checkDuration
from PyQt6.QtCore import QThread


# ===============================================================================
# MyVideoPlayer-
# ===============================================================================
class MyVideoPlayer(PyQt6.QtWidgets.QMainWindow):
    """
    This class is used to create a video player using PyQt6.
    """

# |-----------------------------------------------------------------------------|
# Constructor :-
# |-----------------------------------------------------------------------------|
    def __init__(self, *args, **kwargs):
        """
        This constructor is used to initialize the main window of the video player.
        """
        super(MyVideoPlayer, self).__init__(*args, **kwargs)
        self.setWindowTitle("My Video Player")
        self.setGeometry(100, 100, 800, 600)
        # Add a menu bar to the main window
        self.__addMenuBar()
        # add my media player and controls
        self.__addMyMediaPlayerWidget()
        # connect media controls to the media player
        self.__connectMediaControls()
        self.__threads = []
        self.show()
# |--------------------------End of Constructor--------------------------------|

# |-----------------------------------------------------------------------------|
# __addMyMediaPlayerWidget :-
# |-----------------------------------------------------------------------------|
    def __addMyMediaPlayerWidget(self):
        """
        This method is used to add my media player and controls of the video player.
        """
        # create a main widget
        self.mainWidget = MyCentralWidget()
        self.setCentralWidget(self.mainWidget)
        # Add my media player and controls
        self.mediaPlayer = MyMediaPlayer()
        self.reelDisplay = MyThumbnailDisplay(self.mainWidget)
        self.mediaControls = MyMediaControls()
        # add media player and controls to the layout
        self.mainWidget.addWidget(self.mediaPlayer)
        self.mainWidget.addWidget(self.reelDisplay)
        self.reelDisplay.setMaximumHeight(100)
        self.mainWidget.addWidget(self.mediaControls)
        # adjust the size of the widgets
        self.mainWidget.adjustWidgetSizes()
# |--------------End of __addMyMediaPlayerWidget--------------------------------|

# |-----------------------------------------------------------------------------|
# __connectMediaControls :-
# |-----------------------------------------------------------------------------|
    def __connectMediaControls(self):
        """
        Connect the media controls to the media player.
        """
        # from media controls to media player
        # need to connect play, pause, stop, seek for both audio and video
        self.mediaControls.playMedia.connect(self.mediaPlayer.videoPlayer.play)
        self.mediaControls.playMedia.connect(self.mediaPlayer.audioPlayer.play)
        self.mediaControls.pauseMedia.connect(
            self.mediaPlayer.videoPlayer.pause)
        self.mediaControls.pauseMedia.connect(
            self.mediaPlayer.audioPlayer.pause)
        self.mediaControls.stopButton.clicked.connect(
            self.mediaPlayer.videoPlayer.stop)
        self.mediaControls.stopButton.clicked.connect(
            self.mediaPlayer.audioPlayer.stop)
        self.mediaControls.seekSlider.valueChanged.connect(
            self.mediaPlayer.videoPlayer.setPosition)
        self.mediaControls.seekSlider.valueChanged.connect(
            self.mediaPlayer.audioPlayer.setPosition)
        # from media player to media controls
        # need to connect positionChanged, durationChanged,
        # mediaStatusChanged, playbackStateChanged
        # using only video player for now (audio player is not used)
        self.mediaPlayer.videoPlayer.positionChanged.connect(
            self.mediaControls.updateSlider)
        self.mediaPlayer.videoPlayer.durationChanged.connect(
            self.mediaControls.seekSlider.setMaximum)
        self.mediaPlayer.videoPlayer.mediaStatusChanged.connect(
            self.__reflectMediaStatus)
        self.mediaPlayer.videoPlayer.playbackStateChanged.connect(
            self.__reflectMediaStatus)
# |--------------------------End of __connectMediaControls----------------------|

# |-----------------------------------------------------------------------------|
# __reflectMediaStatus :-
# |-----------------------------------------------------------------------------|
    def __reflectMediaStatus(self):
        """
        This method is used to reflect the status of the media file.
        """
        playState = self.mediaPlayer.videoPlayer.playbackState()
        mediaStatus = self.mediaPlayer.videoPlayer.mediaStatus()
        self.mediaControls.playButton.setChecked(
            playState == QMediaPlayer.PlaybackState.PlayingState)
        self.mediaControls.stopButton.setEnabled(
            playState == QMediaPlayer.PlaybackState.PlayingState)
        self.mediaControls.seekSlider.setEnabled(
            mediaStatus != QMediaPlayer.MediaStatus.NoMedia)
        self.mediaControls.seekSlider.setValue(
            self.mediaPlayer.videoPlayer.position())
# |----------------------End of __reflectMediaStatus----------------------------|

# |-----------------------------------------------------------------------------|
# __addMenuBar :-
# |-----------------------------------------------------------------------------|
    def __addMenuBar(self):
        """
        This method is used to add a menu bar
        to the main window of the video player.
        """
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu("File")
        openAction = QAction("Open", self)
        openAction.triggered.connect(self.__openFileDailog)
        fileMenu.addAction(openAction)
        exitAction = QAction("Exit", self)
        fileMenu.addAction(exitAction)
        exitAction.triggered.connect(self.close)
        self.setMenuBar(menuBar)
# |--------------------------End of __addMenuBar--------------------------------|

# |-----------------------------------------------------------------------------|
# __openFileDailog :-
# |-----------------------------------------------------------------------------|
    def __openFileDailog(self):
        """
        This method is used to open a file dialog to select a video file.
        """
        self.__fileName, _ = PyQt6.QtWidgets.QFileDialog.getOpenFileName(
            self, "Open Video File", "",
            "All Files (*);;Video Files (*.mp4 *.flv *.ts *.mts *.avi)")
        if self.__fileName:
            self.mediaPlayer.setMediaFile(self.__fileName)
            self.__imageExtract = []
            count = 8
            self.reelDisplay.clearDisplay()
            self.reelDisplay.setDuration(checkDuration(self.__fileName))
            self.mediaPlayer.videoPlayer.positionChanged.connect(
                self.reelDisplay.setPosition)
            self.mediaControls.playMedia.emit()
            for i in range(count):
                self.__imageExtract.append(ExtractImages(
                    fPath=self.__fileName, split=count, pos=i))
                self.__imageExtract[i].reelImage.connect(
                    self.reelDisplay.addImage)
                self.__threads.append(QThread(self))
                t = self.__threads[-1]
                self.__imageExtract[i].moveToThread(t)
                self.__imageExtract[i].finished.connect(t.quit)
                self.__imageExtract[i].finished.connect(
                    self.__imageExtract[i].deleteLater)
                t.finished.connect(t.deleteLater)
                t.started.connect(self.__imageExtract[i].run)
                t.start()
# |--------------------------End of __openFileDailog----------------------------|


# MainWindow of a PyQt6 application
# |-----------------------------------------------------------------------------|
# main executor :-
# |-----------------------------------------------------------------------------|
if __name__ == "__main__":
    import sys
    app = PyQt6.QtWidgets.QApplication(sys.argv)
    window = MyVideoPlayer()
    sys.exit(app.exec())
# |--------------------------End of main executor--------------------------------|
