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
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
    QPushButton, QRadioButton, QSizePolicy, QSlider,
    QSpinBox, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1280, 720)
        self.videoFrame = QLabel(MainWindow)
        self.videoFrame.setObjectName(u"videoFrame")
        self.videoFrame.setGeometry(QRect(10, 0, 1011, 711))
        self.layoutWidget = QWidget(MainWindow)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(1030, 0, 244, 618))
        self.verticalLayout_3 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.optionsWidget = QWidget(self.layoutWidget)
        self.optionsWidget.setObjectName(u"optionsWidget")
        self.verticalLayout_2 = QVBoxLayout(self.optionsWidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.skeletonize = QRadioButton(self.optionsWidget)
        self.skeletonize.setObjectName(u"skeletonize")

        self.verticalLayout_2.addWidget(self.skeletonize)

        self.showContours = QRadioButton(self.optionsWidget)
        self.showContours.setObjectName(u"showContours")

        self.verticalLayout_2.addWidget(self.showContours)

        self.tipOrRootSelector = QComboBox(self.optionsWidget)
        self.tipOrRootSelector.setObjectName(u"tipOrRootSelector")

        self.verticalLayout_2.addWidget(self.tipOrRootSelector)

        self.convertGrayScale = QRadioButton(self.optionsWidget)
        self.convertGrayScale.setObjectName(u"convertGrayScale")

        self.verticalLayout_2.addWidget(self.convertGrayScale)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.applyThresholdButton = QRadioButton(self.optionsWidget)
        self.applyThresholdButton.setObjectName(u"applyThresholdButton")

        self.verticalLayout.addWidget(self.applyThresholdButton)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.optionsWidget)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(16777215, 20))

        self.horizontalLayout.addWidget(self.label)

        self.thresholdValue = QLabel(self.optionsWidget)
        self.thresholdValue.setObjectName(u"thresholdValue")
        self.thresholdValue.setMaximumSize(QSize(16777215, 20))

        self.horizontalLayout.addWidget(self.thresholdValue)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.thresholdSlider = QSlider(self.optionsWidget)
        self.thresholdSlider.setObjectName(u"thresholdSlider")
        self.thresholdSlider.setMaximumSize(QSize(16777215, 20))
        self.thresholdSlider.setMaximum(255)
        self.thresholdSlider.setOrientation(Qt.Horizontal)
        self.thresholdSlider.setTickPosition(QSlider.TicksBelow)

        self.verticalLayout.addWidget(self.thresholdSlider)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.cropButton = QRadioButton(self.optionsWidget)
        self.cropButton.setObjectName(u"cropButton")

        self.verticalLayout_2.addWidget(self.cropButton)

        self.pointSelect1 = QHBoxLayout()
        self.pointSelect1.setObjectName(u"pointSelect1")
        self.pointSelect1X = QSpinBox(self.optionsWidget)
        self.pointSelect1X.setObjectName(u"pointSelect1X")

        self.pointSelect1.addWidget(self.pointSelect1X)

        self.label_3 = QLabel(self.optionsWidget)
        self.label_3.setObjectName(u"label_3")

        self.pointSelect1.addWidget(self.label_3)

        self.pointSelect1Y = QSpinBox(self.optionsWidget)
        self.pointSelect1Y.setObjectName(u"pointSelect1Y")

        self.pointSelect1.addWidget(self.pointSelect1Y)


        self.verticalLayout_2.addLayout(self.pointSelect1)

        self.pointSelect2 = QHBoxLayout()
        self.pointSelect2.setObjectName(u"pointSelect2")
        self.pointSelect2X = QSpinBox(self.optionsWidget)
        self.pointSelect2X.setObjectName(u"pointSelect2X")

        self.pointSelect2.addWidget(self.pointSelect2X)

        self.label_4 = QLabel(self.optionsWidget)
        self.label_4.setObjectName(u"label_4")

        self.pointSelect2.addWidget(self.label_4)

        self.pointSelect2Y = QSpinBox(self.optionsWidget)
        self.pointSelect2Y.setObjectName(u"pointSelect2Y")

        self.pointSelect2.addWidget(self.pointSelect2Y)


        self.verticalLayout_2.addLayout(self.pointSelect2)

        self.confirmCrop = QPushButton(self.optionsWidget)
        self.confirmCrop.setObjectName(u"confirmCrop")

        self.verticalLayout_2.addWidget(self.confirmCrop)

        self.cancelCrop = QPushButton(self.optionsWidget)
        self.cancelCrop.setObjectName(u"cancelCrop")

        self.verticalLayout_2.addWidget(self.cancelCrop)


        self.verticalLayout_3.addWidget(self.optionsWidget)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.loadVideo = QPushButton(self.layoutWidget)
        self.loadVideo.setObjectName(u"loadVideo")
        self.loadVideo.setMaximumSize(QSize(16777215, 20))

        self.horizontalLayout_2.addWidget(self.loadVideo)

        self.exportVideo = QPushButton(self.layoutWidget)
        self.exportVideo.setObjectName(u"exportVideo")
        self.exportVideo.setMaximumSize(QSize(16777215, 20))

        self.horizontalLayout_2.addWidget(self.exportVideo)

        self.playPause = QPushButton(self.layoutWidget)
        self.playPause.setObjectName(u"playPause")
        self.playPause.setMaximumSize(QSize(16777215, 20))

        self.horizontalLayout_2.addWidget(self.playPause)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.previewWindowText = QLabel(self.layoutWidget)
        self.previewWindowText.setObjectName(u"previewWindowText")
        self.previewWindowText.setMaximumSize(QSize(16777215, 50))

        self.verticalLayout_3.addWidget(self.previewWindowText)

        self.previewWindow = QLabel(self.layoutWidget)
        self.previewWindow.setObjectName(u"previewWindow")
        self.previewWindow.setMinimumSize(QSize(200, 200))
        self.previewWindow.setMaximumSize(QSize(16777215, 400))

        self.verticalLayout_3.addWidget(self.previewWindow)


        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.videoFrame.setText("")
        self.skeletonize.setText(QCoreApplication.translate("MainWindow", u"Skeletonize", None))
        self.showContours.setText(QCoreApplication.translate("MainWindow", u"Show Contours", None))
        self.convertGrayScale.setText(QCoreApplication.translate("MainWindow", u"Convert to Gray Scale", None))
        self.applyThresholdButton.setText(QCoreApplication.translate("MainWindow", u"Apply Threshold", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Threshold", None))
        self.thresholdValue.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.cropButton.setText(QCoreApplication.translate("MainWindow", u"Crop", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Point 1 (x1, y1)", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Point 2 (x1, y1)", None))
        self.confirmCrop.setText(QCoreApplication.translate("MainWindow", u"Confirm Crop", None))
        self.cancelCrop.setText(QCoreApplication.translate("MainWindow", u"Cancel Crop", None))
        self.loadVideo.setText(QCoreApplication.translate("MainWindow", u"Load Video", None))
        self.exportVideo.setText(QCoreApplication.translate("MainWindow", u"Export Data", None))
        self.playPause.setText(QCoreApplication.translate("MainWindow", u"Play", None))
        self.previewWindowText.setText(QCoreApplication.translate("MainWindow", u"Preview Window", None))
        self.previewWindow.setText("")
    # retranslateUi

