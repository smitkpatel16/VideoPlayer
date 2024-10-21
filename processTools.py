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
    reelImage = pyqtSignal(QImage, int)
    finished = pyqtSignal()
    over = pyqtSignal(int)
    # override constructor

    def __init__(self, fPath, split, pos):
        super().__init__()
        self.fPath = fPath
        self.split = split
        self.pos = pos
        self._readVideo = False

    def baselineRead(self):
        self.capture = cv2.VideoCapture(self.fPath)
        # get equally spaced frames from the video
        self.frameCount = int(self.capture.get(cv2.CAP_PROP_FRAME_COUNT))
        fW = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        fH = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.r = fW / fH
        self.frameInterval = math.ceil(self.frameCount / 100)
        self._readVideo = True

    def _transmitFrame(self, frame, pos):
        height, width, channel = frame.shape
        bytesPerLine = 3 * width
        qImg = QImage(frame.data, width, height,
                      bytesPerLine, QImage.Format.Format_BGR888)
        self.reelImage.emit(qImg.scaled(
            int(self.r * 80), 80), pos)

    def run(self):
        """
        Extracts images from a video file and saves them to a folder.
        :param filePath: The path to the video file.
        :param outputPath: The path to the folder where the images will be saved.
        :param imageType: The type of image to extract.
        :return: imageArray
        """
        if not self._readVideo:
            self.baselineRead()
        success, image = self.capture.read()
        for i in range(self.pos*self.frameInterval, self.frameCount, self.frameInterval*self.split):
            # print(f"Thread: {self.pos} Frame: {i} Location: {
            #       math.floor(i/self.frameInterval)}")
            self.capture.set(cv2.CAP_PROP_POS_FRAMES, i)
            success, image = self.capture.read()
            if not success:
                break
            self._transmitFrame(image, math.floor(i/self.frameInterval))
        self.finished.emit()
        self.over.emit(self.pos)


def extractAudio(filePath):
    # XXX: would need to work on streaming or directory permissions here
    input = ffmpeg.input(filePath)
    folder, fileName = os.path.split(filePath)
    name = fileName.split(".")[0]
    audioPath = folder+"/" + name+"_audio" + ".wav"
    output = ffmpeg.output(input.audio, audioPath)
    output.run(overwrite_output=True)
    return audioPath


def checkDuration(filePath):
    """
    Checks the duration of a video file.
    :param filePath: The path to the video file.
    :return: duration
    """
    # get the meta info for the selected video
    # file = Path(filePath)
    # ns = sh.NameSpace(str(file.parent))
    # item = ns.ParseName(str(file.name))
    # colnum = 0
    # columns = []
    # while True:
    #     colname = ns.GetDetailsOf(None, colnum)
    #     if not colname:
    #         break
    #     columns.append(colname)
    #     colnum += 1
    # metaData = {}

    # for colnum in range(len(columns)):
    #     colval = ns.GetDetailsOf(item, colnum)
    #     if colval:
    #         metaData[columns[colnum].lower()] = colval
    # # length or duration of the video
    # duration = metaData.get('length') or metaData.get('duration')
    # return duration
    capture = cv2.VideoCapture(filePath)
    frameCount = capture.get(cv2.CAP_PROP_FRAME_COUNT)
    frameRate = capture.get(cv2.CAP_PROP_FPS)
    dur = frameCount/frameRate
    return round(dur, 3)

# find duration of the audio file using wave module


def checkDurationAudio(filePath):
    """
    Checks the duration of a audio file.
    :param filePath: The path to the audio file.
    :return: duration
    """
    import wave
    raw = wave.open(filePath)
    f_rate = raw.getframerate()
    f_length = raw.getnframes() / f_rate
    return round(f_length, 3)


# ===============================================================================
# SelectionLine- Inherited QGraphicsLineItem for selection movement
# ===============================================================================
class SelectionLine(QGraphicsLineItem):
    updateHighlight = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setPen(QPen(Qt.GlobalColor.red, 3))
        self.setFlags(
            self.GraphicsItemFlag.ItemSendsScenePositionChanges)
        self.setAcceptHoverEvents(True)

    def itemChange(self, change, value):
        if change == self.GraphicsItemChange.ItemPositionChange:
            # restrict vertical movement
            value.setY(0)
        return super().itemChange(change, value)

    def hoverEnterEvent(self, event):
        QApplication.setOverrideCursor(Qt.CursorShape.SizeHorCursor)
        return super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        QApplication.restoreOverrideCursor()
        return super().hoverLeaveEvent(event)
