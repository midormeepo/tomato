from PySide6.QtCore import QRect, Qt
from PySide6.QtWidgets import QWidget, QLabel, QPushButton


class AboutWindow(QWidget):
    def __init__(self, parent=None):
        super(AboutWindow, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.repaint()

        self.resize(400, 300)

        self.label = QLabel(self)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(60, 10, 261, 231))
        self.label.setStyleSheet(u"background-color: rgb(215, 255, 252);")
        self.btn_quit = QPushButton(self)
        self.btn_quit.setObjectName(u"btn_quit")
        self.btn_quit.setGeometry(QRect(280, 20, 31, 24))
        self.btn_quit.clicked.connect(self.handle_close)


        self.label_2 = QLabel(self)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(80, 50, 221, 141))
        self.label_2.setOpenExternalLinks(True)
        self.btn_quit.setText(u"X")
        self.label.setText("")
        self.label_2.setText(u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:700;\">Desktop-tomato</span><span style=\" font-size:12pt;\">\ud83c\udf45 </span><span style=\" font-size:10pt;\">v1.1.1</span></p><p align=\"center\"><span style=\" font-size:10pt;\">@DNZJ </span></p><p><span style=\" font-size:10pt;\">Check Github: </span><a href=\"https://github.com/midormeepo/tomato\"><span style=\" font-size:10pt; text-decoration: underline; color:#0000ff;\">Desktop-tomato</span></a></p></body></html>")


    def handle_close(self):
        self.hide()
