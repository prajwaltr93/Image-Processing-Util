# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtWidgets import QApplication, QWidget, QFileDialog, QLabel
from PySide6.QtGui import QPixmap, QImage, QPainter, QColor, QPen
from PySide6.QtCore import QTimer, QRect, QPoint, Qt
from PreviewWindow import PreviewWindow
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
        self.cropVisible = False

        self.dragStart = QPoint()
        self.dragStop = QPoint()

        self.moveStart = None
        self.moveStop = None

        self.diffPoint = None

        previewPen = QPen(QColor("green"))
        previewPen.setWidth(10)
        self.previewPen = previewPen

        cropPreviewPen = QPen(QColor("red"))
        cropPreviewPen.setWidth(10)
        self.cropPreviewPen = cropPreviewPen

        self.videoFrameCropWindow = QRect(0, 0, self.ui.videoFrame.width(), self.ui.videoFrame.height())

        # hide crop selectors
        for child in reversed(range(self.ui.pointSelect1.count())):
            self.ui.pointSelect1.itemAt(child).widget().hide()

        for child in reversed(range(self.ui.pointSelect2.count())):
            self.ui.pointSelect2.itemAt(child).widget().hide()


        self.playPauseButton = self.ui.playPause


        self.previewWindow = self.ui.previewWindow

        self.videoFrame = self.ui.videoFrame

        self.videoFrame.mousePressEvent = self.dragStart

        self.videoFrame.mouseMoveEvent = self.dragContinue

        self.videoFrame.mouseReleaseEvent = self.dragStop

        # setup up signals and slots
        self.ui.loadVideo.clicked.connect(self.openVideo)
        # self.ui.convertGrayScale.clicked.connect(self.convertToGrayScale)
        self.ui.cropButton.clicked.connect(self.startCropping)
        self.ui.playPause.clicked.connect(self.playPause)

        # setup refreshRate of all windows
        self.refreshTimer = QTimer(self)
        self.refreshTimer.timeout.connect(self.update)

    def startCropping(self):
        if self.cropVisible:
            # hide crop selectors
            for child in reversed(range(self.ui.pointSelect1.count())):
                self.ui.pointSelect1.itemAt(child).widget().hide()
            for child in reversed(range(self.ui.pointSelect2.count())):
                self.ui.pointSelect2.itemAt(child).widget().hide()
            self.cropVisible = False
        else:
            # show crop selectors
            for child in reversed(range(self.ui.pointSelect1.count())):
                self.ui.pointSelect1.itemAt(child).widget().show()
            for child in reversed(range(self.ui.pointSelect2.count())):
                self.ui.pointSelect2.itemAt(child).widget().show()
            self.cropVisible = True


    def dragStart(self, event):
        if event.button() == Qt.RightButton:
            # if self.dragStart is not None and self.dragStop is not None:
            #     self.dragStart = None
            #     self.dragStop = None
            self.dragStart = event.pos()
            # if self.dragStart is None:
            #     self.dragStart = event.pos()
            # else:
            #     self.dragStop = event.pos()

        if event.button() == Qt.LeftButton:
            if self.ui.cropButton.isChecked():
                if self.moveStart is not None and self.moveStop is not None:
                    self.moveStart, self.moveEnd = (None, None)
                if self.moveStart is None:
                    # update manual point selecter
                    self.moveStart = event.pos()
                    self.ui.pointSelect1X.setValue(self.moveStart.x())
                    self.ui.pointSelect1Y.setValue(self.moveStart.y())
                else:
                    # update manual point selecter
                    self.moveStop = event.pos()
                    self.ui.pointSelect2X.setValue(self.moveStop.x())
                    self.ui.pointSelect2Y.setValue(self.moveStop.y())

    def dragContinue(self, event):
        if event.buttons() & Qt.MouseButton.RightButton:
            self.dragStop = event.pos()

    def dragStop(self, event):
        # if event.buttons() == Qt.MouseButton.NoButton:
        #     print('hello')
        #     self.prevDx, self.prevDy = (self.prevDx + self.dx, self.prevDy + self.dy)
        pass

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
            frame_width = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))

            self.ui.pointSelect1X.setMaximum(frame_width)
            self.ui.pointSelect2X.setMaximum(frame_width)

            self.ui.pointSelect1Y.setMaximum(frame_height)
            self.ui.pointSelect2Y.setMaximum(frame_height)

            self.playPauseButton.setText("Pause")
            self.refreshTimer.start(1000)

    def paintEvent(self, paintRegion):
        if not self.refreshTimer.isActive():
            return

        # print(self.dragStart, self.dragStop)
        print(self.moveStart, self.moveStop)

        ret, frame = self.video.read()
        if ret:
            # set image to actual Windows
            height, width, channel = frame.shape
            pixmap = QPixmap(QImage(frame.data, width, height, 3 * width, QImage.Format_RGB888))

            # set Image to video Frame
            diffPoint = self.dragStart - self.dragStop
                # self.prevDx, self.prevDy = (self.prevDx + dx, self.prevDy + dy)
                # self.ui.videoFrame.setPixmap(pixmap.copy(0 + self.prevDx, 0 + self.prevDy, self.ui.videoFrame.width() + self.prevDx, self.ui.videoFrame.height() + self.prevDy))
                # self.ui.videoFrame.setPixmap(pixmap.copy(0 + self.dx + self.prevDx, 0 + self.dy + self.prevDy, self.ui.videoFrame.width() + self.dx + self.prevDx, self.ui.videoFrame.height() + self.dy + self.prevDy))
            # self.ui.videoFrame.setPixmap(pixmap.copy(0 + diffPoint.x(), 0 + diffPoint.y(), self.ui.videoFrame.width() + diffPoint.x(), self.ui.videoFrame.height() + diffPoint.y()))
            self.ui.videoFrame.setPixmap(pixmap.copy(self.videoFrameCropWindow.translated(diffPoint)))

            # resize drawn image and show
            # if pixmap.height() > self.previewWindow.height() or pixmap.width() > self.previewWindow.width():
            #     scaledPixmap = pixmap.scaled(self.previewWindow.width(), self.previewWindow.height())
            #     self.previewWindow.setPixmap(scaledPixmap)

            # Preview Window
            newCropWindowMarker = QRect(self.videoFrameCropWindow)
            newCropWindowMarker.translate(diffPoint)

            copyCurrentFrame = pixmap.copy(QRect())

            # draw a green rectangle on a copy of image shown in preview image
            # make a copy of current frame
            previewPainter = QPainter()
            previewPainter.begin(copyCurrentFrame)
            previewPainter.setPen(self.previewPen)
            previewPainter.drawRect(newCropWindowMarker)

            # show the drag line
            if self.dragStart and self.dragStop:
                previewPainter.drawLine(self.dragStart, self.dragStop)

            previewPainter.end()

            copyCurrentFrame = copyCurrentFrame.scaled(self.previewWindow.width(), self.previewWindow.height())

            # draw crop rectangle
            # if self.ui.cropButton.isChecked():
            #         if self.moveStart is not None and self.moveStop is not None:
            #             cropPreviewPainter = QPainter()
            #             cropPreviewPainter.begin(copyCurrentFrame)
            #             cropPreviewPainter.setPen(self.cropPreviewPen)
            #             # cropPreviewPainter.drawRect(self.moveStart.x(), self.moveStart.y(), self.moveStop.x() - self.moveStart.x(), self.moveStop.y() - self.moveStart.y())
            #             cropPreviewPainter.drawRect(0, 0, 100, 100)
            #             cropPreviewPainter.end()
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
