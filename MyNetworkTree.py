"""
MyNetworkTree.py - UPnP Network Device Browser

This module provides network browsing capabilities for the video player using UPnP (Universal Plug and Play).
It allows discovering and browsing media servers on the local network.

Key Components:
- browseChildren(): Utility function to query UPnP device content directories
- MyNetworkItem: Custom tree widget item representing a network device or media
- MyNetworkTree: Main window with tree widget for displaying network hierarchy

Key Responsibilities:
- Display UPnP media server devices in a tree view
- Allow expanding devices to browse their content
- Extract media files from device content directories
- Emit signals when media files are selected for playback
- Parse XML responses from UPnP ContentDirectory service

The class uses the lxml library to parse UPnP browse results in XML format.

Dependencies:
- PyQt6: GUI components (QMainWindow, QTreeWidget, QTreeWidgetItem)
- lxml: XML parsing for UPnP responses
- upnpy: (Used by main application for UPnP discovery)
"""

import PyQt6.QtWidgets
from lxml import etree
from PyQt6.QtCore import pyqtSignal


def browseChildren(parentID, browse):
    """
    Queries UPnP device for the children of a given container.

    Args:
        parentID (str): The object ID of the parent container
        browse (callable): The Browse action from UPnP ContentDirectory service

    Returns:
        list: List of tuples containing (objectID, title, [resource_url])
              Each tuple represents a child item (container or resource)

    The function parses the XML response from UPnP and extracts:
    - Object ID (for further browsing or playing)
    - Title (display name)
    - Resource URL (only for playable media items)
    """
    childList = []
    try:
        # Call the UPnP ContentDirectory Browse action
        result = browse(
            ObjectID=parentID,  # Root directory or container ID
            BrowseFlag='BrowseDirectChildren',
            Filter='*',
            StartingIndex=0,
            RequestedCount=500,  # Maximum items per browse
            SortCriteria=''
        )
        # print(result["Result"])
        # Parse the XML content returned by the UPnP device
        root = etree.fromstring(result["Result"])
        # Iterate through each child item in the response
        for child in root.iterchildren():
            # Extract metadata from each item
            for spec in child.iterchildren():
                # Extract title/name
                if "title" in spec.tag:
                    childList.append((child.values()[0], spec.text))
                # Extract resource URL (streaming/playback address)
                if "res" in spec.tag:
                    childList[-1] = (*childList[-1], spec.text)
    except:
        # no children to explore or error occurred
        pass
    return childList


# ===============================================================================
# MyNetworkItem-
# ===============================================================================
class MyNetworkItem(PyQt6.QtWidgets.QTreeWidgetItem):
    """
    This class is used to create a playlist widget item for the video player.
    """

# |-----------------------------------------------------------------------------|
# Constructor :-
# |-----------------------------------------------------------------------------|
    def __init__(self, displayText, browse, itemID, address=None, parent=None):
        """
        This constructor is used to initialize the playlist widget.
        """
        super(MyNetworkItem, self).__init__(parent)
        self.setText(0, displayText)
        self.displayText = displayText
        self.browse = browse
        self.itemID = itemID
        self.address = address
# |--------------------------End of Constructor---------------------------------|


# ===============================================================================
# MyNetworkTree-
# ===============================================================================
class MyNetworkTree(PyQt6.QtWidgets.QMainWindow):
    """
    This class is used to create a network view widget for the video player.
    """
    playMediaFile = pyqtSignal(str)
# |-----------------------------------------------------------------------------|
# Constructor :-
# |-----------------------------------------------------------------------------|

    def __init__(self, *args, **kwargs):
        """
        This constructor is used to initialize the playlist widget.
        """
        super(MyNetworkTree, self).__init__(*args, **kwargs)
        self.mainWidget = PyQt6.QtWidgets.QTreeWidget(self)
        self.mainWidget.setHeaderLabel("Devices")
        self.setCentralWidget(self.mainWidget)
        self.mainWidget.itemActivated.connect(self.__itemClicked)
# |--------------------------End of Constructor---------------------------------|

# |-----------------------------------------------------------------------------|
# addPLItem :-
# |-----------------------------------------------------------------------------|
    def addParentItem(self, deviceName, browse=None):
        """
        Adds a top-level UPnP device to the network tree.

        Args:
            deviceName (str): Friendly name of the UPnP device
            browse (callable): The Browse action from ContentDirectory service
        """
        # Create a new network item representing the device
        it = MyNetworkItem(deviceName, browse, '0', parent=self.mainWidget)
        # Add it as a top-level item in the tree
        self.mainWidget.addTopLevelItem(it)
# |--------------------------End of addPLItem-----------------------------------|

    def addChildItem(self, displayName, browse, itemID, address=None, parent=None):
        """
        Adds a child item (folder or media file) to a parent in the tree.

        Args:
            displayName (str): Display name for the item
            browse (callable): Browse action for accessing item's children
            itemID (str): UPnP object ID for the item
            address (str): URL/URI for playable media (optional)
            parent (MyNetworkItem): Parent tree item
        """
        # Create a network item with the provided information
        it = MyNetworkItem(displayName, browse, itemID,
                           address=address, parent=parent)
        # Add it as a child to the parent item
        parent.addChild(it)

    def getParent(self, it, text=[]):
        """
        Recursively builds the full path of an item in the tree.

        Args:
            it: Current tree item
            text (list): Accumulator for the path components

        Returns:
            list: Full path from root to current item as list of names
        """
        # Check if item has displayText attribute (is a network item)
        if hasattr(it, "displayText"):
            # Add this item's name to the beginning of the path
            text.insert(0, it.displayText)
            # Recursively get parent's path
            return self.getParent(it.parent(), text=text)
        else:
            # Reached root (no parent), return the complete path
            return text

    def __itemClicked(self, it):
        """
        Handles tree item activation (double-click or Enter key).

        When a container is clicked:
        - Queries device for children
        - Adds them as child items to the tree

        When a media file is clicked:
        - Emits playMediaFile signal with the file URL

        Args:
            it (MyNetworkItem): The activated tree item
        """
        # print("-----------------------------------------------")
        # print(it.displayText)
        # print("-----------------------------------------------")
        # Query device for children of this item
        outs = browseChildren(it.itemID, it.browse)

        # If item hasn't been expanded yet (no children in tree)
        if it.childCount() == 0:
            # Add all discovered children to this item
            for out in outs:
                if len(out) == 2:
                    # Folder or container (no resource URL)
                    self.addChildItem(out[1], it.browse, out[0], parent=it)
                if len(out) == 3:
                    # Media file with resource URL
                    self.addChildItem(out[1], it.browse,
                                      out[0], address=out[2], parent=it)

            # If no children found, treat as playable media
            if not outs:
                l = self.getParent(it, [])
                print("file:{} address:".format("/".join(l), it.address))
                # Emit signal to play this media file
                self.playMediaFile.emit(it.address)

    def closeEvent(self, *args, **kwargs):
        """
        Handles the close event for the network browser window.

        Clears the tree widget to free resources before closing.
        """
        # Clear all items from the tree
        self.mainWidget.clear()
        # Call parent close event
        super().closeEvent(*args, **kwargs)
