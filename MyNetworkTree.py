import PyQt6.QtWidgets
from lxml import etree
from PyQt6.QtCore import pyqtSignal


def browseChildren(parentID, browse):
    childList = []
    try:
        result = browse(
            ObjectID=parentID,  # Root directory
            BrowseFlag='BrowseDirectChildren',
            Filter='*',
            StartingIndex=0,
            RequestedCount=500,
            SortCriteria=''
        )
        print(result["Result"])
        # Parse the XML content
        root = etree.fromstring(result["Result"])
        for child in root.iterchildren():
            for spec in child.iterchildren():
                if "title" in spec.tag:
                    childList.append((child.values()[0], spec.text))
    except:
        # no children to explore
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
    def __init__(self, displayText, browse, itemID, parent=None):
        """
        This constructor is used to initialize the playlist widget.
        """
        super(MyNetworkItem, self).__init__(parent)
        self.setText(0, displayText)
        self.displayText = displayText
        self.browse = browse
        self.itemID = itemID
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
        it = MyNetworkItem(deviceName, browse, '0', parent=self.mainWidget)
        self.mainWidget.addTopLevelItem(it)
# |--------------------------End of addPLItem-----------------------------------|

    def addChildItem(self, displayName, browse, itemID, parent=None):
        it = MyNetworkItem(displayName, browse, itemID, parent=parent)
        parent.addChild(it)

    def getParent(self, it, text=[]):
        if hasattr(it, "displayText"):
            text.insert(0, it.displayText)
            return self.getParent(it.parent(), text=text)
        else:
            return text

    def __itemClicked(self, it):
        print("-----------------------------------------------")
        print(it.displayText)
        print("-----------------------------------------------")
        outs = browseChildren(it.itemID, it.browse)
        if it.childCount() == 0:
            for out in outs:
                self.addChildItem(out[1], it.browse, out[0], it)
            if not outs:
                l = self.getParent(it, [])
                print("file:///{}".format("/".join(l)))
                self.playMediaFile.emit("file:///{}".format("/".join(l)))

    def closeEvent(self, *args, **kwargs):
        self.mainWidget.clear()
        super().closeEvent(*args, **kwargs)
