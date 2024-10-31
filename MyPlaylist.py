import PyQt6.QtWidgets
import os.path

# ===============================================================================
# MyPlaylist-
# ===============================================================================


class MyPlaylistItem(PyQt6.QtWidgets.QListWidgetItem):
    """
    This class is used to create a playlist widget item for the video player.
    """

# |-----------------------------------------------------------------------------|
# Constructor :-
# |-----------------------------------------------------------------------------|
    def __init__(self, displayText, fullPath, parent=None):
        """
        This constructor is used to initialize the playlist widget.
        """
        super(MyPlaylistItem, self).__init__(displayText, parent=parent)
        self.displayText = displayText
        self.fullPath = fullPath
# |--------------------------End of Constructor---------------------------------|


# ===============================================================================
# MyPlaylist-
# ===============================================================================
class MyPlaylist(PyQt6.QtWidgets.QMainWindow):
    """
    This class is used to create a playlist widget for the video player.
    """

# |-----------------------------------------------------------------------------|
# Constructor :-
# |-----------------------------------------------------------------------------|
    def __init__(self, *args, **kwargs):
        """
        This constructor is used to initialize the playlist widget.
        """
        super(MyPlaylist, self).__init__(*args, **kwargs)
        self.mainWidget = PyQt6.QtWidgets.QListWidget(self)
        self.setCentralWidget(self.mainWidget)
# |--------------------------End of Constructor---------------------------------|

# |-----------------------------------------------------------------------------|
# addPLItem :-
# |-----------------------------------------------------------------------------|
    def addPLItem(self, fullPath):
        fn = fullPath.split("/")[-1]
        it = MyPlaylistItem(fn, fullPath)
        self.mainWidget.addItem(it)

# |--------------------------End of addPLItem-----------------------------------|
