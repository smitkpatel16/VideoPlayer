"""
Main.py - Main Application Entry Point

This module contains the MyVideoPlayer class, which serves as the main application window
for the VideoPlayer application. It orchestrates all UI components including media player,
controls, playlist, network browsing, and preview functionality.

Key Responsibilities:
- Application window management and setup
- Menu bar creation and event handling
- Keyboard shortcuts and fullscreen mode
- Signal/slot connections between components
- File dialog management for loading media
- Network device discovery via UPnP
- Preview generation during timeline scrubbing
- Playback state synchronization across UI components

Dependencies:
- PyQt6: GUI framework (QMainWindow, QSettings, QMediaPlayer, QAction)
- upnpy: UPnP device discovery and control
- Custom modules: MyMediaPlayer, MyMediaControls, MyCentralWidget, MyPlaylist, MyPreview, MyNetworkTree
- Utilities: PreviewPosition, checkDuration from processTools
"""

import upnpy
import os
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QSettings
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtGui import QAction
from MyMediaPlayer import MyMediaPlayer
from MyMediaControls import MyMediaControls
from MyCentralWidget import MyCentralWidget
from MyPlaylist import MyPlaylist
from MyPreview import MyPreview
from MyNetworkTree import MyNetworkTree
from processTools import PreviewPosition
from processTools import checkDuration
from PyQt6.QtCore import pyqtSlot


# ===============================================================================
# MyVideoPlayer-
# ===============================================================================
class MyVideoPlayer(QMainWindow):
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
        self.settings = QSettings(
            "MyVideoPlayerCode", "MyVideoPlayer")
        self.playlist = MyPlaylist()
        self.networktree = MyNetworkTree()
        self.preview = MyPreview()
        self.__previewExtract = None
        self.__fileNames = []
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

        self.hideTimer = PyQt6.QtCore.QTimer(self)
        self.hideTimer.timeout.connect(self.hideControls)

        self.show()
# |--------------------------End of Constructor--------------------------------|

    def keyPressEvent(self, event):
        if event.key() == PyQt6.QtCore.Qt.Key.Key_F:
            self.toggleFullScreen()
        elif event.key() == PyQt6.QtCore.Qt.Key.Key_Escape:
            if self.mediaPlayer.isFullScreen():
                self.toggleFullScreen()
        elif event.key() == PyQt6.QtCore.Qt.Key.Key_Space:
            self.mediaControls.playButton.click()
        elif event.key() == PyQt6.QtCore.Qt.Key.Key_Left:
            self.mediaPlayer.mediaPlayer.setPosition(
                self.mediaPlayer.mediaPlayer.position() - 5000)
        elif event.key() == PyQt6.QtCore.Qt.Key.Key_Right:
            self.mediaPlayer.mediaPlayer.setPosition(
                self.mediaPlayer.mediaPlayer.position() + 5000)
        elif event.key() == PyQt6.QtCore.Qt.Key.Key_Up:
            self.mediaPlayer.adjustVolume(
                min(self.mediaPlayer.volume + 10, 100))
        elif event.key() == PyQt6.QtCore.Qt.Key.Key_Down:
            self.mediaPlayer.adjustVolume(max(self.mediaPlayer.volume - 10, 0))
        return super().keyPressEvent(event)

    def toggleFullScreen(self):
        if self.mediaPlayer.isFullScreen():
            self.mediaPlayer.toggleFullScreen()
            # Restore controls to main widget
            self.mediaControls.setParent(self.mainWidget)
            self.mediaControls.setWindowFlags(
                PyQt6.QtCore.Qt.WindowType.Widget)
            self.mediaControls.setStyleSheet("")
            self.mediaControls.show()
            # Add back to layout
            self.mainWidget.layout().addWidget(self.mediaControls)
            # Remove event filter
            self.mediaPlayer.videoWidget().removeEventFilter(self)
            self.setCursor(PyQt6.QtCore.Qt.CursorShape.ArrowCursor)
            self.menuBar().show()
            self.hideTimer.stop()
        else:
            self.mediaPlayer.toggleFullScreen()
            # Parent controls to video widget for overlay
            self.mediaControls.setParent(self.mediaPlayer.videoWidget())
            self.mediaControls.setWindowFlags(
                PyQt6.QtCore.Qt.WindowType.FramelessWindowHint)
            self.mediaControls.setAttribute(
                PyQt6.QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
            self.mediaControls.setStyleSheet(
                "background-color: rgba(0, 0, 0, 128); color: white; border-radius: 10px;")

            # Position controls at bottom
            self.updateControlsPosition()
            self.mediaControls.show()
            self.mediaControls.raise_()

            # Install event filter for hover detection
            self.mediaPlayer.videoWidget().installEventFilter(self)
            self.menuBar().hide()

            # Auto-hide timer
            self.hideTimer.start(3000)

    def updateControlsPosition(self):
        if self.mediaPlayer.isFullScreen():
            video_geo = self.mediaPlayer.videoWidget().geometry()
            controls_height = self.mediaControls.sizeHint().height()
            controls_width = int(video_geo.width() * 0.8)  # 80% width
            x = (video_geo.width() - controls_width) // 2
            y = video_geo.height() - controls_height - 20  # 20px padding from bottom
            self.mediaControls.setGeometry(
                x, y, controls_width, controls_height)

    def eventFilter(self, source, event):
        if self.mediaPlayer.isFullScreen() and source == self.mediaPlayer.videoWidget():
            if event.type() == PyQt6.QtCore.QEvent.Type.MouseMove:
                self.mediaControls.show()
                self.setCursor(PyQt6.QtCore.Qt.CursorShape.ArrowCursor)
                self.hideTimer.start(3000)  # Reset timer
            elif event.type() == PyQt6.QtCore.QEvent.Type.Resize:
                self.updateControlsPosition()

        return super().eventFilter(source, event)

    def hideControls(self):
        if self.mediaPlayer.isFullScreen():
            self.mediaControls.hide()
            self.setCursor(PyQt6.QtCore.Qt.CursorShape.BlankCursor)

    # Original implementation (commented out) preserved below:
        # if self.isFullScreen():
        #     self.showNormal()
        #     self.menuBar().show()
        #     self.mediaControls.show()
        # else:
        #     self.showFullScreen()
        #     self.menuBar().hide()
            # self.mediaControls.hide() # Keep controls visible for now or implement auto-hide

# |-----------------------------------------------------------------------------|
# __addMyMediaPlayerWidget :-
# |-----------------------------------------------------------------------------|
    def __addMyMediaPlayerWidget(self):
        """
        This method is used to add my media player and controls of the video player.
        """
        # create a main widget
        self.mainWidget = MyCentralWidget()
        # allow light and dark theme support with a swtich
        self.setStyleSheet("background-color: #2E2E2E; color: white;")
        # create a preview widget
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
        self.mediaControls.volumeDial.valueChanged.connect(
            self.mediaPlayer.adjustVolume)
        self.mediaControls.seekSlider.showPreview.connect(self.previewDisplay)
        self.mediaControls.seekSlider.enterPreview.connect(
            self.mediaPlayer.mediaPlayer.pause)
        self.mediaControls.seekSlider.exitPreview.connect(
            self.mediaPlayer.mediaPlayer.play)
        self.mediaControls.prev.connect(self.playlist.setPrev)
        self.mediaControls.next.connect(self.playlist.setNext)
        self.playlist.mainWidget.itemSelectionChanged.connect(
            self.manageControl)
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
# manageControl :-
# |-----------------------------------------------------------------------------|
    def manageControl(self):
        count = self.playlist.mainWidget.count()
        currentRow = self.playlist.mainWidget.currentRow()
        if currentRow == 0:
            self.mediaControls.prevBtn.setDisabled(True)
        else:
            self.mediaControls.prevBtn.setEnabled(True)
        if currentRow == count-1:
            self.mediaControls.nextBtn.setDisabled(True)
        else:
            self.mediaControls.nextBtn.setEnabled(True)
        item = self.playlist.mainWidget.currentItem()
        self.__playFile(item.fullPath)
# |-------------------------End of manageControl--------------------------------|

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

        viewMenu = menuBar.addMenu("View")
        fullscreenAction = QAction("Fullscreen", self)
        fullscreenAction.setShortcut("F")
        fullscreenAction.triggered.connect(self.toggleFullScreen)
        viewMenu.addAction(fullscreenAction)

        self.setMenuBar(menuBar)
# |--------------------------End of __addMenuBar--------------------------------|

# |-----------------------------------------------------------------------------|
# previewDisplay :-
# |-----------------------------------------------------------------------------|
    @pyqtSlot(tuple)
    def previewDisplay(self, display):
        if display and self.__previewExtract:
            pp = int((display[2]/1000)*self.__fr)
            qimg = self.__previewExtract.extract(pp)
            if qimg:
                # Center the preview above the cursor using global coordinates
                preview_width = self.preview.width()
                preview_height = self.preview.height()
                x = display[0] - (preview_width // 2)
                y = display[1] - preview_height - 10

                self.preview.setGeometry(
                    int(x), int(y),
                    int(preview_width), int(preview_height))
                s = display[2]/1000
                t = f"{int(s//60)}:{int(s % 60):02d}"
                self.preview.showImage(qimg, t)
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
        devices = upnp.discover(delay=5)
        # Find the media server device
        for device in devices:
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
        # self.__imageExtract = []
        # count = 8
        # self.reelDisplay.clearDisplay()
        durationSec, self.__fc, self.__fr = checkDuration(self.__fileNames[0])
        durationSec = int(durationSec)
        # self.reelDisplay.setDuration(durationSec)
        self.mediaControls.seekSlider.duration = durationSec
        self.mediaControls.durationLabel.setText(
            f"{durationSec // 60}:{durationSec % 60:02d}")
        # for i in range(count):
        #     self.__imageExtract.append(ExtractImages(
        #         fPath=self.__fileName, split=count, pos=i))
        #     self.__imageExtract[i].reelImage.connect(
        #         self.reelDisplay.addImage)
        #     self.__threads.append(QThread(self))
        #     t = self.__threads[-1]
        #     self.__imageExtract[i].moveToThread(t)
        #     self.__imageExtract[i].finished.connect(t.quit)
        #     self.__imageExtract[i].finished.connect(
        #         self.__imageExtract[i].deleteLater)
        #     t.finished.connect(t.deleteLater)
        #     t.started.connect(self.__imageExtract[i].run)
        #     t.start()
# |------------------End of __displayReelContent--------------------------------|

# |-----------------------------------------------------------------------------|
# __playFile :-
# |-----------------------------------------------------------------------------|
    def __playFile(self, fileName):
        self.mediaPlayer.setMediaFile(fileName)
        self.__previewExtract = PreviewPosition(fileName)
        self.playlist.setActiveItem(fileName)
        self.mediaControls.playMedia.emit()

# |--------------------------End of __playFile----------------------------------|

# |-----------------------------------------------------------------------------|
# __openFileDailog :-
# |-----------------------------------------------------------------------------|
    def __openFileDailog(self):
        """
        This method is used to open a file dialog to select a video file.
        """
        last_dir = self.settings.value("last_dir", "")
        self.__fileNames, _ = PyQt6.QtWidgets.QFileDialog.getOpenFileNames(
            self, "Open Video File", last_dir,
            "All Files (*);;Video Files (*.mp4 *.flv *.ts *.mts *.avi)")
        if self.__fileNames:
            directory = os.path.dirname(self.__fileNames[0])
            self.settings.setValue("last_dir", directory)
            for fn in self.__fileNames:
                self.__displayReelContent()
                self.playlist.addPLItem(fn)
            self.__playFile(self.__fileNames[0])

    def playNetworkURL(self, path):
        self.__fileNames.append(path)
        self.mediaPlayer.setMediaFile(path)
        self.__previewExtract = PreviewPosition(path)
        self.__displayReelContent()
        self.mediaControls.playMedia.emit()


# MainWindow of a PyQt6 application
# |-----------------------------------------------------------------------------|
# main executor :-
# |-----------------------------------------------------------------------------|
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MyVideoPlayer()
    sys.exit(app.exec())
# |--------------------------End of main executor--------------------------------|
