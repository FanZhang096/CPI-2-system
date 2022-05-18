import os
import instructionswindow
import qdarkgraystyle
from camera_thread import ThreadImg
from qtdesignerUI import Ui_Form
from PyQt5.QtWidgets import QWidget, QToolTip, QMessageBox
from PyQt5.QtCore import pyqtSignal, QTimer, QCoreApplication, QRect
from PyQt5.QtGui import QFont


class MyMainWindow(QWidget, Ui_Form):
    # 在init之前先声明自己定义的信号
    PointsSingnal = pyqtSignal(list, int)
    BoundingBoxSingal = pyqtSignal(list, list)
    ClearSingal = pyqtSignal()
    Camera_thread_False_mode2_Singal = pyqtSignal()
    Camera_thread_True_mode2_Singal = pyqtSignal()
    ThreadImg_break_Singal = pyqtSignal()
    Emit_parameter_Singal = pyqtSignal(int, int, int, int, int, int, int)
    Set_number2_Singal = pyqtSignal()
    Set_number3_Singal = pyqtSignal()

    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)

        # 这块是初始化opencv画线的
        self.number = 0
        self.list1 = []
        self.list3 = []
        self.list4 = []
        # 控制不同的按钮，是否要让camera_thread开始运行
        self.start_mode = False
        # 如果不写下面这个init函数，就不需要下面这句话
        self.init()
        # 设置标题
        self.setWindowTitle("Tele-mentoring")
        # 设置对象名称
        self.setObjectName("MainWindow")
        # 设置窗口背景颜色
        # self.setStyleSheet("#MainWindow{background-color: gray}")
        self.setStyleSheet(qdarkgraystyle.load_stylesheet())
        # 锁定窗口大小
        self.setFixedSize(self.width(), self.height())

        self._translate = QCoreApplication.translate

    def init(self):
        # 这个函数里面写信号与槽函数的连接,label和鼠标事件的连接
        # 鼠标事件
        self.label_show_camera.setMouseTracking(True)
        # 气泡
        QToolTip.setFont(QFont("SansSerif", 12))
        self.instructionButton.setToolTip("Click to view detailed instructions")
        # QToolTip.setFont(QFont("SansSerif", 12))
        # self.real_label.setToolTip("左键单击开始按钮开始操作，按住鼠标左键移动可以画出注释，左键单击橡皮按钮清除标记")
        QToolTip.setFont(QFont("SansSerif", 12))
        self.real_start_button.setToolTip("Click to start")
        QToolTip.setFont(QFont("SansSerif", 12))
        self.real_clear_button.setToolTip("Click to clear annotations")

        QToolTip.setFont(QFont("SansSerif", 12))
        self.save_parameter_button.setToolTip("Click to save co-axial parameters")

        # 类的实例化及绑定
        self.thread1 = ThreadImg()

        # 创建窗体
        self.thread1.create_window(800, 600)
        self.thread1.move_window(1)
        self.thread1.full_screen()

        # 连接信号
        self.thread1.QImgSingnal.connect(self.show_image)
        self.thread1.QpointsSingal.connect(self.send_points)

        # 连接传给thread1的槽函数
        self.PointsSingnal.connect(self.thread1.receivepoints)
        self.ClearSingal.connect(self.thread1.clearline)
        self.Set_number2_Singal.connect(self.thread1.set_number2)
        self.Set_number3_Singal.connect(self.thread1.set_number3)
        self.BoundingBoxSingal.connect(self.thread1.list34)
        # button的connect绑定函数
        self.real_start_button.clicked.connect(self.start1)
        self.real_start_button.clicked.connect(self.get_parameter)
        self.real_clear_button.clicked.connect(self.clear)
        self.save_parameter_button.clicked.connect(self.save_parameter)
        self.real_shizi_button.clicked.connect(self.set_number2)
        self.track_start_button.clicked.connect(self.set_number3)

        # 将参数传给camera_thread这个类
        self.Emit_parameter_Singal.connect(self.thread1.get_parameter)

        # 初始化一个计时器，不停地发送参数给camera
        self.time = QTimer()
        self.time.timeout.connect(self.emit_parameter)

    def set_number2(self):
        self.Set_number2_Singal.emit()

    def set_number3(self):
        self.Set_number3_Singal.emit()

    # 这部分是real-time annotation 的函数
    def start1(self):
        self.time.start(10)
        if not self.start_mode:
            self.start_mode = True
            self.thread1.start()

    def clear(self):
        self.ClearSingal.emit()

    # 这部分是给QThread发送坐标的函数
    def send_points(self):
        self.PointsSingnal.emit(self.list1, self.number)
        # print('send')

    # 这部分显示图像
    def show_image(self, Qpix):
        self.label_show_camera.setPixmap(Qpix)  # 往显示视频的Label里 显示QImage
        # self.label_scene.setText("Record image")

    # 鼠标事件
    def mouseMoveEvent(self, event):
        self.s2 = event.windowPos()        # 不写下面这句话，只有按住左键的时候才会获取值
        # self.setMouseTracking(True)
        if int(self.s2.x()) < 1536 and int(self.s2.y()) < 960:
            self.number = self.number + 1
            self.list1.append((int(1.25*self.s2.x()), int(1.25*self.s2.y())))
            # print(self.list1)

    def mousePressEvent(self, event):
        self.s1 = event.windowPos()
        if int(self.s1.x()) < 1536 and int(self.s1.y()) < 960:
            self.number = self.number + 1
            self.list1.append((int(1.25*self.s1.x()), int(1.25*self.s1.y())))

    def mouseReleaseEvent(self, event):
        for (x, y) in self.list1:
            self.list3.append(x)
            self.list4.append(y)
        self.BoundingBoxSingal.emit(self.list3, self.list4)
        self.list1 = []
        self.list3 = []
        self.list4 = []
        self.number = 0

    # QImage 转 numpy
    # def convertQImageToMat(self, p):
    #     '''  Converts a QImage into an opencv MAT format  '''
    #     p = p.convertToFormat(3)
    #     ptr = p.bits()
    #     ptr.setsize(p.byteCount())
    #     arr = np.array(ptr).reshape(p.height(), p.width(), 1)
    #     return arr

    # 这部分代码用于调同轴
    def emit_parameter(self):
        width = self.width_lineEdit.text()
        height = self.height_lineEdit.text()
        x = self.x_lineEdit.text()
        y = self.y_lineEdit.text()
        thickness = self.thickness_lineEdit.text()
        camera_width_cut = self.camera_width_lineEdit.text()
        camera_height_cut = self.camera_height_lineEdit.text()
        try:
            width = int(width)
            height = int(height)
            x = int(x)
            y = int(y)
            thickness = int(thickness)
            camera_width_cut = int(camera_width_cut)
            camera_height_cut = int(camera_height_cut)
        except: pass
        else:
            if width > 0 and height > 0 and x > 0 and y > 0 and thickness > 0 and camera_width_cut % 5 == 0 and camera_height_cut % 5 == 0:
                self.Emit_parameter_Singal.emit(width, height, x, y, thickness, camera_width_cut, camera_height_cut)
                width = int((1920 - 2*camera_width_cut) / 1.25)
                height = int((1200 - 2*camera_height_cut) / 1.25)
                self.label_show_camera.setGeometry(QRect(0, 0, width, height))
            else:
                pass

    def get_parameter(self):
        filename = 'coaxial.txt'
        list1 = []
        with open(filename, 'r') as file_to_read:
            while True:
                line = file_to_read.readline()
                list1.append(line.strip('\n'))
                if not line:
                    break
        # 调同轴用的参数 475, 365, 223, 408, 10
        self.width_lineEdit.setText('%s' % int(list1[0]))
        self.height_lineEdit.setText('%s' % int(list1[1]))
        self.x_lineEdit.setText('%s' % int(list1[2]))
        self.y_lineEdit.setText('%s' % int(list1[3]))
        self.thickness_lineEdit.setText('%s' % int(list1[4]))
        self.camera_width_lineEdit.setText('%s' % int(list1[5]))
        self.camera_height_lineEdit.setText('%s' % int(list1[6]))

    def save_parameter(self):
        width = self.width_lineEdit.text()
        height = self.height_lineEdit.text()
        x = self.x_lineEdit.text()
        y = self.y_lineEdit.text()
        thickness = self.thickness_lineEdit.text()
        camera_width_cut = self.camera_width_lineEdit.text()
        camera_height_cut = self.camera_height_lineEdit.text()
        l = ['%s' % width, '\n%s' % height, '\n%s' % x, '\n%s' % y, '\n%s' % thickness, '\n%s' % camera_width_cut, '\n%s' % camera_height_cut]
        f = open('coaxial.txt', 'w')
        f.writelines(l)
        self.coxial_textEdit.setHtml(self._translate("Form",
                                                "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                "p, li { white-space: pre-wrap; }\n"
                                                "</style></head><body style=\" font-family:\'Arial\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
                                                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Coaxial parameters saved</p></body></html>"))

    def closeEvent(self, event):
        """
        对MainWindow的函数closeEvent进行重构
        退出软件时结束所有进程
        :param event:
        :return:
        """
        reply = QMessageBox.question(self,
                                               'Tele-mentoring',
                                               "Are you sure to exit？",
                                               QMessageBox.Yes | QMessageBox.No,
                                               QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
            os.exit(0)
        else:
            event.ignore()


# 这个类是用于显示要说明的内容，是按instructions之后弹出来的窗口
class InstructionsWindow(QWidget, instructionswindow.Ui_Form):
    def __init__(self, parent=None):
        super(InstructionsWindow, self).__init__(parent)
        self.setupUi(self)
        # 设置标题
        self.setWindowTitle("Instructions")
        # 设置窗口背景颜色
        self.setStyleSheet("#MainWindow{background-color: gray}")

    def show_w2(self):
        self.show()

