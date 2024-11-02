import PyQt6.QtCore
import PyQt6.QtWidgets
import upnpy
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtGui import QAction
from MyMediaPlayer import MyMediaPlayer
from MyMediaControls import MyMediaControls
from MyCentralWidget import MyCentralWidget
from MyThumbnailDisplay import MyThumbnailDisplay
from MyPlaylist import MyPlaylist
from MyPreview import MyPreview
from MyNetworkTree import MyNetworkTree
from processTools import ExtractImages
from processTools import PreviewPosition
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
        self.playlist = MyPlaylist()
        self.networktree = MyNetworkTree()
        self.preview = MyPreview()
        self.__previewExtract = None
        self.playlist.hide()
        self.networktree.hide()
        self.networktree = MyNetworkTree()
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
        # self.reelDisplay = MyThumbnailDisplay(self.mainWidget)
        self.mediaControls = MyMediaControls()
        # add media player and controls to the layout
        self.mainWidget.addWidget(self.mediaPlayer)
        # self.mainWidget.addWidget(self.reelDisplay)
        # self.reelDisplay.setMaximumHeight(100)
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
        self.networktree.playMediaFile.connect(self.playNetworkURL)
        self.mediaControls.playMedia.connect(self.mediaPlayer.mediaPlayer.play)
        self.mediaControls.pauseMedia.connect(
            self.mediaPlayer.mediaPlayer.pause)
        self.mediaControls.stopButton.clicked.connect(
            self.mediaPlayer.mediaPlayer.stop)
        self.mediaControls.seekSlider.valueChanged.connect(
            self.mediaPlayer.mediaPlayer.setPosition)
        self.mediaControls.seekSlider.showPreview.connect(self.previewDisplay)
        # from media player to media controls
        # need to connect positionChanged, durationChanged,
        # mediaStatusChanged, playbackStateChanged
        # using only video player for now (audio player is not used)
        self.mediaPlayer.mediaPlayer.positionChanged.connect(
            self.mediaControls.updateSlider)
        self.mediaPlayer.mediaPlayer.durationChanged.connect(
            self.mediaControls.seekSlider.setMaximum)
        # self.mediaPlayer.mediaPlayer.positionChanged.connect(
        #     self.reelDisplay.setPosition)
        self.mediaPlayer.mediaPlayer.mediaStatusChanged.connect(
            self.__reflectMediaStatus)
        self.mediaPlayer.mediaPlayer.playbackStateChanged.connect(
            self.__reflectMediaStatus)
# |--------------------------End of __connectMediaControls----------------------|

# |-----------------------------------------------------------------------------|
# __reflectMediaStatus :-
# |-----------------------------------------------------------------------------|
    def __reflectMediaStatus(self):
        """
        This method is used to reflect the status of the media file.
        """
        playState = self.mediaPlayer.mediaPlayer.playbackState()
        mediaStatus = self.mediaPlayer.mediaPlayer.mediaStatus()
        self.mediaControls.playButton.setChecked(
            playState == QMediaPlayer.PlaybackState.PlayingState)
        self.mediaControls.stopButton.setEnabled(
            playState == QMediaPlayer.PlaybackState.PlayingState)
        self.mediaControls.seekSlider.setEnabled(
            mediaStatus != QMediaPlayer.MediaStatus.NoMedia)
        self.mediaControls.seekSlider.setValue(
            self.mediaPlayer.mediaPlayer.position())
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

        openAction = QAction("Open", self)
        openAction.triggered.connect(self.__openFileDailog)
        menuBar.addAction(openAction)

        playlistAction = QAction("Playlist", self)
        playlistAction.triggered.connect(self.showPlaylist)
        menuBar.addAction(playlistAction)

        networkAction = QAction("Network", self)
        networkAction.triggered.connect(self.showNetwork)
        menuBar.addAction(networkAction)

        exitAction = QAction("Exit", self)
        exitAction.triggered.connect(self.close)
        menuBar.addAction(exitAction)

        self.setMenuBar(menuBar)
# |--------------------------End of __addMenuBar--------------------------------|

# |-----------------------------------------------------------------------------|
# previewDisplay :-
# |-----------------------------------------------------------------------------|
    def previewDisplay(self, display):
        if display and self.__previewExtract:
            pp = display[0]/self.mediaControls.seekSlider.width()
            qimg = self.__previewExtract.extract(pp)
            self.preview.setGeometry(
                int(display[0]), int(display[1]+self.height()-200),
                int(self.preview.width()), int(self.preview.height()))
            self.preview.showImage(qimg)
            self.preview.show()
        else:
            self.preview.hide()
# |--------------------------End of showPlaylist--------------------------------|


# |-----------------------------------------------------------------------------|
# showPlaylist :-
# |-----------------------------------------------------------------------------|


    def showPlaylist(self):
        self.playlist.show()
# |--------------------------End of showPlaylist--------------------------------|

# |-----------------------------------------------------------------------------|
# showNetwork :-
# |-----------------------------------------------------------------------------|
    def showNetwork(self):
        # Initialize UPnP object
        upnp = upnpy.UPnP()
        # Discover UPnP devices on the network
        devices = upnp.discover()
        # Find the media server device
        for device in devices:
            print(device)
            try:
                # Get the services available for the media server
                services = device.get_services()
                # Assuming the ContentDirectory service is available
                content_directory = None
                if 'ContentDirectory' in ",".join([service.id for service in services]):
                    content_directory = [
                        service for service in services if "ContentDirectory" in service.id][0]
                if content_directory:
                    self.networktree.addParentItem(
                        device.friendly_name, browse=content_directory.actions['Browse'])
            except Exception as ex:
                print(f"Exception {ex}")

        self.networktree.show()
# |--------------------------End of showNetwork---------------------------------|

# |-----------------------------------------------------------------------------|
# __displayReelContent :-
# |-----------------------------------------------------------------------------|
    def __displayReelContent(self):
        self.__imageExtract = []
        count = 8
        self.reelDisplay.clearDisplay()
        durationSec = int(checkDuration(self.__fileName))
        self.reelDisplay.setDuration(durationSec)
        self.mediaControls.seekSlider.duration = durationSec
        self.mediaControls.durationLabel.setText(
            f"{durationSec // 60}:{durationSec % 60:02d}")
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
# |------------------End of __displayReelContent--------------------------------|

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
            self.__previewExtract = PreviewPosition(self.__fileName)
            # self.__displayReelContent()
            self.playlist.addPLItem(self.__fileName)
            self.mediaControls.playMedia.emit()

# |--------------------------End of __openFileDailog----------------------------|
    def playNetworkURL(self, path):
        self.__fileName = path
        self.mediaPlayer.setMediaFile(self.__fileName)
        self.__previewExtract = PreviewPosition(self.__fileName)
        # self.__displayReelContent()
        self.mediaControls.playMedia.emit()


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
