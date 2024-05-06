# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtWidgets import QApplication, QWidget, QFileDialog, QLabel
from PySide6.QtGui import QPixmap, QImage, QPainter, QColor, QPen
from PySide6.QtCore import QTimer, QRect, QPoint, Qt
import cv2

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_MainWindow


def checkNullPoint(point):
    # fun fact: is checks the id() of operands, since there can only be one None, two operands
    # pointing to None will have same id :)
    if point is None:
        return True

    if point.x() == 0 and point.y() == 0:
        return True
    else:
        return False

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
        self.cropConfirmed = False

        self.dragStart = QPoint()
        self.dragStop = QPoint()

        self.moveStart = QPoint()
        self.moveStop = QPoint()

        self.diffPoint = None

        previewPen = QPen(QColor("green"))
        previewPen.setWidth(10)
        self.previewPen = previewPen

        cropPreviewPen = QPen(QColor("red"))
        cropPreviewPen.setWidth(10)
        self.cropPreviewPen = cropPreviewPen

        self.videoFrameCropWindow = QRect(0, 0, self.ui.videoFrame.width(), self.ui.videoFrame.height())

        self.hideCropGUIAttributes()

        self.playPauseButton = self.ui.playPause


        self.previewWindow = self.ui.previewWindow

        self.videoFrame = self.ui.videoFrame

        self.videoFrame.mousePressEvent = self.dragStartCallBack

        self.videoFrame.mouseMoveEvent = self.dragContinueCallBack

        self.videoFrame.mouseReleaseEvent = self.dragStopCallBack

        # setup up signals and slots
        self.ui.loadVideo.clicked.connect(self.openVideo)
        # self.ui.convertGrayScale.clicked.connect(self.convertToGrayScale)
        self.ui.cropButton.clicked.connect(self.startCropping)
        self.ui.playPause.clicked.connect(self.playPause)

        # connect crop point spin box
        self.ui.pointSelect1X.valueChanged.connect(self.pointSelect1XValueChanged)
        self.ui.pointSelect1Y.valueChanged.connect(self.pointSelect1YValueChanged)

        self.ui.pointSelect2X.valueChanged.connect(self.pointSelect2XValueChanged)
        self.ui.pointSelect2Y.valueChanged.connect(self.pointSelect2YValueChanged)

        # connect confirm and cancel crop here
        self.ui.confirmCrop.clicked.connect(self.confirmCrop)
        self.ui.cancelCrop.clicked.connect(self.cancelCrop)

        # setup refreshRate of all windows
        self.refreshTimer = QTimer(self)
        self.refreshTimer.timeout.connect(self.update)

    def confirmCrop(self):
        # TODO: add a dialog informing resize of videoFrame

        # crop videoFrame and resize to adjust
        self.cropConfirmed = True

    def cancelCrop(self):
        self.cropConfirmed = False
        # also reset moveStart and moveStop
        self.moveStart = QPoint()
        self.moveStop = QPoint()

    def pointSelect2XValueChanged(self, x):
        self.moveStop.setX(x)

    def pointSelect2YValueChanged(self, y):
        self.moveStop.setY(y)

    def pointSelect1XValueChanged(self, x):
        self.moveStart.setX(x)

    def pointSelect1YValueChanged(self, y):
        self.moveStart.setY(y)


    def hideCropGUIAttributes(self):
        # hide crop selectors
        for child in reversed(range(self.ui.pointSelect1.count())):
            self.ui.pointSelect1.itemAt(child).widget().hide()

        for child in reversed(range(self.ui.pointSelect2.count())):
            self.ui.pointSelect2.itemAt(child).widget().hide()

        # hide confirm and cancel crop
        self.ui.cancelCrop.hide()
        self.ui.confirmCrop.hide()

    def showCropGUIAttributes(self):
        # show crop selectors
        for child in reversed(range(self.ui.pointSelect1.count())):
            self.ui.pointSelect1.itemAt(child).widget().show()
        for child in reversed(range(self.ui.pointSelect2.count())):
            self.ui.pointSelect2.itemAt(child).widget().show()

        # show confirm and cancel crop
        self.ui.cancelCrop.show()
        self.ui.confirmCrop.show()


    def startCropping(self):
        if self.cropVisible:
            # hide crop selectors
            self.hideCropGUIAttributes()
            self.cropVisible = False
        else:
            self.showCropGUIAttributes()
            self.cropVisible = True


    def dragStartCallBack(self, event):
        if event.button() == Qt.RightButton:
            self.dragStart = event.pos()
        if event.button() == Qt.LeftButton:
            if self.ui.cropButton.isChecked():
                if checkNullPoint(self.moveStart):
                    # update manual point selecter
                    self.moveStart = event.pos()
                    self.ui.pointSelect1X.setValue(self.moveStart.x())
                    self.ui.pointSelect1Y.setValue(self.moveStart.y())
                else:
                    # update manual point selecter,
                    self.moveStop = event.pos()
                    # but account for dragged video frame, it would have moved self.dx and self.dy
                    if not checkNullPoint(self.diffPoint):
                        # TODO: ironically this is setting x,y, width, height. remember this behaviour or fix it (●'◡'●)
                        self.moveStop += (self.diffPoint - self.moveStart)

                    self.ui.pointSelect2X.setValue(self.moveStop.x())
                    self.ui.pointSelect2Y.setValue(self.moveStop.y())

    def dragContinueCallBack(self, event):
        if event.buttons() & Qt.MouseButton.RightButton:
            self.dragStop = event.pos()
        # else:
        # if event.buttons() & Qt.MouseButton.LeftButton:
        #     # hovering after selecting start crop point
        #     self.moveEnd = event.pos()

    def dragStopCallBack(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            self.dragStop = event.pos()
        # if event.button() == Qt.MouseButton.LeftButton:
        #     self.moveEnd = event.pos()

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
            self.diffPoint = self.dragStart - self.dragStop

            # crop has been selected, crop and resize instead
            if self.cropConfirmed:
                # self.ui.videoFrame.setPixmap(pixmap.copy(QRect(self.moveStart, self.moveStop)).scaled(self.videoFrame.width(), self.videoFrame.height()))
                self.ui.videoFrame.setPixmap(pixmap.copy(self.moveStart.x(), self.moveStart.y(), self.moveStop.x(), self.moveStop.y()).scaled(self.videoFrame.width(), self.videoFrame.height()))
                # self.ui.videoFrame.setPixmap(pixmap.copy(0, 0, 600, 600).scaled(self.videoFrame.width(), self.videoFrame.height()))
            else:
                self.ui.videoFrame.setPixmap(pixmap.copy(self.videoFrameCropWindow.translated(self.diffPoint)))
            # this is slow, TODO: why ?, anchors the image to top left
            # videoFramePainter = QPainter()
            # videoFramePainter.begin(self)
            # videoFramePainter.drawPixmap(QPoint(0, 0), pixmap.copy(self.videoFrameCropWindow.translated(diffPoint)))
            # videoFramePainter.end()

            # Preview Window
            newCropWindowMarker = QRect(self.videoFrameCropWindow)
            newCropWindowMarker.translate(self.diffPoint)

            # get a copy of the current frame, so that it can be scaled and shown in preview window
            copyCurrentFrame = pixmap.copy(QRect())

            # draw a green rectangle on a copy of image shown in preview image
            previewPainter = QPainter()
            previewPainter.begin(copyCurrentFrame)
            previewPainter.setPen(self.previewPen)
            previewPainter.drawRect(newCropWindowMarker)

            # show the drag line
            # if self.dragStart and self.dragStop:
            #     previewPainter.drawLine(self.dragStart, self.dragStop)

            previewPainter.end()


            # draw crop rectangle
            if self.ui.cropButton.isChecked():
                    if not checkNullPoint(self.moveStart) and not checkNullPoint(self.moveStop):
                        cropPreviewPainter = QPainter()
                        cropPreviewPainter.begin(copyCurrentFrame)
                        cropPreviewPainter.setPen(self.cropPreviewPen)
                        # cropPreviewPainter.drawRect(self.moveStart.x(), self.moveStart.y(), self.moveStop.x() - self.moveStart.x(), self.moveStop.y() - self.moveStart.y())
                        cropPreviewPainter.drawRect(self.moveStart.x(), self.moveStart.y(), self.moveStop.x(), self.moveStop.y())
                        cropPreviewPainter.end()

            copyCurrentFrame = copyCurrentFrame.scaled(self.previewWindow.width(), self.previewWindow.height())

            self.previewWindow.setPixmap(copyCurrentFrame)
        return

    def updateFrame(self):
        pass
            # if self.grayScale:
            #     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # pixmap = QPixmap(QImage(frame.data, width, height, width, QImage.Format_Grayscale8))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
