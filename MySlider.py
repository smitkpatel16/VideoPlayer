import PyQt6.QtCore
from PyQt6.QtWidgets import QSlider


# derive QSlilder class to enable hovering to show timestamp
class MySlider(QSlider):
    """
    This class is used to derive the QSlider class to enable hovering to show timestamp.
    """
# |-----------------------------------------------------------------------------|
# Constructor :-
# |-----------------------------------------------------------------------------|

    def __init__(self, *args, **kwargs):
        """
        This constructor is used to initialize the MySlider class.
        """
        super(MySlider, self).__init__(*args, **kwargs)
        self.setMouseTracking(True)
        self.setOrientation(PyQt6.QtCore.Qt.Orientation.Horizontal)
        self.setToolTip("0:00")
# |--------------------------End of Constructor--------------------------------|
