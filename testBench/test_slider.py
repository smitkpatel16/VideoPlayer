
import unittest
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QPoint
import sys
import time
from unittest.mock import MagicMock

# Add project root to path
sys.path.append("..") 
from MySlider import MySlider

app = QApplication(sys.argv)

class TestMySlider(unittest.TestCase):
    def setUp(self):
        self.slider = MySlider()
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.duration = 100 # seconds
        self.slider.resize(100, 20)
        # Verify initial state
        self.assertFalse(self.slider._MySlider__inside)

    def test_enter_leave_events(self):
        # Mock signal slots
        enter_mock = MagicMock()
        exit_mock = MagicMock()
        self.slider.enterPreview.connect(enter_mock)
        self.slider.exitPreview.connect(exit_mock)
        
        # Simulate enter
        self.slider.enterEvent(None)
        self.assertTrue(self.slider._MySlider__inside)
        enter_mock.assert_called_once()
        
        # Simulate leave
        self.slider.leaveEvent(None)
        self.assertFalse(self.slider._MySlider__inside)
        exit_mock.assert_called_once()
        
    def test_mouse_move_signal(self):
        show_mock = MagicMock()
        self.slider.showPreview.connect(show_mock)
        
        # Enter first
        self.slider.enterEvent(None)
        
        # Simulate move
        self.slider._MySlider__inside = True
        # Force sent time update by waiting slightly longer than debounce
        time.sleep(0.06)
        
        # Create a real QMouseEvent
        from PyQt6.QtGui import QMouseEvent
        from PyQt6.QtCore import QEvent, Qt, QPointF
        
        # QMouseEvent(type, localPos, globalPos, button, buttons, modifiers)
        # Note: globalPos is usually calculated by Qt, but we can pass something reasonable
        local_pos = QPointF(50.0, 10.0)
        global_pos = QPointF(50.0, 10.0) # For test, doesn't matter much as mapToGlobal uses widget position
        
        event = QMouseEvent(
            QEvent.Type.MouseMove,
            local_pos,
            global_pos,
            Qt.MouseButton.NoButton,
            Qt.MouseButton.NoButton,
            Qt.KeyboardModifier.NoModifier
        )
        
        # Call mouseMove
        # We need to suppress strict type checking for mapToGlobal or ensure environment is set up
        # mapToGlobal requires the widget to be part of a hierarchy or at least initialized properly on a screen
        # Since we just want to test signal, and mapToGlobal might return (0,0) + pos if not shown, that's fine.
        
        self.slider.mouseMoveEvent(event)
        
        # Assert signal emitted
        show_mock.assert_called()
        args = show_mock.call_args[0][0]
        # Check if coordinates are global (since mapToGlobal is called)
        # We can't really check exact global coords w/o a window system active, 
        # but we can check the time logic
        expected_time = 50 * 1000 # 50s * 1000ms
        self.assertAlmostEqual(args[2], expected_time, delta=100)

if __name__ == '__main__':
    unittest.main()
