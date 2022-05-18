import cv2
import screeninfo
import numpy as np
import copy
import datetime


'''

1.为什么要用Image3 
因为如果
	def addimage(self,image4):
		self.image1 = cv2.add(image4,self.image1)
		self.image1_copy = copy.copy(self.image1)
	image1会不断地叠加，循环中第二次运行 addimage的时候，输入的self.image1就不是纯黑的图了
	而是混合了一帧相机的图，所以要用 image3 作为初始的图.
	
2.为什么要show一下 image3 在show 一下 image1
第一点： 先show image3 在 show image1 这样image1 会覆盖image3 看到的还是image1
第二点： cv2.circle(self.image3, (x, y), 4,color1, -1)要在循环中不断刷新image3才能保证
画出的东西显示出来， 虽然self.image1 = cv2.add(image4,self.image3) image1里面混了image3
image1不断地在刷新，但是仍然看不到做的标记 所以每次show image1 之前需要先show 一下image3.

3.image1 的作用只是显示相机的照片image4 画线 擦线绑定的都是image3 

4.相机拍到的是Image4,和相机混合，在一屏储存标记的是image3,image2是在二屏最开始画线的图，image1是混合了image3和image4的图,
image5是二屏全屏显示的那个黑色图，将想要的东西赋值给image5的一部分就可以了.self.image6是调同轴用的 把二屏框内全黑的部分变成相机拍到
的图 这样容易看相机投影仪视场是不是重合

'''


class Window:
	def __init__(self, windowname1, windowname2, width, height):
		self.windowname1, self.windowname2 = windowname1, windowname2
		self.image1 = np.zeros([height, width, 3], np.uint8)
		self.image2 = np.zeros([height, width, 3], np.uint8)
		self.image3 = np.zeros([height, width, 3], np.uint8)
		self.image4 = np.zeros([height, width, 3], np.uint8)
		self.image5 = np.zeros([height, width, 3], np.uint8)
		self.image6 = np.zeros([height, width, 3], np.uint8)
		self.image7 = np.zeros([height, width, 3], np.uint8)
		self.image8 = np.zeros([height, width, 3], np.uint8)
		self.image2_copy = np.zeros([height, width, 3], np.uint8)
		self.image3_copy = np.zeros([height, width, 3], np.uint8)
		self.mode = True
		self.drawing = False
		self.number = 0
		self.list1 = []
		self.list2 = []
		self.list3 = []
		self.list4 = []
		self.bbox = ()

	def createwindow(self, width, height):
		cv2.namedWindow(self.windowname1, cv2.WINDOW_NORMAL)
		cv2.resizeWindow(self.windowname1, width, height)
		cv2.namedWindow(self.windowname2, cv2.WINDOW_NORMAL)
		cv2.resizeWindow(self.windowname2, width, height)

	def movewindow(self, id):
		screen_id = id
		screen = screeninfo.get_monitors()[screen_id]
		width, height = screen.width, screen.height
		print('width,height are ', width, height)
		cv2.moveWindow(self.windowname2, screen.x, screen.y)
		self.image5 = np.zeros([height, width, 3], np.uint8)

	def nobiaotilan(self):
		cv2.setWindowProperty(self.windowname2, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

	def addimage(self, frame):
		self.image6 = frame
		# 由于投影仪左右反转 所以这里把放在二屏的相机的图左右翻转一下
		# self.image6 = cv2.flip(self.image6, 1)
		self.image1 = cv2.add(frame, self.image3)

	def changeimage(self, width, height, x1, y1, z):
		self.image4 = cv2.resize(self.image2, (width, height))
		# 调同轴，需要投影相机拍到的画面，调用下面这句话，注释上面这句话
		# self.image4 = cv2.resize(self.image6, (width, height))

		self.image5[x1:x1+height, y1:y1+width] = self.image4
		self.image5 = cv2.flip(self.image5, 0)
		# 加框
		# self.image5[x1-1-z:x1-1, y1-1:y1+1+width] = [255, 255, 255]
		# self.image5[x1+height+1:x1+height+1+z, y1-1:y1+1+width] = [255, 255, 255]
		# self.image5[x1-1-z:x1+height+1+z, y1-1-z:y1-1] = [255, 255, 255]
		# self.image5[x1-1-z:x1+height+1+z, y1+width+1:y1+width+1+z] = [255, 255, 255]

	def showimage(self):
		# cv2.imshow(self.windowname1, self.image3)
		cv2.imshow(self.windowname1, self.image1)

		cv2.imshow(self.windowname2, self.image5)

	def bindingwi(self, color1, color2, thickness, width, height):
		def drawline(event, x, y, flags, param):
			if event == cv2.EVENT_LBUTTONDOWN:
				self.drawing = True
				# 由于投影仪自身有反转， 坐标系对应的是opencv的坐标系, x对应width y对应height 如果俩个图画一样的点self.list1和list2
				# 坐标一样就行，左右翻转需要改成width-x,上下翻转height-y
				self.list1.append((x, y))
				self.list2.append((x, y))

				self.start = datetime.datetime.now()
			elif event == cv2.EVENT_MOUSEMOVE:
				if self.drawing:
					if self.mode:
						self.list1.append((x, y))
						self.list2.append((x, y))
						cv2.line(self.image3, self.list1[self.number], self.list1[self.number+1], color1, thickness=thickness)
						cv2.line(self.image2, self.list2[self.number], self.list2[self.number+1], color2, thickness=thickness)
						# 画点 不和画线的坐标一样 画点对应的是opencv的坐标系 x对应width y对应height
						# cv2.circle(self.image3, (x, y), 4,color1, -1)
						# cv2.circle(self.image_annotation_1, (width-x, y), 4, color2, -1)
						self.end = datetime.datetime.now()
						self.number = self.number+1
						_time = str(self.end-self.start)
						a, b, c = _time.split(':')
						print(c)
					else:
						self.image3[y - 25:y + 25, x - 25:x + 25, :] = self.image3_copy[y - 25:y + 25, x - 25:x + 25, :]
						self.image2[y - 25:y + 25, x - 25:x + 25, :] = self.image2_copy[y - 25:y + 25, x - 25:x + 25, :]
			elif event == cv2.EVENT_LBUTTONUP:
				self.drawing = False
				for (x, y) in self.list1:
					self.list3.append(x)
					self.list4.append(y)
				self.list1 = []
				self.list2 = []
				self.number = 0

		cv2.setMouseCallback(self.windowname1, drawline)

	def movebiaoji(self):
		if self.list3:
			self.list3.sort()
			self.list4.sort()
			# print(self.list3[0], self.list3[-1])
			# bbox = (x,y,w,h)
			self.bbox = (int(self.list3[0]-3), int(self.list4[0]-3), int(self.list3[-1]-self.list3[0]+3), int(self.list4[-1]-self.list4[0]+3))
			self.image8 = copy.copy(self.image3[int(self.list4[0]-3):int(self.list4[-1]), int(self.list3[0]-3):int(self.list3[-1])])
			# cv2.imshow('1', self.image8)
			# cv2.waitKey(0)
			print(self.bbox)
			self.list3 = []
			self.list4 = []

	def dong(self, x, y, w, h):
		self.image3[:, :] = [0, 0, 0]
		dst = cv2.resize(self.image8, (w, h))
		self.image3[y:y+h, x:x+w] = dst


