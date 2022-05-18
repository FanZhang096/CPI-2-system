import os
import cv2
import numpy as np
from camera1 import Camera
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage, QFont, QPixmap
import copy
import screeninfo
import time

'''

self.image1 :存一屏标记
self.image_annotation_1 :存二屏标记
self.image :混合了相机的图和一屏的标记
self.image3 :二屏生成的一幅全黑的图，铺满整个二屏
self.image5 :为了调同轴，将image2缩放一下，然后把self.image5赋值给self.image3的一部分

'''


class ThreadImg(QThread):
    QImgSingnal = pyqtSignal(QPixmap)
    QpointsSingal = pyqtSignal()

    def __init__(self):
        super(ThreadImg, self).__init__()
        self.cam = Camera()
        # list and number are used for cv2.line
        self.list = []
        self.number = 0
        self.list3 = []
        self.list4 = []
        # 确定是否需要调出来十字框
        self.number2 = 0
        # 确定是否需要运行追踪算法
        self.number3 = 1
        self.bbox = ()
        # 一屏存标记的图
        self.image1 = np.zeros([1200, 1920, 3], np.uint8)
        # 二屏储存标记的图
        self.image2 = np.zeros([1200, 1920, 3], np.uint8)

        # 调同轴,怕刚开始运行程序，数据还没传过来
        self.width = 475
        self.thickness = 10
        self.height = 365
        self.x1 = 223
        self.y1 = 408
        self.camera_width_cut = 0
        self.camera_height_cut = 0

        # 创建跟踪器
        self.tracker_type = 'CSRT'
        self.tracker = cv2.TrackerCSRT_create()

    def run(self):
        while 1:
            if self.number3:
                self.Rawimg = self.cam.run1()
                self.Rawimg = cv2.flip(self.Rawimg, 0)
                self.Rawimg = cv2.flip(self.Rawimg, 1)
                if self.number2:
                    # 相机图加个十字线
                    self.Rawimg[598:600, :] = [255, 255, 255]
                    self.Rawimg[:, 958:960] = [255, 255, 255]
                    # 二屏加个十字线
                    self.image2[598:600, :] = [255, 255, 255]
                    self.image2[:, 958:960] = [255, 255, 255]
                    # self.image2[:, :] = [255, 255, 255]

                # 重新缩放两张标记图
                self.Rawimg1 = self.Rawimg[self.camera_height_cut:1200 - self.camera_height_cut, self.camera_width_cut:1920 - self.camera_width_cut]
                self.image1_gai = self.image1[self.camera_height_cut:1200 - self.camera_height_cut, self.camera_width_cut:1920 - self.camera_width_cut]
                self.image2_gai = self.image2[self.camera_height_cut:1920 - self.camera_height_cut, self.camera_width_cut:1920 - self.camera_width_cut]
                # 画线
                self.draw()
                # 混合相机和一屏的标记
                self.image_gai = cv2.add(self.Rawimg1, self.image1_gai)
                # print('图像大小是', self.image_gai.shape)
                # 显示二屏的图
                self.change_img(10)
                # openCV格式的图, 把读到的帧的大小重新设置为 1280*960
                width1 = int((1920 - 2*self.camera_width_cut) / 1.25)
                height1 = int((1200 - 2*self.camera_height_cut) / 1.25)
                # print('width height is ', width1, height1)
                self.show = cv2.resize(self.image_gai, (width1, height1))
                # self.show = cv2.resize(self.Rawimg1, (1536, 960))
                # 视频色彩转换回RGB，这样才是现实的颜色
                show = cv2.cvtColor(self.show, cv2.COLOR_BGR2RGB)
                # 把读取到的视频数据变成QImage形式
                showImage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)
                self.pix = QPixmap.fromImage(showImage)
                self.QImgSingnal.emit(self.pix)
                self.QpointsSingal.emit()
            else:
                print('start select ROI')
                while True:
                    self.Rawimg = self.cam.run1()
                    self.Rawimg = cv2.flip(self.Rawimg, 0)
                    self.Rawimg = cv2.flip(self.Rawimg, 1)
                    if self.number2:
                        # 相机图加个十字线
                        self.Rawimg[598:600, :] = [255, 255, 255]
                        self.Rawimg[:, 958:960] = [255, 255, 255]
                        # 二屏加个十字线
                        self.image2[598:600, :] = [255, 255, 255]
                        self.image2[:, 958:960] = [255, 255, 255]
                    # 重新缩放两张标记图
                    self.Rawimg1 = self.Rawimg[self.camera_height_cut:1200 - self.camera_height_cut,
                                   self.camera_width_cut:1920 - self.camera_width_cut]
                    self.image1_gai = self.image1[self.camera_height_cut:1200 - self.camera_height_cut,
                                      self.camera_width_cut:1920 - self.camera_width_cut]
                    self.image2_gai = self.image2[self.camera_height_cut:1920 - self.camera_height_cut,
                                      self.camera_width_cut:1920 - self.camera_width_cut]
                    # 画线
                    self.draw()
                    # 混合相机和一屏的标记
                    self.image_gai = cv2.add(self.Rawimg1, self.image1_gai)
                    # print('图像大小是', self.image_gai.shape)
                    # 显示二屏的图
                    self.change_img(10)
                    # openCV格式的图, 把读到的帧的大小重新设置为 1280*960
                    width1 = int((1920 - 2 * self.camera_width_cut) / 1.25)
                    height1 = int((1200 - 2 * self.camera_height_cut) / 1.25)
                    # print('width height is ', width1, height1)
                    self.show = cv2.resize(self.image_gai, (width1, height1))
                    # self.show = cv2.resize(self.Rawimg1, (1536, 960))
                    # 视频色彩转换回RGB，这样才是现实的颜色
                    show = cv2.cvtColor(self.show, cv2.COLOR_BGR2RGB)
                    # 把读取到的视频数据变成QImage形式
                    showImage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)
                    self.pix = QPixmap.fromImage(showImage)
                    self.QImgSingnal.emit(self.pix)
                    self.QpointsSingal.emit()
                    self.movebiaoji()
                    if self.bbox != ():
                        print('bbox is ', self.bbox)
                        break
                    # 用第一帧初始化
                self.ok = self.tracker.init(self.Rawimg1, self.bbox)
                print('select over')
                while True:
                    self.Rawimg = self.cam.run1()
                    self.Rawimg = cv2.flip(self.Rawimg, 0)
                    self.Rawimg = cv2.flip(self.Rawimg, 1)
                    # 重新缩放两张标记图
                    self.Rawimg1 = self.Rawimg[self.camera_height_cut:1200 - self.camera_height_cut,
                                   self.camera_width_cut:1920 - self.camera_width_cut]
                    self.image1_gai = self.image1[self.camera_height_cut:1200 - self.camera_height_cut,
                                      self.camera_width_cut:1920 - self.camera_width_cut]
                    self.image2_gai = self.image2[self.camera_height_cut:1920 - self.camera_height_cut,
                                      self.camera_width_cut:1920 - self.camera_width_cut]
                    # Update tracker
                    self.ok, self.bbox = self.tracker.update(self.Rawimg1)
                    if self.ok:
                        self.p1 = (int(self.bbox[0]), int(self.bbox[1]))
                        self.p2 = (int(self.bbox[0] + self.bbox[2]), int(self.bbox[1] + self.bbox[3]))
                    self.dong(int(self.bbox[0]), int(self.bbox[1]), int(self.bbox[2]), int(self.bbox[3]))
                    # 混合相机和一屏的标记
                    self.image_gai = cv2.add(self.Rawimg1, self.image1_gai)
                    # print('图像大小是', self.image_gai.shape)
                    # 显示二屏的图
                    self.change_img(10)
                    # openCV格式的图, 把读到的帧的大小重新设置为 1280*960
                    width1 = int((1920 - 2 * self.camera_width_cut) / 1.25)
                    height1 = int((1200 - 2 * self.camera_height_cut) / 1.25)
                    # print('width height is ', width1, height1)
                    self.show = cv2.resize(self.image_gai, (width1, height1))
                    # self.show = cv2.resize(self.Rawimg1, (1536, 960))
                    # 视频色彩转换回RGB，这样才是现实的颜色
                    show = cv2.cvtColor(self.show, cv2.COLOR_BGR2RGB)
                    # 把读取到的视频数据变成QImage形式
                    showImage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)
                    self.pix = QPixmap.fromImage(showImage)
                    self.QImgSingnal.emit(self.pix)
                    self.QpointsSingal.emit()

    def receivepoints(self, list1, number):
        self.list = list1
        self.number = number

    @ staticmethod
    def create_window(width, height):
        cv2.namedWindow('screen2', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('screen2', width, height)

    def move_window(self, id):
        screen_id = id
        screen = screeninfo.get_monitors()[screen_id]
        width, height = screen.width, screen.height
        print('width,height are ', width, height)
        cv2.moveWindow('screen2', screen.x, screen.y)
        self.screen_width = width
        self.screen_height = height
        # 全黑的一幅图
        self.image3 = np.zeros([height, width, 3], np.uint8)

    @ staticmethod
    def full_screen():
        cv2.setWindowProperty('screen2', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    def draw(self):
        # cv2.waitKey(1)
        if len(self.list) >= 2 :
            for i in range(1, self.number - 1, 1):
                cv2.line(self.image1_gai, self.list[i-1], self.list[i], (0, 255, 0), thickness=self.thickness)
                cv2.line(self.image2_gai, self.list[i - 1], self.list[i], (0, 255, 0), thickness=self.thickness-1)
                # print('line')

    def change_img(self, z):
        # self.image5是用来调同轴的
        self.image5 = cv2.resize(self.image2_gai, (self.width, self.height))
        # self.image5 = cv2.flip(self.image5, 2)
        self.image5 = cv2.flip(self.image5, 0)
        self.image3[self.x1:self.x1 + self.height, self.y1:self.y1 + self.width] = self.image5
        # 加框
        self.image3[self.x1 - 1 - z:self.x1 - 1, self.y1 - 1:self.y1 + 1 + self.width] = [0, 255, 0]
        self.image3[self.x1 + self.height + 1:self.x1 + self.height + 1 + z, self.y1 - 1:self.y1 + 1 + self.width] = [0, 255, 0]
        self.image3[self.x1 - z - 1:self.x1 + self.height + z + 1, self.y1 - 1 - z:self.y1 - 1] = [0, 255, 0]
        self.image3[self.x1 - z - 1:self.x1 + self.height + z + 1, self.y1 + self.width + 1:self.y1 + self.width + 1 + z] = [0, 255, 0]
        cv2.imshow('screen2', self.image3)
        self.image3[:, :] = [0, 0, 0]

    def get_parameter(self, width, height, x, y, thickness, camera_width_cut, camera_height_cut):
        # 调同轴用的参数 475, 365, 223, 408, 10
            self.width = width
            self.height = height
            self.x1 = x
            self.y1 = y
            self.thickness = thickness
            self.camera_width_cut = camera_width_cut
            self.camera_height_cut = camera_height_cut

    def clearline(self):
        self.image1 = np.zeros([1200, 1920, 3], np.uint8)
        self.image2 = np.zeros([1200, 1920, 3], np.uint8)

    def set_parameter(self):
        filename = 'coaxial.txt'
        list1 = []
        with open(filename, 'r') as file_to_read:
            while True:
                line = file_to_read.readline()
                list1.append(line.strip('\n'))
                if not line:
                    break
        # 调同轴用的参数 475, 365, 223, 408, 10
        self.width = int(list1[0])
        self.height = int(list1[1])
        self.x1 = int(list1[2])
        self.y1 = int(list1[3])
        self.thickness = int(list1[4])

    def set_number2(self):
        self.number2 = not self.number2
        if self.number2 == 0:
            self.image2[598:600, :] = [0, 0, 0]
            self.image2[:, 958:960] = [0, 0, 0]

    def set_number3(self):
        self.number3 = not self.number3

    def list34(self, list3, list4):
        if self.number3 == 0:
            self.list3 = list3
            self.list4 = list4
            # print('list3 is ', self.list3)
        else:
            pass
        # if self.number3 == 0:
        #     print('list3 is ', list3)

    def movebiaoji(self):
        if self.list3:
            self.list3.sort()
            self.list4.sort()
            # print(self.list3[0], self.list3[-1])
            self.image1_gai[:, :] = [0, 0, 0]
            self.image2_gai[:, :] = [0, 0, 0]
            center_x = int(self.list3[0]+(self.list3[-1] - self.list3[0] )/2)
            center_y = int(self.list4[0]+(self.list4[-1] - self.list4[0] )/2)
            r = min(int(self.list3[-1] - self.list3[0]),int(self.list4[-1] - self.list4[0]))
            # print(center_x,center_y,r)
            cv2.circle(self.image1_gai, (center_x, center_y), radius=r//2+3, color=(0, 255, 0),thickness = 15)
            cv2.circle(self.image2_gai, (center_x, center_y), radius=r // 2 + 3, color=(0, 255, 0), thickness=15)
            # bbox = (x,y,w,h)-
            self.bbox = (int(self.list3[0] - 5), int(self.list4[0] - 5), int(self.list3[-1] - self.list3[0] + 5),
                         int(self.list4[-1] - self.list4[0] + 5))
            self.image1_gai_copy = copy.copy(
                self.image1_gai[int(self.list4[0] - 15):int(self.list4[-1]+15), int(self.list3[0] - 15):int(self.list3[-1]+15)])
            self.image2_gai_copy = copy.copy(
                self.image2_gai[int(self.list4[0] - 15):int(self.list4[-1]+15), int(self.list3[0] - 15):int(self.list3[-1]+15)])
            cv2.imshow('1', self.image1_gai)
            cv2.imshow('2',self.image1_gai_copy)
            cv2.waitKey(0)
            # print(self.bbox)
            self.list3 = []
            self.list4 = []
        else:
            pass

    def dong(self, x, y, w, h):
        self.image1_gai[:, :] = [0, 0, 0]
        self.image2_gai[:, :] = [0, 0, 0]
        dst1 = cv2.resize(self.image1_gai_copy, (w, h))
        dst2 = cv2.resize(self.image2_gai_copy, (w, h))
        self.image1_gai[y:y + h, x:x + w] = dst1
        self.image2_gai[y:y + h, x:x + w] = dst2









