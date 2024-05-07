# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtWidgets import QApplication, QWidget, QFileDialog, QButtonGroup, QDialog
from PySide6.QtGui import QPixmap, QImage, QPainter, QColor, QPen
from PySide6.QtCore import QTimer, QRect, QPoint, Qt
import cv2
import multiprocessing

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_MainWindow
from ui_CustomDialogForm import Ui_CustomDialogForm

def checkNullPoint(point):
    # fun fact: `is` checks the id() of operands (indirectly memory address), since there can only be one None, two operands
    # pointing to None will have same id (memory address) :)
    if point is None:
        return True

    if point.x() == 0 and point.y() == 0:
        return True
    else:
        return False

def findTip(contours):
    # assume first point to be the point of interest (pun intended :))
    tipPoint = contours[0][0][0]
    for contour in contours:
        for point in contour:
            point = point[0]
            if (point[0] > tipPoint[0] and point[1] < tipPoint[1]):
                tipPoint = point
    return tipPoint

def findRoot(contours):
    # assume first point to be the point of interest (pun intended :))
    tipPoint = contours[0][0][0]
    for contour in contours:
        for point in contour:
            point = point[0]
            if (point[0] < tipPoint[0] and point[1] > tipPoint[1]):
                tipPoint = point
    return tipPoint

class CustomDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        # halt parent refresh timer
        if parent.refreshTimer.isActive():
            parent.refreshTimer.stop()

        self.customDialogUI = Ui_CustomDialogForm()
        self.customDialogUI.setupUi(self)

        # setup accept and reject calls
        self.customDialogUI.exportButton.clicked.connect(self.accept)
        self.customDialogUI.cancelButton.clicked.connect(self.reject)

        # ^_____^
        self.parent = parent

        # populate multi proc values
        cpus = multiprocessing.cpu_count()
        cpuValues = [str(i) for i in range(1, cpus + 1)]
        self.customDialogUI.multiProcValues.addItems(cpuValues)


    def execAndCollect(self):
        result = self.exec()
        if result == QDialog.DialogCode.Accepted:
            # grab all selections and pass it on to parent
            self.parent.startExporting(self.customDialogUI.contourDataEachFrame.isChecked(),
                                        self.customDialogUI.tipRootOverlayVideo.isChecked(),
                                        self.customDialogUI.tipRootCoordinates.isChecked(),
                                        int(self.customDialogUI.multiProcValues.currentText()) if self.customDialogUI.multiProcessing.isChecked() else 0)
        else:
            # cancelled export, start doing what you were doing
            if not self.parent.refreshTimer.isActive() and hasattr(self.parent, "video"):
                self.parent.refreshTimer.start()

class MainWindow(QWidget):

    def startExporting(self, exportContourData, exportContourVideo, exportTipCordinates, multiProcessing):
        # start processing sequentially and a progress bar would be nice
        print(exportContourData, exportContourVideo, exportTipCordinates, multiProcessing)
        if exportContourData:
            pass

        if exportContourVideo:
            pass

        if exportTipCordinates:
            pass


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

        # TODO: improve this hardcoded list
        self.nonExclusiveButtonsList = [self.ui.convertGrayScale, self.ui.skeletonize, self.ui.showContours, self.ui.cropButton, self.ui.applyThresholdButton]

        self.nonExclusiveButtonsBG = QButtonGroup(self)
        for button in self.nonExclusiveButtonsList:
            self.nonExclusiveButtonsBG.addButton(button)
        self.nonExclusiveButtonsBG.setExclusive(False)

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

        tipMarkerPen = QPen(QColor("yellow"))
        tipMarkerPen.setWidth(10)
        self.tipMarkerPen = tipMarkerPen

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
        self.ui.convertGrayScale.clicked.connect(self.convertToGrayScale)
        self.ui.cropButton.clicked.connect(self.startCropping)
        self.ui.playPause.clicked.connect(self.playPause)

        self.ui.thresholdSlider.valueChanged.connect(self.thresholdValueChanged)

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

        # hide show contours combo box
        self.ui.tipOrRootSelector.hide()

        # populate combo box
        contourOptions = ["Tip", "Root"]

        self.ui.tipOrRootSelector.addItems(contourOptions)

        self.ui.showContours.clicked.connect(self.showTipOrRoot)

        # customize the QDialog
        customDialog = CustomDialog(self)
        # customDialog.exec()

        self.ui.exportVideo.clicked.connect(customDialog.execAndCollect)


    def showTipOrRoot(self):
        if self.ui.tipOrRootSelector.isVisible():
            self.ui.tipOrRootSelector.hide()
        else:
            self.ui.tipOrRootSelector.show()


    def thresholdValueChanged(self, value):
        self.ui.thresholdValue.setText(str(value))

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
                    # but account for dragged video frame, it would have moved self.dx and self.dy
                    if not checkNullPoint(self.diffPoint):
                        # TODO: ironically this is setting x,y, width, height. remember this behaviour or fix it (●'◡'●)
                        self.moveStart += self.diffPoint
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

        # debug lines
        # print(self.dragStart, self.dragStop)
        # print(self.moveStart, self.moveStop)

        ret, frame = self.video.read()
        if ret:
            # set image to actual Windows
            height, width, channel = frame.shape

            if self.grayScale:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                bits = width
                pixmap = QPixmap(QImage(frame.data, width, height, bits, QImage.Format_Grayscale8))
                if self.ui.applyThresholdButton.isChecked():
                    _, frame = cv2.threshold(frame, int(self.ui.thresholdSlider.value()), 255, cv2.THRESH_BINARY)
                    pixmap = QPixmap(QImage(frame.data, width, height, bits, QImage.Format_Grayscale8))

                # find contours if selected
                if self.ui.showContours.isChecked():
                    # if cropped, find contours only within it
                    if not self.ui.cropButton.isChecked():
                        contours, _ = cv2.findContours(frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    else:
                        frame = frame[self.moveStart.y(): self.moveStop.y() + self.moveStart.y():, self.moveStart.x(): self.moveStart.x() + self.moveStop.x()]
                        # skeletonize after cropping for better results
                        if self.ui.skeletonize.isChecked():
                            frame = cv2.ximgproc.thinning(frame, cv2.ximgproc.THINNING_ZHANGSUEN)
                        contours, _ = cv2.findContours(frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    # paint all contours on to the screen
                    contourPainter = QPainter()
                    contourPainter.begin(pixmap)
                    contourPainter.setPen(self.cropPreviewPen)

                    # for contour in contours:
                    #     for point in contour:
                    #         point = point[0]
                    #         if self.ui.cropButton.isChecked():
                    #             point[0] += self.moveStart.x()
                    #             point[1] += self.moveStart.y()
                    #         contourPainter.drawEllipse(QPoint(point[0], point[1]), 1, 1)

                    # while drawing circles, account for Tip or Root
                    if self.ui.tipOrRootSelector.currentText() == "Tip":
                        # selectedPoint = contours[-1][0][0]
                        selectedPoint = findTip(contours)
                    else:
                        # selectedPoint = contours[0][0][0]
                        selectedPoint = findRoot(contours)

                    # print(selectedPoint, self.ui.tipOrRootSelector.currentText())
                    selectedPoint[0] += self.moveStart.x()
                    selectedPoint[1] += self.moveStart.y()

                    contourPainter.setPen(self.tipMarkerPen)
                    contourPainter.drawEllipse(QPoint(selectedPoint[0], selectedPoint[1]), 1, 1)

                    contourPainter.end()

            else:
                bits = 3 * width
                pixmap = QPixmap(QImage(frame.data, width, height, bits, QImage.Format_BGR888))

            # set Image to video Frame
            self.diffPoint = self.dragStart - self.dragStop

            # crop has been selected, crop and resize instead
            if self.cropConfirmed:
                # self.ui.videoFrame.setPixmap(pixmap.copy(QRect(self.moveStart, self.moveStop)).scaled(self.videoFrame.width(), self.videoFrame.height()))
                self.ui.videoFrame.setPixmap(pixmap.copy(self.moveStart.x(), self.moveStart.y(), self.moveStop.x(), self.moveStop.y()).scaled(self.videoFrame.width(), self.videoFrame.height()))
                # self.ui.videoFrame.setPixmap(pixmap.copy(self.moveStart.x(), self.moveStart.y(), self.moveStop.x(), self.moveStop.y()))
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

            if not checkNullPoint(self.diffPoint):
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

    def convertToGrayScale(self):
        self.grayScale = not self.grayScale

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
