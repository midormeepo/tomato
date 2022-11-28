from PySide6.QtCore import QRect, QMetaObject, Qt
from PySide6.QtWidgets import QLabel, QPushButton


class AboutWindow(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.repaint()

        Dialog.resize(400, 300)

        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(60, 10, 261, 231))
        self.label.setStyleSheet(u"background-color: rgb(215, 255, 252);")
        self.btn_quit = QPushButton(Dialog)
        self.btn_quit.setObjectName(u"btn_quit")
        self.btn_quit.setGeometry(QRect(280, 20, 31, 24))
        self.btn_quit.clicked.connect(self.handle_close)


        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(80, 50, 221, 141))
        self.label_2.setOpenExternalLinks(True)
        self.btn_quit.setText(u"X")
        self.label.setText("")
        self.label_2.setText(u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:700;\">Desktop-tomato</span><span style=\" font-size:12pt;\">\ud83c\udf45 </span><span style=\" font-size:10pt;\">v1.1.1</span></p><p align=\"center\"><span style=\" font-size:10pt;\">@DNZJ </span></p><p><span style=\" font-size:10pt;\">Check Github Update: </span><a href=\"https://github.com/midormeepo/tomato\"><span style=\" font-size:10pt; text-decoration: underline; color:#0000ff;\">Click Here</span></a></p></body></html>")

        QMetaObject.connectSlotsByName(Dialog)
    def handle_close(self):
        self.hide()
