"""
processTools.py - Video/Audio Processing Utilities

This module provides utilities for video and audio file processing including:
- Frame extraction for timeline thumbnails
- Preview frame extraction at specific timestamps
- Duration calculation for media files
- Timeline navigation line graphics item

Key Classes:
- ExtractImages: Multi-threaded frame extraction from videos
- PreviewPosition: Single frame extraction for timeline previews
- SelectionLine: Graphics line item for timeline playhead

Key Functions:
- extractAudio(): Extract audio from video file
- checkDuration(): Get video duration, frame count, and frame rate
- checkDurationAudio(): Get audio file duration
- browseChildren(): (Defined in MyNetworkTree)

Processing Libraries:
- cv2 (OpenCV): Video file reading and frame extraction
- ffmpeg: Audio extraction
- PyQt6: GUI components and signals

Note: This module handles heavy I/O operations and is often used with threading
to prevent UI blocking during frame extraction.
"""

from email.mime import audio
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtCore import QObject
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage
from PyQt6.QtWidgets import QGraphicsLineItem
from PyQt6.QtGui import QPen
from PyQt6.QtWidgets import QApplication
import cv2
import math
# import win32com.client
import os.path
import ffmpeg
import logging
logger = logging.getLogger(__name__)

# sh = win32com.client.gencache.EnsureDispatch('Shell.Application', 0)

# ===============================================================================
# ProcessTools- A collection of methods for processing audio/video files
# ===============================================================================


class ExtractImages(QObject):
    """
    Multi-threaded frame extractor for generating timeline thumbnails.

    This class is designed to be moved to a QThread for non-blocking operation.
    It extracts equally-spaced frames from a video file and emits them as
    QImage objects for display in a thumbnail strip.

    Signals:
    - reelImage(QImage, int): Emitted when a frame is extracted
    - finished(): Emitted when extraction for this thread is complete
    - over(int): Emitted when thread finishes with thread index

    Attributes:
    - fPath: Path to video file
    - split: Number of parallel threads for extraction
    - pos: This thread's index (0 to split-1)
    - capture: OpenCV VideoCapture object
    - frameCount: Total frames in video
    - frameInterval: Spacing between extracted frames
    """

    reelImage = pyqtSignal(QImage, int)  # Signal: extracted frame and position
    finished = pyqtSignal()  # Signal: thread finished extracting
    over = pyqtSignal(int)  # Signal: thread finished with position index

    def __init__(self, fPath, split, pos):
        """
        Initialize frame extractor for a video file.

        Args:
            fPath (str): Path to video file
            split (int): Number of parallel extraction threads
            pos (int): This thread's index (0 to split-1)
        """
        super().__init__()
        self.fPath = fPath
        self.split = split
        self.pos = pos
        self._readVideo = False

    def baselineRead(self):
        """
        Initializes video capture and calculates frame extraction parameters.

        Reads video metadata:
        - Total frame count
        - Frame width and height (for aspect ratio)
        - Frame interval for equally-spaced extraction
        """
        # Open video file with OpenCV
        self.capture = cv2.VideoCapture(self.fPath)
        # Get total number of frames in video
        self.frameCount = int(self.capture.get(cv2.CAP_PROP_FRAME_COUNT))
        # Get video resolution
        fW = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        fH = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        # Calculate aspect ratio for thumbnail resizing
        self.r = fW / fH
        # Calculate interval between frames to extract ~100 thumbnails
        self.frameInterval = math.ceil(self.frameCount / 100)
        # Mark that video info has been read
        self._readVideo = True

    def _transmitFrame(self, frame, pos):
        """
        Converts an OpenCV frame to QImage and emits it.

        Args:
            frame (numpy.ndarray): OpenCV frame in BGR888 format
            pos (int): Frame position in sequence

        Resizes frame to thumbnail size while maintaining aspect ratio
        and emits it through the reelImage signal.
        """
        # Get frame dimensions
        height, width, channel = frame.shape
        # Calculate bytes per line for QImage (3 channels * width)
        bytesPerLine = 3 * width
        # Convert OpenCV BGR frame to QImage
        qImg = QImage(frame.data, width, height,
                      bytesPerLine, QImage.Format.Format_BGR888)
        # Scale to thumbnail size (80px height, maintain aspect ratio)
        self.reelImage.emit(qImg.scaled(
            int(self.r * 80), 80), pos)

    def run(self):
        """
        Extracts frames from the video at equally-spaced intervals.

        This method is called when the thread starts. It:
        1. Reads video metadata if not already done
        2. Extracts frames starting at this thread's designated position
        3. Extracts every (frameInterval * split) frames to distribute work
        4. Emits each frame and signals completion

        Each thread extracts a different subset of frames for parallel processing.
        """
        # Initialize video reading if not done
        if not self._readVideo:
            self.baselineRead()
        success, image = self.capture.read()

        # Extract frames starting at this thread's position
        # Stride by (frameInterval * split) to distribute work across threads
        for i in range(self.pos*self.frameInterval, self.frameCount, self.frameInterval*self.split):
            # Set the frame position
            self.capture.set(cv2.CAP_PROP_POS_FRAMES, i)
            # Read the frame at this position
            success, image = self.capture.read()
            if not success:
                # Stop if can't read frame
                break
            # Send the frame and its sequential position
            self._transmitFrame(image, math.floor(i/self.frameInterval))

        # Signal that this thread finished extracting
        self.finished.emit()
        # Signal which thread finished
        self.over.emit(self.pos)


class PreviewPosition(object):
    """
    Extracts single frames at specific timestamps for timeline preview.

    Used for hovering over timeline to show frame at that position without
    requiring pre-extracted thumbnails. Faster than ExtractImages for single frames.

    Attributes:
    - fPath: Path to video file
    - capture: OpenCV VideoCapture object
    - frameCount: Total frames in video
    - r: Aspect ratio (width/height)
    """

    def __init__(self, fPath):
        """
        Initialize preview extractor for a video file.

        Args:
            fPath (str): Path to video file
        """
        self.fPath = fPath
        # Open video file
        self.capture = cv2.VideoCapture(self.fPath)
        # Get total frames
        self.frameCount = int(self.capture.get(cv2.CAP_PROP_FRAME_COUNT))
        # Get video dimensions
        fW = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        fH = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        # Calculate aspect ratio
        self.r = fW / fH

    def extract(self, positionImage):
        """
        Extracts and returns a frame at a specific frame number.

        Args:
            positionImage (int): Frame number to extract

        Returns:
            QImage: Scaled thumbnail image, or None if extraction failed

        Returns a thumbnail sized image (80px height) maintaining aspect ratio.
        """
        # Seek to the specified frame
        self.capture.set(cv2.CAP_PROP_POS_FRAMES, positionImage)
        # Read the frame
        success, image = self.capture.read()
        if success:
            # Get frame dimensions
            height, width, channel = image.shape
            # Calculate bytes per line
            bytesPerLine = 3 * width
            # Convert OpenCV BGR to QImage
            qImg = QImage(image.data, width, height,
                          bytesPerLine, QImage.Format.Format_BGR888)
            # Scale to thumbnail size
            return qImg.scaled(int(self.r * 80), 80)
        return None


def extractAudio(filePath):
    """
    Extracts audio stream from a video file and saves as WAV.

    Args:
        filePath (str): Path to the video file

    Returns:
        str: Path to the output WAV audio file

    Note: Requires ffmpeg to be installed and available in PATH.
    Note: XXX - would need to work on streaming or directory permissions here
    """
    # Create ffmpeg input from video file
    input = ffmpeg.input(filePath)
    # Split path and filename
    folder, fileName = os.path.split(filePath)
    # Extract filename without extension
    name = fileName.split(".")[0]
    # Create output audio path (same folder, _audio.wav suffix)
    audioPath = folder+"/" + name+"_audio" + ".wav"
    # Create ffmpeg output for audio stream
    output = ffmpeg.output(input.audio, audioPath)
    # Run the conversion, overwriting if file exists
    output.run(overwrite_output=True)
    return audioPath


def checkDuration(filePath):
    """
    Gets the duration and frame information from a video file.

    Args:
        filePath (str): Path to the video file

    Returns:
        tuple: (duration_seconds, frame_count, frame_rate)
               - duration_seconds (float): Video duration in seconds
               - frame_count (int): Total number of frames
               - frame_rate (float): Frames per second

    Uses OpenCV to read video metadata without decompressing the entire file.
    """
    # Open video with OpenCV
    capture = cv2.VideoCapture(filePath)
    # Get total frame count
    frameCount = capture.get(cv2.CAP_PROP_FRAME_COUNT)
    # Get frames per second
    frameRate = capture.get(cv2.CAP_PROP_FPS)
    # Calculate duration
    dur = frameCount/frameRate
    return (round(dur, 3), frameCount, frameRate)

# find duration of the audio file using wave module


def checkDurationAudio(filePath):
    """
    Gets the duration of an audio file.

    Args:
        filePath (str): Path to the audio file (WAV format)

    Returns:
        float: Duration in seconds, rounded to 3 decimal places

    Uses the wave module to read WAV file metadata.
    """
    import wave
    # Open audio file
    raw = wave.open(filePath)
    # Get sample rate (frames per second)
    f_rate = raw.getframerate()
    # Get total number of frames
    f_length = raw.getnframes() / f_rate
    return round(f_length, 3)


# ===============================================================================
# SelectionLine- Inherited QGraphicsLineItem for selection movement
# ===============================================================================
class SelectionLine(QGraphicsLineItem):
    """
    A graphics line item representing a draggable timeline position indicator.

    This class extends QGraphicsLineItem to create an interactive line that:
    - Can be dragged horizontally (restricted to horizontal movement only)
    - Shows a resize cursor on hover
    - Emits signals when position changes

    Signals:
    - updateHighlight(): Emitted when line position changes

    Visual properties:
    - Color: Red line with 3px width
    - Length: 80px vertical line (height of timeline)
    """

    updateHighlight = pyqtSignal()

    def __init__(self, *args, **kwargs):
        """
        Initializes the selection line with red color and drag properties.
        """
        super().__init__(*args, **kwargs)
        # Set line color to red with 3px width
        self.setPen(QPen(Qt.GlobalColor.red, 3))
        # Enable position change notifications and scene position tracking
        self.setFlags(
            self.GraphicsItemFlag.ItemSendsScenePositionChanges)
        # Enable hover events for cursor changes
        self.setAcceptHoverEvents(True)

    def itemChange(self, change, value):
        """
        Restricts movement to horizontal only (prevents vertical dragging).

        Args:
            change: The type of change (position, bounds, etc.)
            value: The new value for the change

        Returns:
            The modified value with Y coordinate reset to 0
        """
        if change == self.GraphicsItemChange.ItemPositionChange:
            # restrict vertical movement
            # Force Y position to 0 so line only moves horizontally
            value.setY(0)
        return super().itemChange(change, value)

    def hoverEnterEvent(self, event):
        """
        Shows resize cursor when mouse hovers over the line.

        Args:
            event: The hover event
        """
        # Change cursor to horizontal resize (left-right arrow)
        QApplication.setOverrideCursor(Qt.CursorShape.SizeHorCursor)
        return super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        """
        Restores normal cursor when mouse leaves the line.

        Args:
            event: The hover event
        """
        # Restore default cursor
        QApplication.restoreOverrideCursor()
        return super().hoverLeaveEvent(event)
