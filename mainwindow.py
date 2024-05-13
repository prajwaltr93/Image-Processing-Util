# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtWidgets import QApplication, QWidget, QFileDialog, QLayout
from PySide6.QtGui import QPixmap, QImage, QPainter, QColor, QPen
from PySide6.QtCore import QTimer, QRect, QPoint, Qt, QThread, Signal
import cv2
import os
import multiprocessing
import csv
from subprocess import Popen, PIPE
from PIL import Image

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_MainWindow

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
    min_x = float('inf')
    max_y = -float('inf')
    rootPoint = None
    for contour in contours:
        for point in contour:
            point = point[0]
            if (point[0] < min_x or (point[0] == min_x and tipPoint[1] > max_y)):
                min_x = point[0]
                max_y = point[1]
                rootPoint = point
    return rootPoint 

class WorkerThread(QThread):
    finished = Signal()
    updateProgress = Signal(int)

    def __init__(self, parent):
        super().__init__(parent)

    def setup(self, configDict):
        self.configDict = configDict

    def run(self):
        self.exportContourData = self.configDict["exportContourData"]
        self.exportContourVideo = self.configDict["exportContourVideo"]
        self.exportTipCordinates = self.configDict["exportTipCordinates"]
        self.videoCapture = self.configDict["videoCaptureHandle"]

        self.numFrames = self.videoCapture.get(cv2.CAP_PROP_FPS)

        self.processHandle = self.configDict["processHandle"]

        # process the video based on configured parameters, threshold, crop, grayscale and skeletonize
        # and extract data also the number of frames for progress bar
        if self.exportContourVideo:
            pass

        if self.exportTipCordinates:
            csvTipRootDataHandle = open(f"output/{self.configDict['tipOrRootSelection']}.csv", "w", newline='')
            csvTipRootDataWriter = csv.writer(csvTipRootDataHandle)

        index = 0
        while True:
            ret, originalFrame = self.videoCapture.read()
            

            if not ret:
                break
            # TODO: use multi proc if configured
            # TODO: sanity check

            # set image to actual Windows
            frame = cv2.cvtColor(originalFrame, cv2.COLOR_BGR2GRAY)
            _, frame = cv2.threshold(frame, int(self.configDict['thresholdValue']), 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            frame = frame[self.configDict['moveStart'].y(): self.configDict['moveStop'].y(), self.configDict['moveStart'].x(): self.configDict['moveStop'].x()]

            # skeletonize after cropping for better results
            frame = cv2.ximgproc.thinning(frame, cv2.ximgproc.THINNING_ZHANGSUEN)
            contours, _ = cv2.findContours(frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # find contours if selected
            if self.exportContourData:
                # if cropped, find contours only within it
                csvContourDataHandle = open(f"output/contour-data/ContourData_Frame_{index}.csv", "w", newline='')
                csvContourDataWriter = csv.writer(csvContourDataHandle)

                for contour in contours:
                    for point in contour:
                        point = point[0]
                        point[0] += self.configDict['moveStart'].x()
                        point[1] += self.configDict['moveStart'].y()
                        csvContourDataWriter.writerow(point)
                csvContourDataHandle.close()


            if self.exportTipCordinates:
                # while drawing circles, account for Tip or Root
                if self.configDict['tipOrRootSelection'] == "Tip":
                    # selectedPoint = contours[-1][0][0]
                    selectedPoint = findTip(contours)
                else:
                    # selectedPoint = contours[0][0][0]
                    selectedPoint = findRoot(contours)
                    # print(selectedPoint, self.ui.tipOrRootSelector.currentText())
                selectedPoint[0] += self.configDict['moveStart'].x()
                selectedPoint[1] += self.configDict['moveStart'].y()
                if self.exportContourVideo:
                    cv2.circle(originalFrame, selectedPoint, 5, (0, 0, 255), -1)

                csvTipRootDataWriter.writerow(selectedPoint)

            if self.exportContourVideo:
                Image.fromarray(originalFrame).save(self.processHandle.stdin, 'JPEG')


            # update progress bar
            self.updateProgress.emit(index)

            index += 1

        # close all file handles
        if self.exportTipCordinates:
            csvTipRootDataHandle.close()

        self.videoCapture.release()
        # notify parent
        self.finished.emit()

class MainWindow(QWidget):

    def updateProgressBar(self, index):
        self.ui.progressBar.setValue((index/self.numFrames) * 100)

    def startExporting(self):
        if hasattr(self, "video"):
            # close the video handle and get a new one
            self.video.release()

        if not os.path.isdir("output"):
            os.mkdir("output")

        if not os.path.isdir("output/contour-data"):
            os.mkdir("output/contour-data")

        videoCapture = cv2.VideoCapture(self.fileName)
        self.frameRate = videoCapture.get(cv2.CAP_PROP_FPS)
        self.numFrames = videoCapture.get(cv2.CAP_PROP_FRAME_COUNT)

        if self.ui.tipRootOverlayVideo.isChecked():
            self.processHandle = Popen(['D:\\ffmpeg-binaries\\bin\\ffmpeg', '-y', '-f', 'image2pipe', '-vcodec', 'mjpeg', '-r', f'{self.frameRate}', '-i', '-', '-vcodec', 'h264', '-r', f'{self.frameRate}', './output/output-video.mp4'], stdin=PIPE)
        else:
            self.processHandle = None

        # prep a dict to carry all necessary information that is bound a MainWindow attributes
        # '''
        configDict = {
                "exportContourData" : self.ui.contourDataEachFrame.isChecked(),
                "exportContourVideo" : self.ui.tipRootOverlayVideo.isChecked(),
                "exportTipCordinates" : self.ui.tipRootCoordinates.isChecked(),
                "videoCaptureHandle" : videoCapture,
                "thresholdValue" : self.ui.thresholdSlider.value(),
                "moveStart" : self.moveStart,
                "moveStop" : self.moveStop,
                "tipOrRootSelection" : self.ui.tipOrRootSelector.currentText(),
                "progressBarObject" : self.ui.progressBar,
                # TODO: multi processing
                "processHandle" : self.processHandle
        }
        # '''

        # disable export while one is already running
        self.ui.exportButton.setDisabled(True)
        self.workerThread = WorkerThread(self)
        self.workerThread.setup(configDict)
        self.workerThread.finished.connect(self.onThreadFinished)
        self.workerThread.updateProgress.connect(self.updateProgressBar)
        self.workerThread.start()

    def onThreadFinished(self):
        self.ui.progressBar.setValue(0)
        if self.processHandle:
            self.processHandle.stdin.close()
            self.processHandle.wait()
        self.ui.exportButton.setDisabled(False)

    def hideWindowsRecursive(self, window):
        # DFS !
        if isinstance(window, QLayout):
            # handle all Children
            for child in reversed(range(window.count())):
                childInstance = window.itemAt(child)
                if isinstance(childInstance, QLayout):
                    self.hideWindowsRecursive(childInstance)
                else:
                    childInstance.widget().hide()
        else:
            # end condition
            # likely a widget, hide it !!
            window.hide()

    def showWindowsRecursive(self, window):
        # DFS !
        if isinstance(window, QLayout):
            # handle all Children
            for child in reversed(range(window.count())):
                childInstance = window.itemAt(child)
                if isinstance(childInstance, QLayout):
                    self.showWindowsRecursive(childInstance)
                else:
                    childInstance.widget().show()
        else:
            # end condition
            # likely a widget, show it !!
            window.show()


    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # set window title

        # Instance Attributes
        self.fileName = None
        self.currentFrame = None
        self.grayScale = False
        self.cropConfirmed = False
        self.workerThread = None

        self.dragStart = QPoint()
        self.dragStop = QPoint()

        self.moveStart = QPoint()
        self.moveStop = QPoint()

        self.diffPoint = QPoint()

        previewPen = QPen(QColor("green"))
        previewPen.setWidth(10)
        self.previewPen = previewPen

        cropPreviewPen = QPen(QColor("red"))
        cropPreviewPen.setWidth(10)
        self.cropPreviewPen = cropPreviewPen

        tipMarkerPen = QPen(QColor("yellow"))
        tipMarkerPen.setWidth(10)
        self.tipMarkerPen = tipMarkerPen

        self.videoFrameCropWindow = QRect(0, 0, self.ui.VideoFrame.width(), self.ui.VideoFrame.height())

        # hide crop options for now
        self.hideWindowsRecursive(self.ui.cropSelectWindow)
        self.ui.cropButton.clicked.connect(self.handleCropClick)

        # hide applyThresholdwindow for now
        self.hideWindowsRecursive(self.ui.applyThresholdWindow)
        self.ui.convertGrayScale.clicked.connect(self.handleGrayScaleConv)

        # hide Preview and Export Window
        self.hideWindowsRecursive(self.ui.previewWindow)
        self.hideWindowsRecursive(self.ui.exportDataWindow)
        self.ui.exportData.clicked.connect(self.handleExportCallBack)

        # '''
        self.playPauseButton = self.ui.playPause
        self.previewWindow = self.ui.PreviewWindow
        self.videoFrame = self.ui.VideoFrame

        self.videoFrame.mousePressEvent = self.dragStartCallBack
        self.videoFrame.mouseMoveEvent = self.dragContinueCallBack
        self.videoFrame.mouseReleaseEvent = self.dragStopCallBack

        self.videoFrame.resizeEvent = self.handleVideoFrameResize

        # setup up signals and slots
        self.ui.loadVideo.clicked.connect(self.openVideo)
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

        # populate combo box
        contourOptions = ["Tip", "Root", "All"]
        self.ui.tipOrRootSelector.addItems(contourOptions)

        # '''
        # setup refreshRate of all windows
        self.refreshTimer = QTimer(self)
        self.refreshTimer.timeout.connect(self.update)

        # populate multi proc values
        cpus = multiprocessing.cpu_count()
        cpuValues = [str(i) for i in range(1, cpus + 1)]
        self.ui.multiProcValues.addItems(cpuValues)

        # on clicking export
        self.ui.exportButton.clicked.connect(self.startExporting)

        # on clicking abort export
        self.ui.cancelButton.clicked.connect(self.stopExport)

        # self.ui.cropButton.setChecked(True)
        # self.ui.convertGrayScale.setChecked(True)
        # self.ui.applyThresholdButton.setChecked(True)
        self.ui.thresholdSlider.setValue(38)

        # self.moveStart = QPoint(1089, 407)
        # self.moveStop = QPoint(1610, 699)

    def stopExport(self):
        if isinstance(self.workerThread, QThread):
            self.workerThread.terminate()
            # TODO: wait while thread terminates
            # also close necessary files, maybe under when clause

    # handle videoFrame resize event
    def handleVideoFrameResize(self, ResizeEvent):
        self.videoFrameCropWindow = QRect(0, 0, self.ui.VideoFrame.width(), self.ui.VideoFrame.height())

    def handleGrayScaleConv(self):
        if self.ui.convertGrayScale.isChecked():
            self.showWindowsRecursive(self.ui.applyThresholdWindow)
        else:
            self.hideWindowsRecursive(self.ui.applyThresholdWindow)

    def handleCropClick(self):
        if self.ui.cropButton.isChecked():
            self.showWindowsRecursive(self.ui.cropSelectWindow)
        else:
            self.hideWindowsRecursive(self.ui.cropSelectWindow)

    def handleExportCallBack(self):
        if self.ui.exportData.isChecked():
            self.showWindowsRecursive(self.ui.exportDataWindow)
        else:
            self.hideWindowsRecursive(self.ui.exportDataWindow)

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

    def dragStartCallBack(self, event):
        if event.button() == Qt.RightButton:
            self.dragStart = event.pos()
        if event.button() == Qt.LeftButton:
            if self.ui.cropButton.isChecked():
                if checkNullPoint(self.moveStart):
                    # first point hasn't been selected yet. capture that !
                    self.moveStart = event.pos()
                    # but account for dragged video frame, it would have moved self.dx and self.dy
                    if not checkNullPoint(self.diffPoint):
                        # TODO: ironically this is setting x,y, width, height. remember this behaviour or fix it (●'◡'●)
                        self.moveStart += self.diffPoint

                    # update manual point selecter
                    self.ui.pointSelect1X.setValue(self.moveStart.x())
                    self.ui.pointSelect1Y.setValue(self.moveStart.y())
                else:
                    # we have a first point, let's get the second 
                    self.moveStop = event.pos()
                    # but account for dragged video frame, it would have moved self.dx and self.dy
                    if not checkNullPoint(self.diffPoint):
                        # TODO: ironically this is setting x,y, width, height. remember this behaviour or fix it (●'◡'●)
                        # self.moveStop += (self.diffPoint - self.moveStart)
                        self.moveStop += self.diffPoint
                    # update manual point selecter,
                    self.ui.pointSelect2X.setValue(self.moveStop.x())
                    self.ui.pointSelect2Y.setValue(self.moveStop.y())

    def dragContinueCallBack(self, event):
        if event.buttons() & Qt.MouseButton.RightButton:
            self.dragStop = event.pos()

    def dragStopCallBack(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            self.dragStop = event.pos()

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
        # self.fileName = "D:\\point detection algorithm implementation-python\\750_trimmed.mp4"
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

            # enable Preview Window
            self.showWindowsRecursive(self.ui.previewWindow)

    def paintEvent(self, paintRegion):
        if not self.refreshTimer.isActive():
            return

        # debug lines
        # print(self.dragStart, self.dragStop)
        # print(self.moveStart, self.moveStop)

        ret, frame = self.video.read()
        if ret:
            # set image to actual Windows
            height, width, _ = frame.shape

            if self.ui.convertGrayScale.isChecked():
                bits = width
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
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
                        # frame = frame[self.moveStart.y(): self.moveStop.y() + self.moveStart.y(), self.moveStart.x(): self.moveStart.x() + self.moveStop.x()]
                        frame = frame[self.moveStart.y(): self.moveStop.y(), self.moveStart.x(): self.moveStop.x()]
                        # skeletonize after cropping for better results
                        if self.ui.skeletonize.isChecked():
                            frame = cv2.ximgproc.thinning(frame, cv2.ximgproc.THINNING_ZHANGSUEN)

                        contours, _ = cv2.findContours(frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                    # paint all contours on to the screen
                    contourPainter = QPainter()
                    contourPainter.begin(pixmap)
                    contourPainter.setPen(self.cropPreviewPen)

                    if self.ui.tipOrRootSelector.currentText() == "All":
                        for contour in contours:
                            for point in contour:
                                point = point[0]
                                if self.ui.cropButton.isChecked():
                                    point[0] += self.moveStart.x()
                                    point[1] += self.moveStart.y()
                                contourPainter.drawEllipse(QPoint(point[0], point[1]), 1, 1)

                    # while drawing circles, account for Tip or Root
                    if self.ui.tipOrRootSelector.currentText() == "Tip":
                        # selectedPoint = contours[-1][0][0]
                        selectedPoint = findTip(contours)
                    else:
                        # selectedPoint = contours[0][0][0]
                        selectedPoint = findRoot(contours)

                    if self.ui.tipOrRootSelector.currentText() != "All":
                        # Tip or GROOOT
                        selectedPoint[0] += self.moveStart.x()
                        selectedPoint[1] += self.moveStart.y()

                        contourPainter.setPen(self.tipMarkerPen)
                        contourPainter.drawEllipse(QPoint(selectedPoint[0], selectedPoint[1]), 1, 1)

                    contourPainter.end()
            else:
                # just plain vanilla image as is
                bits = 3 * width
                pixmap = QPixmap(QImage(frame.data, width, height, bits, QImage.Format_BGR888))

            # set Image to video Frame
            self.diffPoint = self.dragStart - self.dragStop

            if self.cropConfirmed:
                # crop has been selected, crop and resize instead
                self.ui.VideoFrame.setPixmap(pixmap.copy(self.moveStart.x(), self.moveStart.y(), self.moveStop.x() - self.moveStart.x(), self.moveStop.y() - self.moveStart.y()).scaled(self.videoFrame.width(), self.videoFrame.height()))
            else:
                self.ui.VideoFrame.setPixmap(pixmap.copy(self.videoFrameCropWindow.translated(self.diffPoint)))

            # Preview Window, get a copy of current videoFrame
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
            previewPainter.end()

            # draw crop rectangle, if selected
            if self.ui.cropButton.isChecked():
                if not checkNullPoint(self.moveStart) and not checkNullPoint(self.moveStop):
                    cropPreviewPainter = QPainter()
                    cropPreviewPainter.begin(copyCurrentFrame)
                    cropPreviewPainter.setPen(self.cropPreviewPen)
                    cropPreviewPainter.drawRect(self.moveStart.x(), self.moveStart.y(), self.moveStop.x() - self.moveStart.x(), self.moveStop.y() - self.moveStart.y())
                    cropPreviewPainter.end()

            copyCurrentFrame = copyCurrentFrame.scaled(self.previewWindow.width(), self.previewWindow.height())
            self.previewWindow.setPixmap(copyCurrentFrame)

        # end of painting pipeline
        return

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
