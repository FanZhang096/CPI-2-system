# coding=utf-8
import cv2
import numpy as np
import mvsdk
import time
import copy


class Camera:
    def __init__(self):
        # 枚举相机
        DevList = mvsdk.CameraEnumerateDevice()
        self.nDev = len(DevList)
        if self.nDev < 1:
            print("No camera was found!")
            return

        self.DevInfo = DevList[0]
        print(self.DevInfo)

        # 打开相机
        self.hCamera = 0
        try:
            self.hCamera = mvsdk.CameraInit(self.DevInfo, -1, -1)
        except mvsdk.CameraException as e:
            print("CameraInit Failed({}): {}".format(e.error_code, e.message))
            return

        # 获取相机特性描述
        self.cap = mvsdk.CameraGetCapability(self.hCamera)

        # 判断是黑白相机还是彩色相机
        self.monoCamera = (self.cap.sIspCapacity.bMonoSensor != 0)

        # 黑白相机让ISP直接输出MONO数据，而不是扩展成R=G=B的24位灰度
        if self.monoCamera:
            mvsdk.CameraSetIspOutFormat(self.hCamera, mvsdk.CAMERA_MEDIA_TYPE_MONO8)

        # 相机模式切换  连续采集0，软触发1，硬触发2
        # mvsdk.CameraSetTriggerMode(self.hCamera, 0)
        #
        # mvsdk.CameraGetTriggerMode(self.hCamera)

        # 设置并获取硬触发信号种类  0上升沿触发 1下降沿 2高电平 3低电平
        # mvsdk.CameraSetExtTrigSignalType(self.hCamera, 1)
        #
        # mvsdk.CameraGetExtTrigSignalType(self.hCamera)

        # 设置并获取相机外触发模式下的触发延迟时间,单位是微秒 当硬触发信号来临后，经过指定的延时，再开始采集图像。
        # mvsdk.CameraSetTriggerDelayTime(self.hCamera, 10)
        #
        # mvsdk.CameraGetTriggerDelayTime(self.hCamera)

        # 另一种设置外触发信号延迟时间的函数
        # mvsdk.CameraSetExtTrigDelayTime(hCamera, 0)

        # mvsdk.CameraGetExtTrigDelayTime(hCamera)

        # 设置触发模式下  一次触发的帧数 默认为1帧
        # mvsdk.CameraSetTriggerCount(hCamera, 1)

        # mvsdk.CameraGetTriggerCount(hCamera)

        # 手动曝光 曝光时间3ms
        # mvsdk.CameraSetAeState(self.hCamera, 0)
        # mvsdk.CameraSetExposureTime(self.hCamera, 2 * 1000)

        # 设置增益，获得增益
        # mvsdk.CameraSetAnalogGain(self.hCamera, 2)
        # mvsdk.CameraGetAnalogGain(self.hCamera)

        # 让SDK内部取图线程开始工作
        mvsdk.CameraPlay(self.hCamera)

        # 计算RGB buffer所需的大小，这里直接按照相机的最大分辨率来分配
        self.FrameBufferSize = self.cap.sResolutionRange.iWidthMax * self.cap.sResolutionRange.iHeightMax *\
                               (1 if self.monoCamera else 3)

        # 设置相机的分辨率，外触发需要调至800*600居中裁剪
        # mvsdk.CameraSetImageResolution(self.hCamera, mvsdk.CameraCustomizeResolution(self.hCamera))

        # 分配RGB buffer，用来存放ISP输出的图像
        # 备注：从相机传输到PC端的是RAW数据，在PC端通过软件ISP转为RGB数据（如果是黑白相机就不需要转换格式，但是ISP还有其它处理，所以也需要分配这个buffer）
        self.pFrameBuffer = mvsdk.CameraAlignMalloc(self.FrameBufferSize, 16)

    def run1(self):
        try:

            self.pRawData, self.FrameHead = mvsdk.CameraGetImageBuffer(self.hCamera, 200)
            mvsdk.CameraImageProcess(self.hCamera, self.pRawData, self.pFrameBuffer, self.FrameHead)
            mvsdk.CameraReleaseImageBuffer(self.hCamera, self.pRawData)

            # 此时图片已经存储在pFrameBuffer中，对于彩色相机pFrameBuffer=RGB数据，黑白相机pFrameBuffer=8位灰度数据
            # 把pFrameBuffer转换成opencv的图像格式以进行后续算法处理
            self.frame_data = (mvsdk.c_ubyte * self.FrameHead.uBytes).from_address(self.pFrameBuffer)
            self.frame = np.frombuffer(self.frame_data, dtype=np.uint8)
            self.frame = self.frame.reshape((self.FrameHead.iHeight, self.FrameHead.iWidth,1 if self.FrameHead.uiMediaType == mvsdk.CAMERA_MEDIA_TYPE_MONO8 else 3))

            return self.frame
        except mvsdk.CameraException as e:
            if e.error_code != mvsdk.CAMERA_STATUS_TIME_OUT:
                print("CameraGetImageBuffer failed({}): {}".format(e.error_code, e.message))

        # 释放帧缓存
        mvsdk.CameraAlignFree(self.pFrameBuffer)

    def baipingheng(self):
        mvsdk.CameraSetOnceWB(self.hCamera)






