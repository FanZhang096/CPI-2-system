import cv2
import sys
from camera1 import Camera
from window import Window

if __name__ == '__main__':
    # 实例化相机对象
    cam = Camera()
    # 生成窗体对象
    pro = Window('projector_1', 'projector_2', 1920, 1200)
    # 前两个参数是第一个窗体，后两个是第二个窗体
    pro.createwindow(800, 600)
    # 连投影仪运行这句话，不连就把1改成0，否则会报错 out of range
    pro.movewindow(1)
    # 前两个参数是一屏二屏标记的颜色，第三个参数是标记的宽度，最后两个参数 要和生成窗体对象的最后两个参数保持一致，如果想要二屏标记也是绿色就把（255,255,255）改成（0,255,0）
    pro.bindingwi((0, 255, 0), (0, 255, 0), 3, 1600, 1200)
    pro.nobiaotilan()
    # 创建跟踪器
    tracker_type = 'CSRT'
    tracker = cv2.TrackerCSRT_create()
    while True:
        # 读入第一帧
        frame = cam.run1()
        frame = cv2.flip(frame, 0)
        # print(frame.shape)
        pro.addimage(frame)
        pro.showimage()
        cv2.waitKey(1)
        pro.movebiaoji()
    # 定义一个bounding box
    # bbox = (287, 23, 86, 320)
        if pro.bbox != ():
            print(pro.bbox)
            # cv2.destroyAllWindows()
            break
# 用第一帧初始化
    ok = tracker.init(frame, pro.bbox)
    print('select over')

    while True:
        # cv2.imshow('1', pro.image8)
        # cv2.waitKey(0)
        frame = cam.run1()
        frame = cv2.flip(frame, 0)
        # pro.addimage(frame)
        # Start timer
        timer = cv2.getTickCount()
        # Update tracker
        ok, bbox = tracker.update(frame)
        # Cakculate FPS
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
        # Draw bonding box
        # 前两个参数调大小，后两个参数调位置,第五个参数调框的宽度
        pro.changeimage(550, 400, 245, 190, 5)
        if ok:
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            # cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
        else:
            cv2.putText(frame, "Tracking failed detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
        # 展示tracker类型
        cv2.putText(frame, tracker_type + "Tracker", (100, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)
        # 展示FPS
        cv2.putText(frame, "FPS:" + str(fps), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)
        # Result
        # cv2.imshow("Tracking", frame)
        pro.dong(int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3]))
        pro.addimage(frame)
        pro.showimage()
        # Exit
        k = cv2.waitKey(1) & 0xff
        if k == 27: break
