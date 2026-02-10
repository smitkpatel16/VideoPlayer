"""
MyPlaylist.py - Playlist Management

This module provides playlist management functionality for the video player.

Key Components:
- MyPlaylistItem: Custom list widget item storing both display name and full file path
- MyPlaylist: Main playlist window with list view and navigation methods

Key Responsibilities:
- Store and display playlist items with file paths
- Set and highlight the currently playing item
- Navigate to previous/next items in the playlist
- Extract and display file names

Dependencies:
- PyQt6: GUI components (QMainWindow, QListWidget, QListWidgetItem)
"""

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
        """
        Adds a media file to the playlist.

        Args:
            fullPath (str): Complete file path to the media

        Extracts the filename from the path for display and creates
        a playlist item storing both the display name and full path.
        """
        # Extract filename from full path (last component after /)
        fn = fullPath.split("/")[-1]
        # Create a new playlist item
        it = MyPlaylistItem(fn, fullPath)
        # Add it to the playlist widget
        self.mainWidget.addItem(it)
# |--------------------------End of addPLItem-----------------------------------|

# |-----------------------------------------------------------------------------|
# setActiveItem :-
# |-----------------------------------------------------------------------------|
    def setActiveItem(self, fullPath):
        """
        Highlights the currently playing item in the playlist.

        Args:
            fullPath (str): Full path of the file to highlight

        Searches for the item with matching file path and sets it as current.
        """
        # Iterate through all items in the playlist
        for itemIndex in range(self.mainWidget.count()):
            item = self.mainWidget.item(itemIndex)
            # Check if this item's path matches the target
            if item.fullPath == fullPath:
                # Set as current item (highlighted)
                self.mainWidget.setCurrentItem(item)
                break
# |-------------------------End of setActiveItem--------------------------------|

# |-----------------------------------------------------------------------------|
# setPrev :-
# |-----------------------------------------------------------------------------|
    def setPrev(self):
        """
        Navigates to the previous item in the playlist.

        Moves selection to the item before the current one.
        """
        # Get current item's index
        row = self.mainWidget.currentRow()-1
        # Get the item at the previous position
        item = self.mainWidget.item(row)
        # Set it as current
        self.mainWidget.setCurrentItem(item)
# |--------------------------End of setPrev-------------------------------------|

# |-----------------------------------------------------------------------------|
# setPrev :-
# |-----------------------------------------------------------------------------|
    def setNext(self):
        """
        Navigates to the next item in the playlist.

        Moves selection to the item after the current one.
        """
        # Get current item's index
        row = self.mainWidget.currentRow()+1
        # Get the item at the next position
        item = self.mainWidget.item(row)
        # Set it as current
        self.mainWidget.setCurrentItem(item)
# |--------------------------End of setPrev-------------------------------------|
