# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtWidgets import QApplication, QWidget, QFileDialog, QLabel
from PySide6.QtGui import QPixmap, QImage, QPainter, QColor, QPen
# from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtCore import QTimer, QRect, QPoint
from copy import deepcopy
import cv2

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_MainWindow

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Instance Attributes
        self.fileName = None
        self.currentFrame = None
        self.grayScale = False
        previewPen = QPen(QColor("green"))
        previewPen.setWidth(20)
        self.previewPen = previewPen

        self.cropWindow = QRect(0, 0, self.ui.videoFrame.width(), self.ui.videoFrame.height())

        self.ui.loadVideo.clicked.connect(self.openVideo)

        self.ui.convertGrayScale.clicked.connect(self.convertToGrayScale)

        # self.mediaPlayer = QMediaPlayer(None)

        self.refreshTimer = QTimer(self)
        self.refreshTimer.timeout.connect(self.update)

        self.playPauseButton = self.ui.playPause

        self.ui.playPause.clicked.connect(self.playPause)

        self.previewWindow = self.ui.previewWindow


    def playPause(self):
        if self.fileName is None:
            return

        if self.playPauseButton.text() == "Play":
            self.refreshTimer.start()
            self.playPauseButton.setText("Pause")
        else:
            self.refreshTimer.stop()
            self.playPauseButton.setText("Play")

    def openVideo(self):
        self.fileName, _ = QFileDialog.getOpenFileName(self, "Open Video", "", "Video Files (*.mp4 *.avi *.mkv)")
        self.fileName = "D:\\point detection algorithm implementation-python\\750.mp4"
        if self.fileName != '':
            self.video = cv2.VideoCapture(self.fileName)
            self.playPauseButton.setText("Pause")
            self.refreshTimer.start(1000)

    def paintEvent(self, paintRegion):
        if not self.refreshTimer.isActive():
            return

        ret, frame = self.video.read()
        if ret:
            # set image to actual Windows
            # viewPainter = QPainter()

            height, width, channel = frame.shape
            pixmap = QPixmap(QImage(frame.data, width, height, 3 * width, QImage.Format_RGB888))
            # retain a copy just in case, hope original isn't modified
            self.currentFrame = pixmap

            # viewPainter.begin(self.ui.videoFrame)
            # viewPainter.drawPixmap(QPoint(0, 0), pixmap)
            # viewPainter.end()
            self.ui.videoFrame.setPixmap(pixmap.copy(0, 0, self.ui.videoFrame.width(), self.ui.videoFrame.height()))

            # resize drawn image and show
            # if pixmap.height() > self.previewWindow.height() or pixmap.width() > self.previewWindow.width():
            #     scaledPixmap = pixmap.scaled(self.previewWindow.width(), self.previewWindow.height())
            #     self.previewWindow.setPixmap(scaledPixmap)

        # draw a green rectangle on a copy of image shown to preview image
        # make a copy of current frame
        if self.currentFrame is not None:
            copyCurrentFrame = self.currentFrame.copy(0, 0, self.currentFrame.width(), self.currentFrame.height())
            previewPainter = QPainter()
            previewPainter.begin(copyCurrentFrame)
            previewPainter.setPen(self.previewPen)
            previewPainter.drawRect(self.cropWindow)
            # previewPainter.drawRect(0, 0, 200, 200)
            previewPainter.end()

            copyCurrentFrame = copyCurrentFrame.scaled(self.previewWindow.width(), self.previewWindow.height())
            self.previewWindow.setPixmap(copyCurrentFrame)
        return

    def updateFrame(self):
        pass

            # print(frame) print(frame.shape)
            # height, width, channel = frame.shape
            # self.currentFrameNonGrayScale = frame
            # if self.grayScale:
            #     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # pixmap = QPixmap(QImage(frame.data, width, height, width, QImage.Format_Grayscale8))
            # if pixmap.height() > self.ui.videoFrame.height() or pixmap.width() > self.ui.videoFrame.width():
            #     pixmap = pixmap.scaled(self.ui.videoFrame.width(), self.ui.videoFrame.height())

            # self.currentFrame = pixmap
            # self.ui.videoFrame.setPixmap(pixmap)


    def convertToGrayScale(self):
        if not self.grayScale:
            self.grayScale = True
        else:
            return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
