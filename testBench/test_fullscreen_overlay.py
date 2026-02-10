
import sys
import os
import unittest
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Main import MyVideoPlayer

app = QApplication(sys.argv)

class TestFullscreenOverlay(unittest.TestCase):
    def setUp(self):
        self.player = MyVideoPlayer()
        
    def tearDown(self):
        self.player.close()

    def test_toggle_fullscreen_reparenting(self):
        # Initial state: controls should be in mainWidget
        self.assertEqual(self.player.mediaControls.parent(), self.player.mainWidget)
        
        # Toggle fullscreen ON
        self.player.toggleFullScreen()
        
        # Check if controls are reparented to videoWidget
        self.assertEqual(self.player.mediaControls.parent(), self.player.mediaPlayer.videoWidget())
        
        # Check window flags and attributes
        self.assertEqual(self.player.mediaControls.windowFlags() & Qt.WindowType.FramelessWindowHint, Qt.WindowType.FramelessWindowHint)
        self.assertTrue(self.player.mediaControls.testAttribute(Qt.WidgetAttribute.WA_TranslucentBackground))
        
        # Check stylesheet (simplified check)
        self.assertIn("rgba(0, 0, 0, 128)", self.player.mediaControls.styleSheet())
        
        # Toggle fullscreen OFF
        self.player.toggleFullScreen()
        
        # Check if controls are restored to mainWidget
        self.assertEqual(self.player.mediaControls.parent(), self.player.mainWidget)
        self.assertEqual(self.player.mediaControls.windowFlags() & Qt.WindowType.Widget, Qt.WindowType.Widget)

    def test_controls_positioning(self):
        # Toggle fullscreen ON
        self.player.toggleFullScreen()
        
        # Force an update of position (simulate resize or initial show)
        self.player.updateControlsPosition()
        
        video_geo = self.player.mediaPlayer.videoWidget().geometry()
        controls_geo = self.player.mediaControls.geometry()
        
        # Check width is 80%
        expected_width = int(video_geo.width() * 0.8)
        self.assertEqual(controls_geo.width(), expected_width)
        
        # Check centered horizontally
        expected_x = (video_geo.width() - expected_width) // 2
        self.assertEqual(controls_geo.x(), expected_x)
        
        # Check positioned at bottom
        # expected_y = video_geo.height() - controls_height - 20
        # Just check it is near bottom
        self.assertTrue(controls_geo.y() > video_geo.height() * 0.7)

if __name__ == '__main__':
    unittest.main()
