#coding=utf-8


#https://www.cnblogs.com/adong7639/p/7695282.html
#https://www.pyimagesearch.com/2017/04/10/detect-eyes-nose-lips-jaw-dlib-opencv-python/?spm=a2c4e.11153940.blogcont336184.7.28a771e8O1D5Oz
import dlib
#from skimage import io
import cv2
import numpy as np
#import sys
#from imutils import face_utils
import time
#from matplotlib import pyplot as plt
import os
import datetime
from threading import Timer
"""
1.捕捉人脸定位
2.定位到眼睛
3.检测眨眼
4.定位瞳孔

"""
points = []

def eye_aspect_ratio(eye):
    # compute the euclidean distances between the two sets of
    # vertical eye landmarks (x, y)-coordinates
    """
    每一只眼睛总共有6个坐标，14为眼睛长度，26为眼睛左边高度，3,5为右边高度

    :param eye:
    :return:
    """


    A = euclidean_dist(eye[1], eye[5])
    B = euclidean_dist(eye[2], eye[4])

    # compute the euclidean distance between the horizontal
    # eye landmark (x, y)-coordinates
    C = euclidean_dist(eye[0], eye[3])

    # compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)

    # return the eye aspect ratio
    return ear
def euclidean_dist(list1,list2):
    # compute and return the euclidean distance between the two
    # points
    return np.linalg.norm(list1 - list2)

def ear_curve(EAR):
    pass

def pupil_location(eye,img,gray,points,RECORD):
    """

    :param eye:
    :param img:
    :param gray:
    :return:
    """

    l=abs(eye[3,0]-eye[0,0])
    tl=(eye[0,0],eye[0,1]-int(l/2))
    br=(eye[3,0],eye[3,1]+int(l/2))
    #print(tl,br)
    cv2.rectangle(img, tl, br, (255, 255, 255), 1)
    crop = gray[tl[1]:(tl[1]+l) , tl[0]:(tl[0]+l)]
    gb = cv2.GaussianBlur(crop, (5, 5), 15)
    cv2.imshow("gb",gb)

    eh = cv2.equalizeHist(gb)
    cv2.imshow("eh",eh)
    ret, th1 = cv2.threshold(eh, 50, 255, cv2.THRESH_BINARY)
    cv2.imshow("th1",th1)
    canny = cv2.Canny(th1, 60, 150)
    cv2.imshow("canny",canny)
    circles = cv2.HoughCircles(canny, cv2.HOUGH_GRADIENT, 2, 40, param1=30, param2=30, minRadius=0, maxRadius=20)
    #print(circles)
    #if circles!=None:
    if  np.all(circles!=None):
        #print("检测到瞳孔！")
        #return circles[0]
        for circle in circles[0]:
            x=int(circle[0])
            y=int(circle[1])
            r=int(circle[2])
            points.extend([(x,y)])
            #print(points)
            if len(points)==5:
                xy = stabilize(points)
                RECORD.extend([xy])

                #print(points)

                x=int(xy[0])
                y=int(xy[1])

                #crop = img.copy()
                #crop=cv2.circle(crop,(x,y),r,(255,255,255),1)
                crop = cv2.circle(crop, (x, y), 1, (255, 255, 255), -1)
                cv2.imshow("crop", crop)
                xx = tl[0] + x
                yy = tl[1] + y
                img = cv2.circle(img, (xx, yy), 3, (255, 255, 255), -1)

                points=[]
                #print(RECORD)
        #xx = tl[0] + x
        #yy = tl[1] + y
        #img = cv2.circle(img, (xx, yy), 3, (255, 255, 255), -1)
    return points,RECORD

    #return img



    #return xx,yy
    #elif type(circles)=="NoneType":
    #    pass

def stabilize(points):
    """
    因为houghCircle的结果一直变化所以我们需要计算瞳孔位置的平均值来稳定结果

    :return:
    """
    sumX=0
    sumY=0
    count=0
    for i in range(len(points)):
        sumX+=points[i][0]
        sumY+=points[i][1]
        count+=1
    if count>0:
        sumX/=count
        sumY/=count

    return (sumX,sumY)


RECORD=[]

#img=cv2.imread("2.jpeg")

detector = dlib.get_frontal_face_detector() #使用detector进行人脸检测 dets为返回的结果


predictor_path = "./shape_predictor_68_face_landmarks.dat"

#使用官方提供的模型构建特征提取器,predictor为一个类
predictor = dlib.shape_predictor(predictor_path)

#定义一些参数
RIGHT_EYE_START = 37 - 1
RIGHT_EYE_END = 42 - 1
LEFT_EYE_START = 43 - 1
LEFT_EYE_END = 48 - 1
#对应了人脸特征点中对应眼睛的那几个特征点的序号。由于list中默认从0开始，为保持一致，所以减一。
EAR=[]
EYE_AR_THRESH = 0.25
EYE_AR_CONSEC_FRAMES=5
COUNT=0
flag=1
def closewindow():
    global flag
    flag=0



timer=Timer(60*5,closewindow)



nowtime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print(type(nowtime))
print("Begin at {}.".format(nowtime))
cap = cv2.VideoCapture(0)
#plt.figure()
timer.start()
while(flag==1):

    stime = time.time()
    ret, img = cap.read()  # 读取视频流的一帧

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)  # 转成灰度图像
    dets = detector(gray, 0)

    #cv2.rectangle(img, (170, 60),(180,70) ,(255, 0, 0), thickness=-1)

    cv2.putText(img, "Begin at {}".format(nowtime), (170, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                (250, 255, 250), 2)

    cv2.putText(img, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), (300, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                (250, 255, 250), 2)



    for i, d in enumerate(dets):
        """
        使用enumerate 函数遍历序列中的元素以及它们的下标
        下标i即为人脸序号
        left：人脸左边距离图片左边界的距离 ；right：人脸右边距离图片左边界的距离
        top：人脸上边距离图片上边界的距离 ；bottom：人脸下边距离图片上边界的距离
        """
        #print("dets{}".format(d))
        #print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}"
        #    .format( i, d.left(), d.top(), d.right(), d.bottom()))
        #cv2.rectangle(img, (int(d.left()),int(d.top())), (int(d.right()),int(d.bottom())), (0,0,255), 2)
        shape=predictor(img, d)
        #print(predictor(img,dets[i]))
        #print(predictor(img, dets[i]).parts())#打印出来list中套着tuple
        #points = face_utils.shape_to_np(shape)
        #print(points)#打印出列表中套着列表

        landmarks = np.matrix([[p.x, p.y] for p in shape.parts()])
        #landmarks为矩阵列表，68×2的矩阵，可以通过landmarks[m,n]的形式获取对象，存储了所有的关键点坐标
        #predictor(img, dets[i]).parts()为坐标点对象
        #print(landmarks)#打印出来列表中套着列表


        left_eye=landmarks[LEFT_EYE_START:LEFT_EYE_END+1]
        right_eye=landmarks[RIGHT_EYE_START:LEFT_EYE_END+1]
        #print("左眼坐标序列：{}".format(left_eye))

        points,RECORD=pupil_location(left_eye,img,gray,points,RECORD)
        #points=[]
        #pupil_location(right_eye,img,gray)





        l_ear=eye_aspect_ratio(left_eye)
        r_ear=eye_aspect_ratio(right_eye)
        ear=(l_ear+r_ear) /2.0
        #print("当前的眼睛纵横比是{}".format(ear))
        EAR.append(ear)

        if ear<EYE_AR_THRESH:
            COUNT+=1

            if COUNT>EYE_AR_CONSEC_FRAMES:
                cv2.putText(img,"BLINK",(10,50),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        else:
            COUNTER = 0




        #print(EAR)

        #plt.ion()

        #plt.title(" eye tracking scatter")


        #plt.grid(True)
        #plt.xlim(0, 50)
        #plt.ylim(0, 50)
        #plt.plot(ear)

        # plt.scatter(xy[0],xy[1])
        #plt.pause(0.01)

        for idx, point in enumerate(landmarks):
            pos=(point[0,0],point[0,1])
            cv2.circle(img,pos,2,(0,255,0),-1)
        for idx1, point1 in enumerate(left_eye):
            pos=(point1[0,0],point1[0,1])
            cv2.circle(img,pos,2,(0,0,255),-1)
        for idx2, point2 in enumerate(right_eye):
            pos=(point2[0,0],point2[0,1])
            cv2.circle(img,pos,2,(0,0,255),-1)



    cv2.namedWindow("img")
    cv2.imshow("img", img)
    #print("elapse time is {}".format(1/(time.time()-stime)))

    if cv2.waitKey(1) & 0xFF==ord('q'):
        #endtime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        endtime = datetime.datetime.now().strftime('%H:%M:%S')
        print("End at {}.".format(endtime))
        break
#如果定时器时间到了，会直接到这一步
endtime = datetime.datetime.now().strftime('%H:%M:%S')
print("End at {}.".format(endtime))
filename="/home/hx-104b/EyeTracking/data/{}-{}.txt".format(nowtime,endtime)
with open(filename,"w") as f:
    #f.write('\n''\n')
    f.write("Begin at {}".format(nowtime))
    for i in RECORD:
        f.write('\n')
        f.writelines(str(i))
    f.write('\n')
    f.write("End at {}".format(endtime))

cap.release()
cv2.destroyAllWindows()
