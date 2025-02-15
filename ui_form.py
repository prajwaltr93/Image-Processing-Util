# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
    QHBoxLayout, QLabel, QProgressBar, QPushButton,
    QSizePolicy, QSlider, QSpinBox, QVBoxLayout,
    QWidget)
import rc_resources

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1177, 714)
        icon = QIcon()
        icon.addFile(u":/icons/resources/app-icon.svg", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.gridLayout = QGridLayout(MainWindow)
        self.gridLayout.setObjectName(u"gridLayout")
        self.mainWindow = QHBoxLayout()
        self.mainWindow.setObjectName(u"mainWindow")
        self.VideoFrame = QLabel(MainWindow)
        self.VideoFrame.setObjectName(u"VideoFrame")
        self.VideoFrame.setMinimumSize(QSize(800, 600))
        self.VideoFrame.setMaximumSize(QSize(100000, 100000))

        self.mainWindow.addWidget(self.VideoFrame)

        self.optionsLayout = QVBoxLayout()
        self.optionsLayout.setObjectName(u"optionsLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.loadVideo = QPushButton(MainWindow)
        self.loadVideo.setObjectName(u"loadVideo")
        self.loadVideo.setMaximumSize(QSize(16777215, 20))

        self.horizontalLayout_2.addWidget(self.loadVideo)

        self.playPause = QPushButton(MainWindow)
        self.playPause.setObjectName(u"playPause")
        self.playPause.setMaximumSize(QSize(16777215, 20))

        self.horizontalLayout_2.addWidget(self.playPause)


        self.optionsLayout.addLayout(self.horizontalLayout_2)

        self.CropSelectWindow = QVBoxLayout()
        self.CropSelectWindow.setObjectName(u"CropSelectWindow")
        self.cropButton = QCheckBox(MainWindow)
        self.cropButton.setObjectName(u"cropButton")

        self.CropSelectWindow.addWidget(self.cropButton)

        self.cropSelectWindow = QVBoxLayout()
        self.cropSelectWindow.setObjectName(u"cropSelectWindow")
        self.pointSelect1 = QHBoxLayout()
        self.pointSelect1.setObjectName(u"pointSelect1")
        self.pointSelect1X = QSpinBox(MainWindow)
        self.pointSelect1X.setObjectName(u"pointSelect1X")

        self.pointSelect1.addWidget(self.pointSelect1X)

        self.point1Text = QLabel(MainWindow)
        self.point1Text.setObjectName(u"point1Text")

        self.pointSelect1.addWidget(self.point1Text)

        self.pointSelect1Y = QSpinBox(MainWindow)
        self.pointSelect1Y.setObjectName(u"pointSelect1Y")

        self.pointSelect1.addWidget(self.pointSelect1Y)


        self.cropSelectWindow.addLayout(self.pointSelect1)

        self.pointSelect2_2 = QHBoxLayout()
        self.pointSelect2_2.setObjectName(u"pointSelect2_2")
        self.pointSelect2X = QSpinBox(MainWindow)
        self.pointSelect2X.setObjectName(u"pointSelect2X")

        self.pointSelect2_2.addWidget(self.pointSelect2X)

        self.point2Text = QLabel(MainWindow)
        self.point2Text.setObjectName(u"point2Text")

        self.pointSelect2_2.addWidget(self.point2Text)

        self.pointSelect2Y = QSpinBox(MainWindow)
        self.pointSelect2Y.setObjectName(u"pointSelect2Y")

        self.pointSelect2_2.addWidget(self.pointSelect2Y)


        self.cropSelectWindow.addLayout(self.pointSelect2_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.cancelCrop = QPushButton(MainWindow)
        self.cancelCrop.setObjectName(u"cancelCrop")

        self.horizontalLayout_3.addWidget(self.cancelCrop)

        self.confirmCrop = QPushButton(MainWindow)
        self.confirmCrop.setObjectName(u"confirmCrop")

        self.horizontalLayout_3.addWidget(self.confirmCrop)


        self.cropSelectWindow.addLayout(self.horizontalLayout_3)


        self.CropSelectWindow.addLayout(self.cropSelectWindow)


        self.optionsLayout.addLayout(self.CropSelectWindow)

        self.convertToGrayScaleWindow = QVBoxLayout()
        self.convertToGrayScaleWindow.setObjectName(u"convertToGrayScaleWindow")
        self.convertGrayScale = QCheckBox(MainWindow)
        self.convertGrayScale.setObjectName(u"convertGrayScale")

        self.convertToGrayScaleWindow.addWidget(self.convertGrayScale)

        self.applyThresholdWindow = QVBoxLayout()
        self.applyThresholdWindow.setObjectName(u"applyThresholdWindow")
        self.applyThresholdButton = QCheckBox(MainWindow)
        self.applyThresholdButton.setObjectName(u"applyThresholdButton")

        self.applyThresholdWindow.addWidget(self.applyThresholdButton)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.thresholdText = QLabel(MainWindow)
        self.thresholdText.setObjectName(u"thresholdText")
        self.thresholdText.setMaximumSize(QSize(16777215, 20))

        self.horizontalLayout.addWidget(self.thresholdText)

        self.thresholdValue = QLabel(MainWindow)
        self.thresholdValue.setObjectName(u"thresholdValue")
        self.thresholdValue.setMaximumSize(QSize(16777215, 20))

        self.horizontalLayout.addWidget(self.thresholdValue)


        self.applyThresholdWindow.addLayout(self.horizontalLayout)

        self.thresholdSlider = QSlider(MainWindow)
        self.thresholdSlider.setObjectName(u"thresholdSlider")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.thresholdSlider.sizePolicy().hasHeightForWidth())
        self.thresholdSlider.setSizePolicy(sizePolicy)
        self.thresholdSlider.setMaximumSize(QSize(16777215, 20))
        self.thresholdSlider.setMaximum(255)
        self.thresholdSlider.setOrientation(Qt.Horizontal)
        self.thresholdSlider.setTickPosition(QSlider.TicksBelow)

        self.applyThresholdWindow.addWidget(self.thresholdSlider)

        self.showContours = QCheckBox(MainWindow)
        self.showContours.setObjectName(u"showContours")

        self.applyThresholdWindow.addWidget(self.showContours)

        self.tipOrRootSelector = QComboBox(MainWindow)
        self.tipOrRootSelector.setObjectName(u"tipOrRootSelector")

        self.applyThresholdWindow.addWidget(self.tipOrRootSelector)

        self.skeletonize = QCheckBox(MainWindow)
        self.skeletonize.setObjectName(u"skeletonize")

        self.applyThresholdWindow.addWidget(self.skeletonize)


        self.convertToGrayScaleWindow.addLayout(self.applyThresholdWindow)


        self.optionsLayout.addLayout(self.convertToGrayScaleWindow)

        self.previewWindow = QVBoxLayout()
        self.previewWindow.setObjectName(u"previewWindow")
        self.previewWindowText = QLabel(MainWindow)
        self.previewWindowText.setObjectName(u"previewWindowText")
        self.previewWindowText.setMaximumSize(QSize(16777215, 50))
        font = QFont()
        font.setBold(True)
        self.previewWindowText.setFont(font)

        self.previewWindow.addWidget(self.previewWindowText)

        self.PreviewWindow = QLabel(MainWindow)
        self.PreviewWindow.setObjectName(u"PreviewWindow")
        self.PreviewWindow.setMinimumSize(QSize(350, 250))

        self.previewWindow.addWidget(self.PreviewWindow)


        self.optionsLayout.addLayout(self.previewWindow)

        self.exportDataWindowParent = QVBoxLayout()
        self.exportDataWindowParent.setObjectName(u"exportDataWindowParent")
        self.exportData = QCheckBox(MainWindow)
        self.exportData.setObjectName(u"exportData")

        self.exportDataWindowParent.addWidget(self.exportData)

        self.exportDataWindow = QVBoxLayout()
        self.exportDataWindow.setObjectName(u"exportDataWindow")
        self.verticalLayout_15 = QVBoxLayout()
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.contourDataEachFrame = QCheckBox(MainWindow)
        self.contourDataEachFrame.setObjectName(u"contourDataEachFrame")

        self.verticalLayout_15.addWidget(self.contourDataEachFrame)

        self.tipRootOverlayVideo = QCheckBox(MainWindow)
        self.tipRootOverlayVideo.setObjectName(u"tipRootOverlayVideo")

        self.verticalLayout_15.addWidget(self.tipRootOverlayVideo)

        self.tipRootCoordinates = QCheckBox(MainWindow)
        self.tipRootCoordinates.setObjectName(u"tipRootCoordinates")

        self.verticalLayout_15.addWidget(self.tipRootCoordinates)

        self.multiProcLayout = QHBoxLayout()
        self.multiProcLayout.setObjectName(u"multiProcLayout")
        self.multiProcessing = QCheckBox(MainWindow)
        self.multiProcessing.setObjectName(u"multiProcessing")

        self.multiProcLayout.addWidget(self.multiProcessing)

        self.multiProcValues = QComboBox(MainWindow)
        self.multiProcValues.setObjectName(u"multiProcValues")

        self.multiProcLayout.addWidget(self.multiProcValues)


        self.verticalLayout_15.addLayout(self.multiProcLayout)


        self.exportDataWindow.addLayout(self.verticalLayout_15)

        self.progressBar = QProgressBar(MainWindow)
        self.progressBar.setObjectName(u"progressBar")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy1)
        self.progressBar.setValue(0)

        self.exportDataWindow.addWidget(self.progressBar)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.exportButton = QPushButton(MainWindow)
        self.exportButton.setObjectName(u"exportButton")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.exportButton.sizePolicy().hasHeightForWidth())
        self.exportButton.setSizePolicy(sizePolicy2)

        self.horizontalLayout_10.addWidget(self.exportButton)

        self.cancelButton = QPushButton(MainWindow)
        self.cancelButton.setObjectName(u"cancelButton")
        sizePolicy2.setHeightForWidth(self.cancelButton.sizePolicy().hasHeightForWidth())
        self.cancelButton.setSizePolicy(sizePolicy2)

        self.horizontalLayout_10.addWidget(self.cancelButton)


        self.exportDataWindow.addLayout(self.horizontalLayout_10)


        self.exportDataWindowParent.addLayout(self.exportDataWindow)


        self.optionsLayout.addLayout(self.exportDataWindowParent)


        self.mainWindow.addLayout(self.optionsLayout)


        self.gridLayout.addLayout(self.mainWindow, 0, 0, 1, 1)


        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Image Processing Util", None))
        self.VideoFrame.setText("")
        self.loadVideo.setText(QCoreApplication.translate("MainWindow", u"Load Video", None))
        self.playPause.setText(QCoreApplication.translate("MainWindow", u"Play", None))
        self.cropButton.setText(QCoreApplication.translate("MainWindow", u"Crop", None))
        self.point1Text.setText(QCoreApplication.translate("MainWindow", u"Point 1 (x1, y1)", None))
        self.point2Text.setText(QCoreApplication.translate("MainWindow", u"Point 2 (x1, y1)", None))
        self.cancelCrop.setText(QCoreApplication.translate("MainWindow", u"Cancel Crop", None))
        self.confirmCrop.setText(QCoreApplication.translate("MainWindow", u"Confirm Crop", None))
        self.convertGrayScale.setText(QCoreApplication.translate("MainWindow", u"Convert to Gray Scale", None))
        self.applyThresholdButton.setText(QCoreApplication.translate("MainWindow", u"Apply Threshold", None))
        self.thresholdText.setText(QCoreApplication.translate("MainWindow", u"Threshold", None))
        self.thresholdValue.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.showContours.setText(QCoreApplication.translate("MainWindow", u"Show Contours", None))
        self.skeletonize.setText(QCoreApplication.translate("MainWindow", u"Skeletonize", None))
        self.previewWindowText.setText(QCoreApplication.translate("MainWindow", u"Preview Window", None))
        self.PreviewWindow.setText("")
        self.exportData.setText(QCoreApplication.translate("MainWindow", u"Export Data", None))
        self.contourDataEachFrame.setText(QCoreApplication.translate("MainWindow", u"Export Contour Data of each Frame (.csv)", None))
        self.tipRootOverlayVideo.setText(QCoreApplication.translate("MainWindow", u"Export modified video with Tip/Root overlay (.mp4) (ffmeg)", None))
        self.tipRootCoordinates.setText(QCoreApplication.translate("MainWindow", u"Export Data of Tip/Root Co-ordinates vs Time (.csv)", None))
        self.multiProcessing.setText(QCoreApplication.translate("MainWindow", u"Use Multi Processing", None))
        self.exportButton.setText(QCoreApplication.translate("MainWindow", u"Export ", None))
        self.cancelButton.setText(QCoreApplication.translate("MainWindow", u"Cancel", None))
    # retranslateUi

