# import screeninfo
# try:
#     screen = screeninfo.get_monitors()[1]
# except:
#     print('No third screen')
#
# print('yes')

# import random
# print(random.randint(5, 25))

# coding: utf-8
from PIL import ImageGrab
import numpy as np
import cv2

fps = 60
start = 1  # 延时录制
end = 7200  # 自动结束时间

curScreen = ImageGrab.grab()  # 获取屏幕对象
width, height = curScreen.size
# print(height, width)
video = cv2.VideoWriter(r'C:\Users\Administrator\Desktop\video.avi', cv2.VideoWriter_fourcc(*'XVID'), fps, (width, height))

imageNum = 0
while True:
    imageNum += 1
    captureImage = ImageGrab.grab()  # 抓取屏幕
    frame = cv2.cvtColor(np.array(captureImage), cv2.COLOR_RGB2BGR)

    # 显示无图像的窗口
    cv2.imshow('capturing', np.zeros((1, 255), np.uint8))

    # 控制窗口显示位置，方便通过按键方式退出
    # cv2.moveWindow('capturing', height - 100, width - 100)
    if imageNum > fps * start:
        video.write(frame)
    # 退出条件
    if cv2.waitKey(1) == ord('q') or imageNum > fps * end:
        break
video.release()
cv2.destroyAllWindows()