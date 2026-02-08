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

# |-----------------------------------------------------------------------------|
# setActiveItem :-
# |-----------------------------------------------------------------------------|
    def setActiveItem(self, fullPath):
        for itemIndex in range(self.mainWidget.count()):
            item = self.mainWidget.item(itemIndex)
            if item.fullPath == fullPath:
                self.mainWidget.setCurrentItem(item)
                break
# |-------------------------End of setActiveItem--------------------------------|

# |-----------------------------------------------------------------------------|
# setPrev :-
# |-----------------------------------------------------------------------------|
    def setPrev(self):
        row = self.mainWidget.currentRow()-1
        item = self.mainWidget.item(row)
        self.mainWidget.setCurrentItem(item)
# |--------------------------End of setPrev-------------------------------------|

# |-----------------------------------------------------------------------------|
# setPrev :-
# |-----------------------------------------------------------------------------|
    def setNext(self):
        row = self.mainWidget.currentRow()+1
        item = self.mainWidget.item(row)
        self.mainWidget.setCurrentItem(item)
# |--------------------------End of setPrev-------------------------------------|
