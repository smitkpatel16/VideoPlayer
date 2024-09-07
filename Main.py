import PyQt6.QtWidgets
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget
from MyMediaPlayer import MyMediaPlayer
from MyMediaControls import MyMediaControls


# ===============================================================================
# MyVideoPlayer-
# ===============================================================================
class MyVideoPlayer(object):
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
        self.window = PyQt6.QtWidgets.QMainWindow()
        self.window.setWindowTitle("My Video Player")
        self.window.setGeometry(100, 100, 800, 600)
        # Add a menu bar to the main window
        self.__addMenuBar()
        # add my media player and controls
        self.__addMyMediaPlayerWidget()
# |--------------------------End of Constructor--------------------------------|

# |-----------------------------------------------------------------------------|
# __addMyMediaPlayerWidget :-
# |-----------------------------------------------------------------------------|
    def __addMyMediaPlayerWidget(self):
        """
        This method is used to add my media player and controls of the video player.
        """
        # create a main widget
        self.mainWidget = QWidget()
        self.window.setCentralWidget(self.mainWidget)
        self.mainLayout = QVBoxLayout()
        self.mainWidget.setLayout(self.mainLayout)
        # Add my media player and controls
        self.mediaPlayer = MyMediaPlayer()
        self.mediaControls = MyMediaControls()
        self.mainLayout.addWidget(self.mediaPlayer)
        self.mainLayout.addWidget(self.mediaControls)
# |--------------End of __addMyMediaPlayerWidget--------------------------------|

# |-----------------------------------------------------------------------------|
# show :-
# |-----------------------------------------------------------------------------|
    def show(self):
        """
        This method is used to show the main window of the video player.
        """
        self.window.show()
# |--------------------------End of show----------------------------------------|

# |-----------------------------------------------------------------------------|
# __addMenuBar :-
# |-----------------------------------------------------------------------------|
    def __addMenuBar(self):
        """
        This method is used to add a menu bar
        to the main window of the video player.
        """
        menuBar = self.window.menuBar()
        fileMenu = menuBar.addMenu("File")
        openAction = QAction("Open", self.window)
        openAction.triggered.connect(self.__openFileDailog)
        fileMenu.addAction(openAction)
        exitAction = QAction("Exit", self.window)
        fileMenu.addAction(exitAction)
        exitAction.triggered.connect(self.window.close)
        self.window.setMenuBar(menuBar)
# |--------------------------End of __addMenuBar--------------------------------|

# |-----------------------------------------------------------------------------|
# __openFileDailog :-
# |-----------------------------------------------------------------------------|
    def __openFileDailog(self):
        """
        This method is used to open a file dialog to select a video file.
        """
        fileName, _ = PyQt6.QtWidgets.QFileDialog.getOpenFileName(
            self.window, "Open Video File", "",
            "Video Files (*.mp4 *.flv *.ts *.mts *.avi)")
        if fileName:
            self.mediaPlayer.playMediaFile(fileName)
# |--------------------------End of __openFileDailog----------------------------|


# MainWindow of a PyQt6 application
# |-----------------------------------------------------------------------------|
# main executor :-
# |-----------------------------------------------------------------------------|
if __name__ == "__main__":
    app = PyQt6.QtWidgets.QApplication([])
    window = MyVideoPlayer()
    window.show()
    app.exec()
# |--------------------------End of main executor--------------------------------|
