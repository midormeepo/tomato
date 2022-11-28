
from PySide6.QtCore import QPoint, QRect
from PySide6.QtGui import QPainter, QPen, Qt, QBrush, QPolygon, QColor, QFont, QPainterPath


def tomato(self):
    qp1 = QPainter(self)
    qp1.setRenderHint(QPainter.Antialiasing)
    # 设置画笔
    pen = QPen()
    pen.setWidth(2)  # 线宽
    pen.setColor(Qt.white)  # 画线颜色
    pen.setStyle(Qt.SolidLine)  # 线的类型，如实线、虚线等
    pen.setCapStyle(Qt.FlatCap)  # 线端点样式
    pen.setJoinStyle(Qt.RoundJoin)  # 线的连接点样式
    qp1.setPen(pen)
    qp1.scale(self.size, self.size)

    # 设置画刷
    brush = QBrush()
    brush.setStyle(Qt.SolidPattern)
    if self.condition < 60:  # 绿色
        brush.setColor(QColor(60 + round(self.condition) * 2.75, 225, 0, 200))
    elif self.condition >= 60 & self.condition < 130:  # 红色
        brush.setColor(QColor(225, 450 - round(self.condition) * 3.75, 0, 200))
    # 填充样式
    qp1.setBrush(brush)
    qp1.translate(-5, 4)
    qp1.rotate(-8)
    qp1.drawChord(2, 7, 74, 65, 110 * 18, 270 * 18)


# 高光
def highlight(self):
    qp5 = QPainter(self)
    qp5.setRenderHint(QPainter.Antialiasing)
    ##设置画笔
    pen = QPen()
    pen.setWidth(2)  # 线宽
    pen.setColor(Qt.transparent)  # 画线颜色
    pen.setStyle(Qt.SolidLine)  # 线的类型，如实线、虚线等
    pen.setCapStyle(Qt.FlatCap)  # 线端点样式
    pen.setJoinStyle(Qt.RoundJoin)  # 线的连接点样式
    qp5.setPen(pen)
    qp5.scale(self.size, self.size)
    ##设置画刷
    brush = QBrush()
    brush.setColor(QColor(255, 255, 255, 120))
    brush.setStyle(Qt.SolidPattern)  # 填充样式
    qp5.setBrush(brush)
    qp5.translate(50, 25)
    qp5.drawEllipse(5, 5, 10, 8)


# 果实阴影
def tomato_mask(self):
    qp4 = QPainter(self)
    qp4.setRenderHint(QPainter.Antialiasing)
    ##设置画笔
    pen = QPen()
    pen.setWidth(2)  # 线宽
    pen.setColor(Qt.transparent)  # 画线颜色
    pen.setStyle(Qt.SolidLine)  # 线的类型，如实线、虚线等
    pen.setCapStyle(Qt.FlatCap)  # 线端点样式
    pen.setJoinStyle(Qt.RoundJoin)  # 线的连接点样式
    qp4.setPen(pen)
    qp4.scale(self.size, self.size)
    ##设置画刷
    brush4 = QBrush()
    brush4.setStyle(Qt.SolidPattern)  # 填充样式
    brush4.setColor(QColor(0, 0, 0, 50))
    # brush4.setColor(QColor(0, 0, 0, 255))
    qp4.setBrush(brush4)
    # qp4.drawChord(3, 5, 65, 65, 165 * 16, 135 * 16)
    path = QPainterPath()
    rect = QRect(4, 5, 70, 65)
    path.arcTo(rect, 0, 90 * 16)
    rect2 = QRect(9, -8, 75, 68)
    pathE = QPainterPath()
    pathE.arcTo(rect2, 0, 60 * 16)
    # pathE.addEllipse(-100, -100, 200, 200)
    pathR = QPainterPath()
    pathR.addRect(0, 0, 100, 100)

    qp4.drawPath(path - pathE)
    qp4.restore()


# 叶萼阴影
def leaf_mask(self):
    leaf_mask = QPainter(self)
    leaf_mask.setRenderHint(QPainter.Antialiasing)
    pen = QPen()
    pen.setWidth(2)  # 线宽
    pen.setColor(Qt.transparent)  # 画线颜色
    pen.setStyle(Qt.SolidLine)  # 线的类型，如实线、虚线等
    pen.setCapStyle(Qt.FlatCap)  # 线端点样式
    pen.setJoinStyle(Qt.RoundJoin)  # 线的连接点样式
    leaf_mask.setPen(pen)
    leaf_mask.scale(self.size, self.size)

    leaf_mask_brush = QBrush()
    leaf_mask_brush.setColor(QColor(0, 0, 0, 80))
    leaf_mask_brush.setStyle(Qt.SolidPattern)  # 填充样式
    leaf_mask.setBrush(leaf_mask_brush)
    leaf_mask.drawPolygon(
        QPolygon([QPoint(24, 14), QPoint(26, 16),
                  QPoint(26, 20), QPoint(33, 18),
                  QPoint(42, 19), QPoint(39, 15),
                  QPoint(43, 12), QPoint(32, 11),
                  QPoint(24, 14)]))


# 叶萼
def leaf(self):
    qp2 = QPainter(self)
    qp2.setRenderHint(QPainter.Antialiasing)
    pen = QPen()
    pen.setWidth(2)  # 线宽
    pen.setColor(Qt.white)  # 画线颜色
    pen.setStyle(Qt.SolidLine)  # 线的类型，如实线、虚线等
    pen.setCapStyle(Qt.FlatCap)  # 线端点样式
    pen.setJoinStyle(Qt.RoundJoin)  # 线的连接点样式
    qp2.setPen(pen)
    qp2.scale(self.size, self.size)

    brush2 = QBrush()
    brush2.setColor(QColor(40, 150, 0, 250))
    brush2.setStyle(Qt.SolidPattern)  # 填充样式
    qp2.setBrush(brush2)
    qp2.drawPolygon(
        QPolygon([QPoint(7, 18), QPoint(20, 19),
                  QPoint(18, 30), QPoint(33, 23),
                  QPoint(53, 27), QPoint(48, 15),
                  QPoint(59, 7), QPoint(40, 5),
                  QPoint(28, 1), QPoint(25, 9), QPoint(7, 18)]))


# 枝
def stick(self):
    qp3 = QPainter(self)
    qp3.setRenderHint(QPainter.Antialiasing)
    pen = QPen()
    pen.setWidth(2)  # 线宽
    pen.setColor(Qt.white)  # 画线颜色
    pen.setStyle(Qt.SolidLine)  # 线的类型，如实线、虚线等
    pen.setCapStyle(Qt.FlatCap)  # 线端点样式
    pen.setJoinStyle(Qt.RoundJoin)  # 线的连接点样式
    qp3.setPen(pen)
    qp3.scale(self.size, self.size)

    brush2 = QBrush()
    brush2.setColor(QColor(110, 68, 40, 250))
    brush2.setStyle(Qt.SolidPattern)  # 填充样式
    qp3.setBrush(brush2)
    qp3.drawPolygon(
        QPolygon([QPoint(36, 1), QPoint(31, 15),
                  QPoint(34, 16), QPoint(43, 0), QPoint(36, 1)]))


def word(self):
    if self.is_shownum & self.starttomato:
        painter = QPainter(self)
        painter.begin(self)
        # 设置画笔颜色
        painter.setPen(QColor(255, 255, 255))
        painter.scale(self.size, self.size)
        # 设置字体大小
        painter.setFont(QFont('SimSun', 12))
        # 设置要书写的内容
        self.text = str(round((1500000 - self.condition * 12500) / (1000 * 60)))
        if self.condition == 120:
            self.text = f"完成啦"
        rect = QRect(5, 10, 70, 65)
        painter.drawText(rect, Qt.AlignCenter, self.text)
        painter.end()
