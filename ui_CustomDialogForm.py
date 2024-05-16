# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CustomDialogForm.ui'
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
    QHBoxLayout, QLabel, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_CustomDialogForm(object):
    def setupUi(self, CustomDialogForm):
        if not CustomDialogForm.objectName():
            CustomDialogForm.setObjectName(u"CustomDialogForm")
        CustomDialogForm.resize(438, 257)
        self.gridLayout = QGridLayout(CustomDialogForm)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label = QLabel(CustomDialogForm)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(33)
        font.setBold(True)
        self.label.setFont(font)

        self.verticalLayout_3.addWidget(self.label)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.contourDataEachFrame = QCheckBox(CustomDialogForm)
        self.contourDataEachFrame.setObjectName(u"contourDataEachFrame")

        self.verticalLayout.addWidget(self.contourDataEachFrame)

        self.tipRootOverlayVideo = QCheckBox(CustomDialogForm)
        self.tipRootOverlayVideo.setObjectName(u"tipRootOverlayVideo")

        self.verticalLayout.addWidget(self.tipRootOverlayVideo)

        self.tipRootCoordinates = QCheckBox(CustomDialogForm)
        self.tipRootCoordinates.setObjectName(u"tipRootCoordinates")

        self.verticalLayout.addWidget(self.tipRootCoordinates)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.multiProcessing = QCheckBox(CustomDialogForm)
        self.multiProcessing.setObjectName(u"multiProcessing")

        self.horizontalLayout.addWidget(self.multiProcessing)

        self.multiProcValues = QComboBox(CustomDialogForm)
        self.multiProcValues.setObjectName(u"multiProcValues")

        self.horizontalLayout.addWidget(self.multiProcValues)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.exportButton = QPushButton(CustomDialogForm)
        self.exportButton.setObjectName(u"exportButton")

        self.horizontalLayout_2.addWidget(self.exportButton)

        self.cancelButton = QPushButton(CustomDialogForm)
        self.cancelButton.setObjectName(u"cancelButton")

        self.horizontalLayout_2.addWidget(self.cancelButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.verticalLayout_3.addLayout(self.verticalLayout_2)


        self.gridLayout.addLayout(self.verticalLayout_3, 0, 0, 1, 1)


        self.retranslateUi(CustomDialogForm)

        QMetaObject.connectSlotsByName(CustomDialogForm)
    # setupUi

    def retranslateUi(self, CustomDialogForm):
        CustomDialogForm.setWindowTitle(QCoreApplication.translate("CustomDialogForm", u"Form", None))
        self.label.setText(QCoreApplication.translate("CustomDialogForm", u"Export Data", None))
        self.contourDataEachFrame.setText(QCoreApplication.translate("CustomDialogForm", u"Export Contour Data of each Frame (.csv)", None))
        self.tipRootOverlayVideo.setText(QCoreApplication.translate("CustomDialogForm", u"Export modified video with Tip/Root overlay (.mp4) (ffmeg)", None))
        self.tipRootCoordinates.setText(QCoreApplication.translate("CustomDialogForm", u"Export Data of Tip/Root Co-ordinates vs Time (.csv)", None))
        self.multiProcessing.setText(QCoreApplication.translate("CustomDialogForm", u"Use Multi Processing", None))
        self.exportButton.setText(QCoreApplication.translate("CustomDialogForm", u"Export ", None))
        self.cancelButton.setText(QCoreApplication.translate("CustomDialogForm", u"Cancel", None))
    # retranslateUi

