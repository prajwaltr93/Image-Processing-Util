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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
    QRadioButton, QSizePolicy, QSlider, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1280, 720)
        self.widget_2 = QWidget(MainWindow)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setGeometry(QRect(1020, 0, 156, 181))
        self.verticalLayout_2 = QVBoxLayout(self.widget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.convertGrayScale = QRadioButton(self.widget_2)
        self.convertGrayScale.setObjectName(u"convertGrayScale")

        self.verticalLayout_2.addWidget(self.convertGrayScale)

        self.skeletonize = QRadioButton(self.widget_2)
        self.skeletonize.setObjectName(u"skeletonize")

        self.verticalLayout_2.addWidget(self.skeletonize)

        self.showContours = QRadioButton(self.widget_2)
        self.showContours.setObjectName(u"showContours")

        self.verticalLayout_2.addWidget(self.showContours)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.widget_2)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.label_2 = QLabel(self.widget_2)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalSlider = QSlider(self.widget_2)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setOrientation(Qt.Horizontal)

        self.verticalLayout.addWidget(self.horizontalSlider)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.radioButton = QRadioButton(self.widget_2)
        self.radioButton.setObjectName(u"radioButton")

        self.verticalLayout_2.addWidget(self.radioButton)

        self.videoFrame = QLabel(MainWindow)
        self.videoFrame.setObjectName(u"videoFrame")
        self.videoFrame.setGeometry(QRect(10, 0, 1000, 650))
        self.layoutWidget = QWidget(MainWindow)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(1020, 280, 254, 26))
        self.horizontalLayout_2 = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.loadVideo = QPushButton(self.layoutWidget)
        self.loadVideo.setObjectName(u"loadVideo")

        self.horizontalLayout_2.addWidget(self.loadVideo)

        self.exportVideo = QPushButton(self.layoutWidget)
        self.exportVideo.setObjectName(u"exportVideo")

        self.horizontalLayout_2.addWidget(self.exportVideo)

        self.playPause = QPushButton(self.layoutWidget)
        self.playPause.setObjectName(u"playPause")

        self.horizontalLayout_2.addWidget(self.playPause)

        self.previewWindow = QLabel(MainWindow)
        self.previewWindow.setObjectName(u"previewWindow")
        self.previewWindow.setGeometry(QRect(1020, 390, 251, 191))
        self.previewWindowText = QLabel(MainWindow)
        self.previewWindowText.setObjectName(u"previewWindowText")
        self.previewWindowText.setGeometry(QRect(1020, 360, 121, 16))

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.convertGrayScale.setText(QCoreApplication.translate("MainWindow", u"Convert to Gray Scale", None))
        self.skeletonize.setText(QCoreApplication.translate("MainWindow", u"Skeletonize", None))
        self.showContours.setText(QCoreApplication.translate("MainWindow", u"Show Contours", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Threshold", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.radioButton.setText(QCoreApplication.translate("MainWindow", u"resize", None))
        self.videoFrame.setText("")
        self.loadVideo.setText(QCoreApplication.translate("MainWindow", u"Load Video", None))
        self.exportVideo.setText(QCoreApplication.translate("MainWindow", u"Export Data", None))
        self.playPause.setText(QCoreApplication.translate("MainWindow", u"Play", None))
        self.previewWindow.setText("")
        self.previewWindowText.setText(QCoreApplication.translate("MainWindow", u"Preview Window", None))
    # retranslateUi

