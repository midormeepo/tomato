import os
import sys
import about
import pic_rc
import Qpainter
import configparser
from PySide6 import QtCore
from functools import partial
from PySide6.QtCore import QTimer, QRect
from PySide6.QtGui import Qt, QAction, QIcon, QCursor, QActionGroup
from PySide6.QtWidgets import QWidget, QApplication, QMenu, QSystemTrayIcon, QPushButton, QLabel


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
        # 图标大小
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
        if data == []:
            config.add_section("base")
            config.set("base", "vibration", "1")
            config.set("base", "shownum", "0")
            config.set("base", "size", "1")
            config.set('base', 'language', '0')
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

    # 绘图
    def paintEvent(self, e):
        Qpainter.tomato(self)
        Qpainter.tomato(self)
        Qpainter.leaf(self)
        Qpainter.leaf_mask(self)
        Qpainter.stick(self)
        Qpainter.tomato_mask(self)
        Qpainter.highlight(self)
        Qpainter.word(self)

    def clickAction(self):
        if self.condition < 120:
            self.condition += 1
            self.update()
            self.paintEvent(self)
            # self.timer.singleShot(12500, self.clickAction)
            self.timer.singleShot(25, self.clickAction)
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
        self.startTomato = self.menu.addAction(self.tr("开始"))
        self.hide = self.menu.addAction(self.tr("隐藏"))

        # 插入分隔符
        separator = QAction(self)
        separator.setSeparator(True)
        self.menu.addAction(separator)

        self.quitAction = self.menu.addAction(self.tr("退出"))

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

        # 插入分隔符
        separator0 = QAction(self)
        separator0.setSeparator(True)

        quit_action = QAction(self.tr("退出"), self, triggered=self.quit)
        # 设置这个点击选项的图片
        # quit_action.setIcon(QIcon(os.path.join(':pic/icon1.ico')))
        # 菜单项显示，点击后调用showing函数
        showing = QAction(self.tr("显示"), self, triggered=self.show_win)
        # showing.setIcon(QIcon(os.path.join(':pic/show.ico')))

        # 新建一个菜单项控件
        self.tray_icon_menu = QMenu(self)

        self.setting = self.tray_icon_menu.addMenu(self.tr("设置"))
        # 在菜单栏添加一个无子菜单的菜单项‘显示’
        self.tray_icon_menu.addAction(showing)
        self.tray_icon_menu.addAction(separator0)
        # 在菜单栏添加一个无子菜单的菜单项‘退出’
        self.tray_icon_menu.addAction(quit_action)


        timeshow = QAction(self.tr("显示倒计时"), self, checkable=True)
        timeshow.setStatusTip(self.tr("显示倒计时"))
        timeshow.setChecked(self.is_shownum)
        timeshow.triggered.connect(self.show_timeNum)
        self.setting.addAction(timeshow)

        vibration = QAction(self.tr("开启抖动"), self, checkable=True)
        vibration.setStatusTip(self.tr("开启抖动"))
        vibration.setChecked(self.is_vibration)
        vibration.triggered.connect(self.set_vibration)
        self.setting.addAction(vibration)

        self.setsize = self.setting.addMenu(self.tr("图标大小"))
        self.ceui = QActionGroup(self, setExclusive=True)
        self.size_s = QAction(self.tr("图标小"), self, checkable=True)
        self.size_s.setStatusTip(self.tr("图标小"))
        self.size_s.triggered.connect(partial(self.set_size, '0.8'))
        self.setsize.addAction(self.size_s)
        self.ceui.addAction(self.size_s)

        self.size_m = QAction(self.tr("图标中"), self, checkable=True)
        self.size_m.setStatusTip(self.tr("图标中"))
        self.size_m.triggered.connect(partial(self.set_size, '1.0'))
        self.setsize.addAction(self.size_m)
        self.ceui.addAction(self.size_m)

        self.size_l = QAction(self.tr("图标大"), self, checkable=True)
        self.size_l.setStatusTip(self.tr("图标大"))
        self.size_l.triggered.connect(partial(self.set_size, '1.2'))
        self.setsize.addAction(self.size_l)
        self.ceui.addAction(self.size_l)

        self.setlanguage = self.setting.addMenu(self.tr("切换语言"))
        self.language_G = QActionGroup(self, setExclusive=True)
        self.zh = QAction("简体中文", self, checkable=True)
        self.zh.triggered.connect(partial(self.set_language, 'zh'))
        self.setlanguage.addAction(self.zh)
        self.language_G.addAction(self.zh)

        self.en = QAction("English", self, checkable=True)
        self.en.triggered.connect(partial(self.set_language, 'en'))
        self.setlanguage.addAction(self.en)
        self.language_G.addAction(self.en)

        # 插入分隔符
        separator = QAction(self)
        separator.setSeparator(True)
        self.setting.addAction(separator)

        web = QAction(self.tr("检查更新:1.1.1"), self, triggered=self.show_web)
        self.setting.addAction(web)

        # QSystemTrayIcon类为应用程序在系统托盘中提供一个图标
        self.tray_icon = QSystemTrayIcon(self)
        # 设置托盘化图标
        self.tray_icon.setIcon(QIcon(os.path.join(':pic/icon0.ico')))
        # 设置托盘化菜单项
        self.tray_icon.setContextMenu(self.tray_icon_menu)
        # 展示
        self.tray_icon.show()

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

    def set_language(self, lan):
        setnum = {'zh': '0', 'en': 'eng-chs.qm', '2': 'size_l'}
        config = configparser.ConfigParser()
        config.read('tomato.ini')
        config['base']['language'] = setnum[lan]
        # 将config对象写入配置文件
        with open('tomato.ini', mode='w') as fp:
            config.write(fp)
        self.update()
        self.paintEvent(self)

    def set_size(self, size: str):
        setnum = {'0.8': 'size_s', '1.0': 'size_m', '1.2': 'size_l'}
        self.size = float(size)
        try:
            eval(f'self.{setnum[size]}').setChecked(True)
        except:
            print(f'自定义大小：{size}')
        config = configparser.ConfigParser()
        config.read('tomato.ini')
        config['base']['size'] = size
        # 将config对象写入配置文件
        with open('tomato.ini', mode='w') as fp:
            config.write(fp)
        self.initSet(0)
        self.update()
        self.paintEvent(self)

    # 打开更新网页
    def show_web(self):
        # QDesktopServices.openUrl(QUrl("https://t.bilibili.com/731192047445213186"))
        s.show()

if __name__ == '__main__':
    # 创建了一个QApplication对象，对象名为app，带两个参数argc,argv
    # 所有的应用必须创建一个应用（Application）对象。sys.argv参数是一个来自命令行的参数列表。
    app = QApplication(sys.argv)
    # QtCore.QTextCodec.setCodecForTr(QtCore.QTextCodec.codecForName("UTF-8"))
    config = configparser.ConfigParser()
    config.read('tomato.ini')
    language = str(config['base']['language'])

    myappTranslator = QtCore.QTranslator()
    myappTranslator.load(language)
    app.installTranslator(myappTranslator)

    # 窗口组件初始化
    tomato = DesktopTomato()
    s = about.AboutWindow()
    s.setWindowTitle(tomato.tr("检查更新"))

    # 1. 进入时间循环；
    # 2. wait，直到响应app可能的输入；
    # 3. QT接收和处理用户及系统交代的事件（消息），并传递到各个窗口；
    # 4. 程序遇到exit()退出时，机会返回exec()的值。
    sys.exit(app.exec())
