# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ExportProgressBar.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QProgressBar, QPushButton,
    QSizePolicy, QWidget)

class Ui_ExportProgressBar(object):
    def setupUi(self, ExportProgressBar):
        if not ExportProgressBar.objectName():
            ExportProgressBar.setObjectName(u"ExportProgressBar")
        ExportProgressBar.resize(328, 158)
        self.progressBar = QProgressBar(ExportProgressBar)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(10, 40, 301, 71))
        self.progressBar.setValue(37)
        self.label = QLabel(ExportProgressBar)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 0, 181, 31))
        font = QFont()
        font.setPointSize(17)
        self.label.setFont(font)
        self.exportCancelButton = QPushButton(ExportProgressBar)
        self.exportCancelButton.setObjectName(u"exportCancelButton")
        self.exportCancelButton.setGeometry(QRect(230, 120, 80, 24))

        self.retranslateUi(ExportProgressBar)

        QMetaObject.connectSlotsByName(ExportProgressBar)
    # setupUi

    def retranslateUi(self, ExportProgressBar):
        ExportProgressBar.setWindowTitle(QCoreApplication.translate("ExportProgressBar", u"Form", None))
        self.label.setText(QCoreApplication.translate("ExportProgressBar", u"Exporting Data", None))
        self.exportCancelButton.setText(QCoreApplication.translate("ExportProgressBar", u"Cancel", None))
    # retranslateUi

