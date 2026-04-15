# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.11.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QMainWindow, QMenu, QMenuBar,
    QPushButton, QSizePolicy, QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.actioneeeerrrrr = QAction(MainWindow)
        self.actioneeeerrrrr.setObjectName(u"actioneeeerrrrr")
        self.actionttttggg = QAction(MainWindow)
        self.actionttttggg.setObjectName(u"actionttttggg")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(320, 240, 81, 25))
        self.DialogButton = QPushButton(self.centralwidget)
        self.DialogButton.setObjectName(u"DialogButton")
        self.DialogButton.setGeometry(QRect(310, 170, 81, 25))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        self.menueeeee = QMenu(self.menubar)
        self.menueeeee.setObjectName(u"menueeeee")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menueeeee.menuAction())
        self.menueeeee.addAction(self.actioneeeerrrrr)
        self.menueeeee.addAction(self.actionttttggg)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actioneeeerrrrr.setText(QCoreApplication.translate("MainWindow", u"eeeerrrrr", None))
        self.actionttttggg.setText(QCoreApplication.translate("MainWindow", u"ttttggg", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.DialogButton.setText(QCoreApplication.translate("MainWindow", u"DialogButton", None))
        self.menueeeee.setTitle(QCoreApplication.translate("MainWindow", u"eeeee", None))
    # retranslateUi

