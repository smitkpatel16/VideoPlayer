import PyQt6.QtWidgets


# ===============================================================================
# MyCentralWidget-
# ===============================================================================
class MyCentralWidget(PyQt6.QtWidgets.QWidget):
    """
    This class is used to create a central widget for the video player.
    """
# |-----------------------------------------------------------------------------|
# Constructor :-
# |-----------------------------------------------------------------------------|

    def __init__(self, *args, **kwargs):
        """
        This constructor is used to initialize the central widget.
        """
        super(MyCentralWidget, self).__init__(*args, **kwargs)
        self.mainLayout = PyQt6.QtWidgets.QVBoxLayout()
        self.setLayout(self.mainLayout)
        self.installEventFilter(self)
# |--------------------------End of Constructor---------------------------------|

    def eventFilter(self, obj, event):
        if type(event) == PyQt6.QtCore.QChildEvent:
            return super().eventFilter(obj, event)
        if event.type() == PyQt6.QtCore.QEvent.Type.Paint:
            self.adjustWidgetSizes()
        return super().eventFilter(obj, event)
# |-----------------------------------------------------------------------------|
# addWidget :-
# |-----------------------------------------------------------------------------|

    def addWidget(self, widget):
        """
        This method is used to add a widget to the main layout.
        """
        self.mainLayout.addWidget(widget)
# |--------------------------End of addWidget-----------------------------------|

# |-----------------------------------------------------------------------------|
# adjustWidgetSizes :-
# |-----------------------------------------------------------------------------|
    def adjustWidgetSizes(self):
        """
        This method is used to adjust the size of the widgets in the main layout.
        """
        if self.mainLayout.itemAt(0):
            w = self.mainLayout.itemAt(0).widget()
            w.setMinimumWidth(int(self.width()*0.9))
            w.setMinimumHeight(self.height() - 250)
        if self.mainLayout.itemAt(1):
            w = self.mainLayout.itemAt(1).widget()
            w.setMinimumWidth(int(self.width()*0.8))
            w.setMinimumHeight(120)
        if self.mainLayout.itemAt(2):
            w = self.mainLayout.itemAt(2).widget()
            w.setMinimumWidth(int(self.width()*0.9))
            w.setMinimumHeight(100)
# |--------------------------End of adjustWidgetSizes---------------------------|
