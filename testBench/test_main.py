
import sys
import unittest
from unittest.mock import MagicMock, patch
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtCore import Qt, QEvent

# Add project root to path
sys.path.append("..") 
# We need to ensure we can import Main
# Since Main.py is in parent, we might need to modify sys.path
# already done above.

# Mocking modules that might cause side effects if imported or instantiated
with patch('MyPlaylist.MyPlaylist'), \
     patch('MyNetworkTree.MyNetworkTree'), \
     patch('MyPreview.MyPreview'):
    from Main import MyVideoPlayer

app = QApplication(sys.argv)

class TestMyVideoPlayer(unittest.TestCase):
    def setUp(self):
        self.player = MyVideoPlayer()
        # Mock internal components to isolate tests
        self.player.mediaPlayer = MagicMock()
        self.player.mediaControls = MagicMock()
        
    def test_toggle_fullscreen(self):
        # Call toggle
        self.player.toggleFullScreen()
        # Verify delegation
        self.player.mediaPlayer.toggleFullScreen.assert_called_once()
        
    def test_shortcuts(self):
        # Check 'F' key
        event = QKeyEvent(QEvent.Type.KeyPress, Qt.Key.Key_F, Qt.KeyboardModifier.NoModifier)
        self.player.keyPressEvent(event)
        self.player.mediaPlayer.toggleFullScreen.assert_called()
        self.player.mediaPlayer.toggleFullScreen.reset_mock()
        
        # Check 'Esc' key
        self.player.mediaPlayer.isFullScreen.return_value = True
        event = QKeyEvent(QEvent.Type.KeyPress, Qt.Key.Key_Escape, Qt.KeyboardModifier.NoModifier)
        self.player.keyPressEvent(event)
        self.player.mediaPlayer.toggleFullScreen.assert_called()
        
        # Check 'Space' key
        event = QKeyEvent(QEvent.Type.KeyPress, Qt.Key.Key_Space, Qt.KeyboardModifier.NoModifier)
        self.player.keyPressEvent(event)
        self.player.mediaControls.playButton.click.assert_called()

if __name__ == '__main__':
    unittest.main()
