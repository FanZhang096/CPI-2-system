import cv2
import numpy as np
import mvsdk
from camera1 import Camera


class Image:
    def __init__(self):
        # 实例化相机
        self.cam = Camera()
        self.n = 0
        self.image = np.zeros([1200, 1920, 3], np.uint8)
        self.image1 = np.zeros([1200, 1920, 3], np.uint8)

    def enhance_bri(self, m):
        self.n = self.n + 1
        frame = self.cam.run1()
        # frame1 = cv2.flip(frame, -1)
        # frame = cv2.resize(frame, (800, 600))
        # frame1 = cv2.GaussianBlur(frame1, (5, 5), 1.5)
        self.image = cv2.add(frame, self.image)
        if self.n % m == 0:
            self.n = 0
            self.image1 = self.image
            self.image = np.zeros([1200, 1920, 3], np.uint8)
            # 裁剪相机拍到的图 左右各裁剪一部分宽度 高度不变
            # self.image2 = self.image1[:, 170:1750]
            # print('相机图尺寸', self.image2.shape)
            # self.image2[598:600, :] = [255, 255, 255]
            # self.image2[:, 1580 // 2 - 2:1580 // 2] = [255, 255, 255]
            return self.image1
        # print('self.n', self.n)

    def close_camera(self):
        mvsdk.CameraUnInit(self.cam.hCamera)


image = Image()
n = 0
m = 3
while 1:
    n = n + 1
    image1 = image.enhance_bri(m)
    cv2.namedWindow('1')
    cv2.resizeWindow('1',(800,600))
    if n % m == 0:
        n = 0
        cv2.imshow('1', image1)
        cv2.waitKey(1000)


















