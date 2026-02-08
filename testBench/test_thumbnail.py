
import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add project root to path
sys.path.append("..")
import processTools

class TestThumbnail(unittest.TestCase):
    @patch('cv2.VideoCapture')
    def test_preview_position_extract(self, mock_capture):
        # Setup mock
        instance = mock_capture.return_value
        mock_image = MagicMock()
        mock_image.shape = (100, 100, 3)
        mock_image.data = b'0'*100*100*3
        instance.read.return_value = (True, mock_image) # success, image
        instance.get.return_value = 100 # frame count
        
        # Test constructor
        pp = processTools.PreviewPosition("dummy.mp4")
        self.assertIsNotNone(pp)
        
        # Test extract
        qimg = pp.extract(50)
        instance.set.assert_called_with(processTools.cv2.CAP_PROP_POS_FRAMES, 50)
        self.assertIsNotNone(qimg)

if __name__ == '__main__':
    unittest.main()
