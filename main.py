import os
import sys
import random
import configparser
import functools

from PySide6.QtCore import QPoint, QTimer, QRect, QUrl
from PySide6.QtGui import QPainter, QPen, Qt, QBrush, QPolygon, QAction, QIcon, QCursor, QColor, QFont, QPainterPath, \
    QDesktopServices, QActionGroup
import pic_rc
from PySide6.QtWidgets import QWidget, QApplication, QMenu, QSystemTrayIcon


class DesktopTomato(QWidget):
    def __init__(self, parent=None, **kwargs):
        super(DesktopTomato, self).__init__(parent)

        # 数据初始化
        self.init_data()
        # 窗体初始化
        self.init()
        # 托盘化初始
        self.initTray()
        # 静态加载
        self.initSet(9)
        self.set_size(str(self.size))

    # 初始化数据
    def init_data(self):
        # 标准初始化
        self.timeout_num = 0
        self.condition = 120
        self.is_follow_mouse = False
        self.starttomato = False

        # 读取配置
        config = configparser.ConfigParser()
        data = config.read('tomato.ini')
        # todo：初始化配置
        if data == []:
            config.add_section("base")
            config.set("base", "vibration", "1")
            config.set("base", "shownum", "0")
            config.set("base", "size", "1")
            config.write(open('tomato.ini', "w"))
            config = configparser.ConfigParser()
            config.read('tomato.ini')

        # 定义初始化
        self.is_vibration = bool(int(config['base']['vibration']))
        self.is_shownum = bool(int(config['base']['shownum']))
        self.size = float(config['base']['size'])

    # 窗体初始化
    def init(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.repaint()

    # 静态初始图加载
    def initSet(self, sign):
        self.resize(80 * self.size, 75 * self.size)
        # 调用自定义的setPosition
        self.setPosition(sign)
        self.show()

    # 果实
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
        rect = QRect(3, 5, 70, 65)
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
                      QPoint(59, 7), QPoint(39, 6),
                      QPoint(27, 1), QPoint(25, 9), QPoint(7, 18)]))

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
            QPolygon([QPoint(35, 1), QPoint(31, 15),
                      QPoint(34, 17), QPoint(43, 0), QPoint(35, 1)]))

    # 文字
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
            self.text = str(round((1500000 - self.condition * 12500) / (1000 * 60))) + f"分钟"
            if self.condition == 120:
                self.text = f"完成啦"
            rect = QRect(5, 10, 70, 65)
            painter.drawText(rect, Qt.AlignCenter, self.text)
            painter.end()

    # 绘图
    def paintEvent(self, e):
        self.tomato()
        self.leaf()
        self.leaf_mask()
        self.stick()
        self.tomato_mask()
        self.highlight()
        self.word()

    def clickAction(self):
        if self.condition < 120:
            self.condition += 1
            self.update()
            self.paintEvent(self)
            # todo:设置时间
            self.timer.singleShot(12500, self.clickAction)
            # self.timer.singleShot(25, self.clickAction)
            if self.condition == 120:
                self.tray_icon.setIcon(QIcon(os.path.join(':pic/icon1.ico')))
                self.timeout_num = 0
                self.timeOut()
                self.setWindowOpacity(1)

    # 到点儿
    def timeOut(self):
        if self.is_vibration:
            if self.timeout_num < 20:
                self.timeout_num += 1
                if (self.timeout_num % 2) == 0:
                    self.setPosition(1)
                else:
                    self.setPosition(2)
                self.update()
                self.paintEvent(self)
                self.timer.singleShot(50, self.timeOut)

    # 开始番茄钟
    def startTomatoClock(self):
        self.starttomato = True
        self.timer = QTimer()
        self.condition = -1
        self.clickAction()
        self.tray_icon.setIcon(QIcon(os.path.join(':pic/icon0.ico')))

    # 退出操作，关闭程序
    def quit(self):
        self.close()
        sys.exit()

    # 显示透明度-1
    def show_win(self):
        # setWindowOpacity（）设置窗体的透明度，通过调整窗体透明度实现的展示和隐藏
        self.setWindowOpacity(1)

    # 位置&抖动
    def setPosition(self, sign):
        # 抖动 norandom
        tomato_geo = self.geometry()
        if sign == 0:
            return self.move(tomato_geo.x(), tomato_geo.y())
        if sign == 1:
            return self.move(tomato_geo.x() + 3, tomato_geo.y() - 2)
        if sign == 2:
            return self.move(tomato_geo.x() - 3, tomato_geo.y() + 2)

        # 抖动 random
        # if sign == 1:
        #     return self.move(self.geometry().x() + random.randint(2, 5), self.geometry().y() - random.randint(2, 5))
        # if sign == 2:
        #     return self.move(self.geometry().x() - random.randint(2, 5), self.geometry().y() + random.randint(2, 5))

        screen_geo = self.screen().geometry()
        width = (screen_geo.width() - tomato_geo.width() - 100)
        height = (screen_geo.height() - tomato_geo.height() - 100)
        self.move(width, height)

    # 鼠标左键按下时, 将和鼠标位置绑定
    def mousePressEvent(self, event):
        # 更改状态为点击
        if event.button() == Qt.LeftButton:
            self.is_follow_mouse = True
        # globalPos() 事件触发点相对于桌面的位置
        # pos() 程序相对于桌面左上角的位置，实际是窗口的左上角坐标
        self.mouse_drag_pos = event.globalPosition().toPoint() - self.pos()
        event.accept()
        # 拖动时鼠标图形的设置
        self.setCursor(QCursor(Qt.ClosedHandCursor))
        screen_geo = self.geometry()

    # 鼠标移动时调用，实现随鼠标移动
    def mouseMoveEvent(self, event):
        # 如果鼠标左键按下，且处于绑定状态
        if Qt.LeftButton and self.is_follow_mouse:
            # 随鼠标进行移动
            self.move(event.globalPosition().toPoint() - self.mouse_drag_pos)
        event.accept()

    # 鼠标释放调用，取消绑定
    def mouseReleaseEvent(self, event):
        self.is_follow_mouse = False
        self.update()
        self.paintEvent(self)
        # 鼠标图形设置为箭头
        self.setCursor(QCursor(Qt.ArrowCursor))

    # 鼠标移进时调用
    def enterEvent(self, event):
        # 设置鼠标形状 Qt.ClosedHandCursor   非指向手
        self.setCursor(Qt.OpenHandCursor)

    # 右键点击交互
    def contextMenuEvent(self, event):
        # 定义菜单
        self.menu = QMenu(self)
        # 定义菜单项
        self.startTomato = self.menu.addAction("开始")
        self.hide = self.menu.addAction("隐藏")

        # 插入分隔符
        separator = QAction(self)
        separator.setSeparator(True)
        self.menu.addAction(separator)

        self.quitAction = self.menu.addAction("退出")

        # 使用exec_()方法显示菜单。从鼠标右键事件对象中获得当前坐标。mapToGlobal()方法把当前组件的相对坐标转换为窗口（window）的绝对坐标。
        action = self.menu.exec(self.mapToGlobal(event.pos()))
        # 点击事件为退出
        if action == self.startTomato:
            self.startTomatoClock()
        # 点击事件为退出
        if action == self.quitAction:
            sys.exit(app.exec())
        # 点击事件为隐藏
        if action == self.hide:
            # 通过设置透明度方式隐藏
            self.setWindowOpacity(0)

    # 托盘化设置
    def initTray(self):
        # 设置右键显示最小化的菜单项
        # 菜单项退出，点击后调用quit函数
        quit_action = QAction('退出', self, triggered=self.quit)
        # 设置这个点击选项的图片
        # quit_action.setIcon(QIcon(os.path.join(':pic/icon1.ico')))
        # 菜单项显示，点击后调用showing函数
        showing = QAction(u'显示', self, triggered=self.show_win)
        # showing.setIcon(QIcon(os.path.join(':pic/show.ico')))

        # 新建一个菜单项控件
        self.tray_icon_menu = QMenu(self)
        # 在菜单栏添加一个无子菜单的菜单项‘显示’
        self.tray_icon_menu.addAction(showing)
        # 在菜单栏添加一个无子菜单的菜单项‘退出’
        self.tray_icon_menu.addAction(quit_action)
        self.setting = self.tray_icon_menu.addMenu(u"设置")

        self.setsize = self.setting.addMenu(u"图标大小")
        self.ceui = QActionGroup(self, setExclusive=True)
        self.size_s = QAction('图标小', self, checkable=True)
        self.size_s.setStatusTip('图标小')
        self.size_s.triggered.connect(functools.partial(self.set_size, '0.8'))
        self.setsize.addAction(self.size_s)
        self.ceui.addAction(self.size_s)

        self.size_m = QAction('图标中', self, checkable=True)
        self.size_m.setStatusTip('图标中')
        self.size_m.triggered.connect(functools.partial(self.set_size, '1.0'))
        # self.size_m.setChecked(True)
        self.setsize.addAction(self.size_m)
        self.ceui.addAction(self.size_m)

        self.size_l = QAction('图标大', self, checkable=True)
        self.size_l.setStatusTip('图标大')
        self.size_l.triggered.connect(functools.partial(self.set_size, '1.2'))
        self.setsize.addAction(self.size_l)
        self.ceui.addAction(self.size_l)

        timeshow = QAction('显示倒计时', self, checkable=True)
        timeshow.setStatusTip('显示倒计时')
        timeshow.setChecked(self.is_shownum)
        timeshow.triggered.connect(self.show_timeNum)
        self.setting.addAction(timeshow)

        vibration = QAction('开启抖动', self, checkable=True)
        vibration.setStatusTip('开启抖动')
        vibration.setChecked(self.is_vibration)
        vibration.triggered.connect(self.set_vibration)
        self.setting.addAction(vibration)

        # 插入分隔符
        separator = QAction(self)
        separator.setSeparator(True)
        self.setting.addAction(separator)

        # todo:更新
        web = QAction(u'检查更新:1.1.1', self, triggered=self.show_web)
        self.setting.addAction(web)

        # QSystemTrayIcon类为应用程序在系统托盘中提供一个图标
        self.tray_icon = QSystemTrayIcon(self)
        # 设置托盘化图标
        self.tray_icon.setIcon(QIcon(os.path.join(':pic/icon0.ico')))
        # 设置托盘化菜单项
        self.tray_icon.setContextMenu(self.tray_icon_menu)
        # 展示
        self.tray_icon.show()

    # 打开更新网页
    def show_web(self):
        QDesktopServices.openUrl(QUrl("https://t.bilibili.com/731192047445213186"))

    # 显示倒计时
    def show_timeNum(self):
        config = configparser.ConfigParser()
        config.read('tomato.ini')
        self.is_shownum = not self.is_shownum
        if self.is_shownum:
            config['base']['shownum'] = '1'
        else:
            config['base']['shownum'] = '0'
        # 将config对象写入配置文件
        with open('tomato.ini', mode='w') as fp:
            config.write(fp)
        self.update()
        self.paintEvent(self)

    # 开关抖动
    def set_vibration(self):
        self.is_vibration = not self.is_vibration
        config = configparser.ConfigParser()
        config.read('tomato.ini')
        if self.is_vibration:
            config['base']['vibration'] = '1'
        else:
            config['base']['vibration'] = '0'
        # 将config对象写入配置文件
        with open('tomato.ini', mode='w') as fp:
            config.write(fp)
        self.update()
        self.paintEvent(self)

    def set_size(self, size: str):
        setnum = {'0.8': 'size_s', '1.0': 'size_m', '1.2': 'size_l'}
        self.size = float(size)
        eval(f'self.{setnum[size]}').setChecked(True)
        config = configparser.ConfigParser()
        config.read('tomato.ini')
        config['base']['size'] = size
        # 将config对象写入配置文件
        with open('tomato.ini', mode='w') as fp:
            config.write(fp)
        self.initSet(0)
        self.update()
        self.paintEvent(self)


if __name__ == '__main__':
    # 创建了一个QApplication对象，对象名为app，带两个参数argc,argv
    # 所有的应用必须创建一个应用（Application）对象。sys.argv参数是一个来自命令行的参数列表。
    app = QApplication(sys.argv)
    # 窗口组件初始化
    tomato = DesktopTomato()
    # 1. 进入时间循环；
    # 2. wait，直到响应app可能的输入；
    # 3. QT接收和处理用户及系统交代的事件（消息），并传递到各个窗口；
    # 4. 程序遇到exit()退出时，机会返回exec()的值。
    sys.exit(app.exec())
