from Eyetracking_main import *
from Eyetracking_process import *
from PyQt5.QtWidgets import QApplication,QMainWindow,QDialog,QMessageBox
from PyQt5.QtCore import QTimer,QThread,pyqtSignal
from PyQt5.QtGui import QIcon,QFont,QImage,QPixmap
import sys
import time
import datetime
import cv2
import dlib
import numpy as np

import matplotlib
matplotlib.use("Qt5Agg")#声明使用QT5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import random
from scipy import interpolate
from threading import Timer


"""
PyQt5 实时获取屏幕界面图像，python3使用matplotlib
https://blog.csdn.net/qq_34190023/article/details/78163622?locationNum=9&fps=1
Matplotlib植入PyQt5 + QT5的UI呈现
http://www.cnblogs.com/laoniubile/p/5904817.html
https://www.cnblogs.com/sesshoumaru/p/6035548.html
https://blog.csdn.net/resorcap/article/details/38965153
PyQt5教程-13-滑块控件
https://blog.csdn.net/weiaitaowang/article/details/52104795
matplotlib绘图常见说明
https://www.cnblogs.com/nju2014/p/5707980.html

"""
class MyThread(QThread):
    trigger = pyqtSignal(str)

    def __init__(self, parent=None):
        super(MyThread, self).__init__(parent)

    def setup(self, thread_no):
        self.thread_no = thread_no

    def run(self):
#        time.sleep(random.random() * 5)  # random sleep to imitate working
        self.trigger.emit(self.thread_no)



class Figure_Canvas(FigureCanvas):
    def __init__(self,parent=None,width=3.2,height=3,dpi=100):
        self.fig=Figure(figsize=(width,height),dpi=100)
        FigureCanvas.__init__(self,self.fig)
        self.setParent(parent)
        self.axes=self.fig.add_subplot(111)
        #self.axe2 =fig.add_subplot(212)
        self.axes.set_xlim(-.5,.5)
        self.axes.set_ylim(-.5,.5)
        #self.axes.set_xticks([-0.5,-0.25, 0, 0.25,0.5])
        #self.axes.set_yticks([-0.5,-0.25, 0, 0.25,0.5])




        self.xs = [0, 0]
        self.ys = [0, 0]

    def test(self,list):
        x = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        y = [23, 21, 32, 13, 3, 132, 13, 3, 1]
        self.axes.plot(x, y)
    def plot(self):
        timer = QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(1000)

    def update_figure(self,xy):
        if len(xy) <=2:
            return
        #print(xy)

        #print(xy.split(','))
        xy_0=float(xy.split(',')[0][1:])
        xy_1 = float(xy.split(',')[1][:-1])
        #print(xy_0,xy_1)
        #return
        #print(xy[0],xy[1])
        # x = np.linspace(0, 10, 10)
        # y = [random.randint(0, 10) for i in range(10)]
        # xx = np.linspace(0,10)
        # f = interpolate.interp1d(x, y, 'quadratic')  # 产生插值曲线的函数
        # yy = f(xx)

        #print (type(xy))
        #return
        # if type(xy)=="<class 'str'>":
        #     print("yes")
        #     return
        #print(xy)




        self.xs[0]=self.xs[1]
        self.ys[0]=self.ys[1]
        # self.xs[1]=xy[0]
        # self.ys[1]=xy[1]#因为眼睛opencv的图像与画图时候的图像是上下反着的，因此用1减去y的值
        self.xs[1] = xy_0
        self.ys[1]=xy_1

        self.axes.grid(True)
        #self.axes.cla()
        self.axes.plot(self.xs,self.ys)
        #self.axe2.scatter(xy[0],xy[1])

        self.draw()

        #print(self.l_RECORD)
    def clean(self):
        self.axes.cla()
    # def savefig(self,name):
    #     print("保存成功!")
    #     self.axes.savefig(name.split('.')[0])
    def save(self,name):
        self.fig.savefig(name)




class parentWindow(QMainWindow):
    signal1 = pyqtSignal(list)
    #信号设置一定在函数体外https://stackoverflow.com/questions/2970312/pyqt4-qtcore-pyqtsignal-object-has-no-attribute-connect'PyQt5.QtCore.pyqtSignal' object has no attribute 'connect'

    def __init__(self):
        """
        初始化主窗口Ui_MainWindow()
        """

        QMainWindow.__init__(self)

        self.main_ui = Ui_MainWindow()
        self.main_ui.setupUi(self)
        self.setWindowIcon(QIcon("cat.png"))
        self.flag=1

        #初始化dlib中的库
        self.detector = dlib.get_frontal_face_detector()#检测人脸
        predictor_path = "./shape_predictor_68_face_landmarks.dat"
        self.predictor = dlib.shape_predictor(predictor_path)#68个特征点提取器

        #初始化dlib中的人脸特征点排号
        self.RIGHT_EYE_START = 37 - 1
        self.RIGHT_EYE_END = 42 - 1
        self.LEFT_EYE_START = 43 - 1
        self.LEFT_EYE_END = 48 - 1

        #初始化瞳孔定位的一些初值
        self.l_points = []
        self.l_RECORD = []
        self.r_points = []
        self.r_RECORD = []
        self.left_eye_crop=[]
        self.right_eye_crop=[]

        self.threads = MyThread(self)
        #self.threads_1 = MyThread(self)





        btn2 = self.main_ui.toolButton_2
        btn2.clicked.connect(self._start)  # 这里的对象不要加括号



    def _start(self):

        #定义一些初始化的函数
        self.timer1 = QTimer()
        self.timer1.setInterval(1)
        self.timer2 = QTimer()
        self.timer2.setInterval(1000)
        self.timer3=QTimer()
        self.timer3.setInterval(1000*60*5)









        #self.openVideo()
        self.dr= Figure_Canvas()
        self.threads.trigger.connect(self.dr.update_figure)
        #self.threads.trigger.connect(dr.savefig)
        #self.signal1.connect(dr.update_figure)
        self.main_ui.toolButton_4.clicked.connect(self.dr.save)
        graphicscene = QtWidgets.QGraphicsScene()  # 第三步，创建一个QGraphicsScene，因为加载的图形（FigureCanvas）不能直接放到graphicview控件中，必须先放到graphicScene，然后再把graphicscene放到graphicview中

        graphicscene.addWidget(self.dr)  # 第四步，把图形放到QGraphicsScene中，注意：图形是作为一个QWidget放到QGraphicsScene中的
        #
        self.main_ui.graphicsView.setScene(graphicscene)  # 第五步，把QGraphicsScene放入QGraphicsView
        #
        self.main_ui.graphicsView.show()  # 最后，调用show方法呈现图形！Voila!!

        self.initCanvas()

        self.openVideo()
        self.initTime()



    def initCanvas(self):
        pass



    def initTime(self):

        self.timer2.start()
        # 信号连接到槽
        self.timer2.timeout.connect(self.onTimerOut)


        # self.timer3.setInterval(1000)
        # self.time3.start()
        # self.timer3.timeout.connect()


    def onTimerOut(self):
        self.main_ui.lcdNumber_2.display(time.strftime("%H:%M:%S",time.localtime()))

        #print(time.strftime("%H:%M:%S",time.localtime()))
        #print(datetime.datetime.now().strftime('%H:%M:%S'))







        # #实例化一个FigureCanvas用来画图
        #
        #
        # dr.plot()  # 画图






    def openVideo(self):
        """
        结合capPicture()函数，利用定时器打开视频
        :return:
        """

        self.main_ui.lcdNumber.display(time.strftime("%H:%M:%S",time.localtime()))
        self.nowtime=time.strftime("%Y-%m-%d%H%M%S",time.localtime())


        self.capture = cv2.VideoCapture(0)


        self.timer1.timeout.connect(self.capPicture)
        self.timer1.start()
        #pass
        self.timer3.timeout.connect(self.closeWindow)
        self.timer3.start()




    def capPicture(self):
        """
        配合定时器打开视频
        :return:
        """
        now=time.time()
        ret, img = self.capture.read()
        if ret:
            img=cv2.flip(img,1,dst=None)
            self.height, self.width, bytesPerComponent = img.shape
            bytesPerLine = 3 * self.width
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 转成灰度图像
            dets = self.detector(gray, 0)
            for i, d in enumerate(dets):
                shape = self.predictor(img, d)
                landmarks = np.matrix([[p.x, p.y] for p in shape.parts()])
                left_eye = landmarks[self.LEFT_EYE_START:self.LEFT_EYE_END + 1]
                right_eye = landmarks[self.RIGHT_EYE_START:self.LEFT_EYE_END + 1]
                l_tracker=[]
                r_tracker=[]
                l_tracker,self.left_eye_crop,self.l_points, self.l_RECORD = self.pupil_location(left_eye, img, gray, self.l_points, self.l_RECORD)
                #self.signal1.emit(l_tracker)
                self.threads.trigger.emit(str(l_tracker))

                l_height, l_width = self.left_eye_crop.shape
                l_bytesPerLine = 1 * l_width
                l_QImg = QImage(bytes(self.left_eye_crop.data), l_width, l_height, l_bytesPerLine,
                                QImage.Format_Indexed8)
                l_pixmap = QPixmap.fromImage(l_QImg).scaled(self.main_ui.label_7.width(), self.main_ui.label_7.height())

                self.main_ui.label_7.setPixmap(l_pixmap)



                r_tracker,self.right_eye_crop,self.r_points, self.r_RECORD = self.pupil_location(right_eye, img, gray, self.r_points, self.r_RECORD)
                #self.signal1.emit(r_tracker)
                r_height, r_width = self.right_eye_crop.shape
                r_bytesPerLine = 1 * r_width
                r_QImg = QImage(bytes(self.right_eye_crop.data), r_width, r_height, r_bytesPerLine,
                                QImage.Format_Indexed8)
                r_pixmap = QPixmap.fromImage(r_QImg).scaled(self.main_ui.label_2.width(), self.main_ui.label_2.height())
                self.main_ui.label_2.setPixmap(r_pixmap)



            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            QImg = QImage(img.data, self.width, self.height, bytesPerLine, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(QImg).scaled(self.main_ui.label.width(), self.main_ui.label.height())
            self.main_ui.label.setPixmap(pixmap)
            #print("fps:{}".format(1/(time.time()-now)))



            # cv2.namedWindow("img")
            # cv2.imshow("img",img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.imwrite(time.strftime("%Y-%m-%d-%H-%M-%S-shot",time.localtime())+".jpeg",img)
    def pupil_location(self,eye,img,gray,points,RECORD):

        #通过68个特征点寻找眼睛部位，并且将眼睛框起来
        l = abs(eye[3, 0] - eye[0, 0])#两只眼角的长度作为宽度
        #确定topleft的坐标
        #tl = (eye[0, 0], eye[0, 1] - int(l / 2))
        #br = (eye[3, 0], eye[3, 1] + int(l / 2))
        tl=(int(eye[5,0]+(eye[4,0]-eye[5,0])/2-l/2),int(eye[5,1]-(eye[5,1]-eye[1,1])/2-l/2))
        cv2.rectangle(img, tl, (tl[0] + l, tl[1] + l), (255, 255, 255), 2)
        crop = gray[tl[1]:(tl[1] + l), tl[0]:(tl[0] + l)]
        #crop = img[tl[1]:(tl[1] + l), tl[0]:(tl[0] + l)]
        #print(type(crop))
        gb = cv2.GaussianBlur(crop, (5, 5), 15)
        #cv2.imshow("gb", gb)

        #eh = cv2.equalizeHist(gb)
        #cv2.imshow("eh", eh)
        ret, th1 = cv2.threshold(gb, 50, 255, cv2.THRESH_BINARY)
        #cv2.imshow("th1", th1)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (6, 6))
        opening = cv2.morphologyEx(th1, cv2.MORPH_OPEN, kernel)
        #cv2.imshow("opening", opening)
        kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (6, 6))
        closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel2)
        # kernel3 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        #cv2.imshow("closing", closing)
        # erosion = cv2.erode(closing, kernel3)
        # cv2.imshow("erosion", erosion)
        # dilation = cv2.dilate(erosion, kernel3)
        # cv2.imshow("dilation", dilation)
        canny = cv2.Canny(closing, 60, 150)
        #cv2.imshow("canny", canny)
        circles = cv2.HoughCircles(canny, cv2.HOUGH_GRADIENT, 2, 40, param1=30, param2=30, minRadius=0, maxRadius=20)
        # print(circles)
        # if circles!=None:
        tracker=[]
        if np.all(circles != None):
            # print("检测到瞳孔！")
            # return circles[0]
            for circle in circles[0]:

                x = int(circle[0])
                y = int(circle[1])
                r = int(circle[2])
                points.extend([(x, y)])
                # print(points)
                if len(points) == self.flag:
                    #通过self.flag调整定位精度
                    xy = self.stabilize(points)
                    x = int(xy[0])
                    y = int(xy[1])
                    # 由于眼动采集时驾驶人来回的移动，导致像素框的大小在记录时不一致，因此坐标值都处于此时的眼睛框大长度做归一化处理
                    tracker=[float('%.3f'%(x / l-0.5)),float('%.3f'%(1- y / l-.5))]
                    RECORD.extend([[float('%.3f'%(x / l-.5)),float('%.3f'%(1- y / l-.5))]])
                    #print(tracker)

                    #print()

                    # print(points)

                    # crop = img.copy()
                    crop = cv2.circle(crop, (x, y), r, (255, 255, 255), 1)
                    crop = cv2.circle(crop, (x, y), 1, (255, 255, 255), -1)
                    #
                    # height, width = crop.shape
                    # bytesPerLine = 1 * width
                    # #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    # print(crop.data)
                    # print(type(crop[:]))
                    # print(type(img))
                    # print(type(img.data))
                    # QImg = QImage(bytes(crop.data), width, height, bytesPerLine, QImage.Format_Indexed8)
                    # pixmap = QPixmap.fromImage(QImg).scaled(self.main_ui.label_7.width(), self.main_ui.label_7.height())
                    # self.main_ui.label_7.setPixmap(pixmap)
                    #
                    #
                    # cv2.imshow("crop", crop)
                    xx = tl[0] + x
                    yy = tl[1] + y
                    img = cv2.circle(img, (xx, yy), 2, (0, 0, 255), -1)

                    points = []
                    # print(RECORD)
                    # plt.title(" eye tracking scatter")
                    #
                    # xs[0] = xs[1]
                    # ys[0] = ys[1]
                    # xs[1] = xy[0] / l
                    # ys[1] = xy[1] / l
                    #
                    # # plt.plot(xs, ys)
                    #
                    # plt.scatter(xs, xs)
                    # plt.pause(0.001)
            # xx = tl[0] + x
            # yy = tl[1] + y
            # img = cv2.circle(img, (xx, yy), 3, (255, 255, 255), -1)
        return tracker,crop,points, RECORD

    def stabilize(self,points):
        """
        因为houghCircle的结果一直变化所以我们需要计算瞳孔位置的平均值来稳定结果

        :return:
        """
        sumX = 0
        sumY = 0
        count = 0
        for i in range(len(points)):
            sumX += points[i][0]
            sumY += points[i][1]
            count += 1
        if count > 0:
            sumX /= count
            sumY /= count

        return (sumX, sumY)

    def closeWindow(self):
        self.capture.release()
        self.timer1.stop()
        self.timer2.stop()
        self.timer3.stop()

        endtime = datetime.datetime.now().strftime('%H%M%S')

        filename = "/home/hx-104b/EyeTracking/data/{}-{}.txt".format(self.nowtime, endtime)
        #pngname="/home/hx-104b/EyeTracking/data/{}.png".format(endtime)
        # ret, Img = self.capture.read()
        pngname = "/home/hx-104b/EyeTracking/data/{}-{}.png".format(self.nowtime,endtime)
        # cv2.imwrite(initname, Img)
        with open(filename, "w") as f:
            # f.write('\n''\n')
            f.write("Begin at {}".format(self.nowtime))
            for i in self.l_RECORD:
                f.write('\n')
                f.writelines(str(i))
            f.write('\n')
            f.write("End at {}".format(endtime))
        #print(pngname)
        self.dr.save(pngname)
        print("眼动轨迹数据已经成功写入文件{}并保存图片.".format(filename))
        #self.threads_1.trigger.emit(filename)
        #savefig

        QMessageBox.information(self,"Done!","眼动轨迹数据已经成功写入文件{}.".format(filename),QMessageBox.Yes)



class childWindow(QDialog):
    def __init__(self):
        """
        初始化子窗口Ui_Dialog()
        """
        QDialog.__init__(self)
        self.child=Ui_Dialog()
        self.child.setupUi(self)


if __name__=='__main__':

    app=QApplication(sys.argv)
    print(sys.argv)
    #main = QMainWindow()
    # main_ui=Ui_MainWindow()
    # main_ui.setupUi(main)


    window=parentWindow()
    child=childWindow()

    #通过toolButton将两个窗体关联
    btn=window.main_ui.toolButton
    btn.clicked.connect(child.show)

    #通过按钮打开摄像头


    # 显示
    window.show()
    sys.exit(app.exec_())
