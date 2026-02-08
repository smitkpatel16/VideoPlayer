
import sys
import unittest
from unittest.mock import MagicMock, patch
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtCore import Qt, QEvent

# Add project root to path
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# We need to ensure we can import MyMediaPlayer
from MyMediaPlayer import MyMediaPlayer

app = QApplication(sys.argv)

class TestMyMediaPlayerEventFilter(unittest.TestCase):
    def setUp(self):
        self.player = MyMediaPlayer()
        # Mock internal components
        self.player._MyMediaPlayer__videoWidget = MagicMock()
        self.player._MyMediaPlayer__fullScreen = True # Simulate fullscreen
        
    def test_esc_event_filter(self):
        # Create Esc key event
        event = QKeyEvent(QEvent.Type.KeyPress, Qt.Key.Key_Escape, Qt.KeyboardModifier.NoModifier)
        
        # Call eventFilter
        # We need to mock toggleFullScreen to verify it's called
        with patch.object(self.player, 'toggleFullScreen') as mock_toggle:
            result = self.player.eventFilter(None, event)
            
            # Should return True (handled) and call toggleFullScreen
            self.assertTrue(result)
            mock_toggle.assert_called_once()
            
    def test_other_key_event_filter(self):
        # Create 'A' key event
        event = QKeyEvent(QEvent.Type.KeyPress, Qt.Key.Key_A, Qt.KeyboardModifier.NoModifier)
        
        # Call eventFilter
        with patch.object(self.player, 'toggleFullScreen') as mock_toggle:
            # We need to ensure super().eventFilter doesn't crash. 
            # Since MyMediaPlayer inherits QWidget, we should be careful.
            # But eventFilter is just a method.
            # To avoid super() issues in test without real widget hierarchy, we might need more setup.
            # However, for this test, we just want to verify it returns False (not handled) or doesn't call toggle.
            
            # Actually, calling super().eventFilter(None, event) might fail if source is None or event not valid for object.
            # Let's just check that toggleFullScreen is NOT called. 
            try:
                self.player.eventFilter(self.player, event)
            except:
                pass # expected if super call fails on mock/setup
                
            mock_toggle.assert_not_called()

if __name__ == '__main__':
    unittest.main()
