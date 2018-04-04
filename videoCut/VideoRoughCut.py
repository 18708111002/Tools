#! /usr/bin/env python
#coding=utf-8

import os
import cv2
import sys
from pictureDiff import *

inputFileDir = sys.argv[1]
outputFileDir = sys.argv[2]

print("inputFileDir  : " + inputFileDir)
print("outputFileDir : " + outputFileDir)
videoList = []
for videoName in os.listdir(inputFileDir):
    videoList.append(videoName)

for videoName in videoList:

    video = cv2.VideoCapture(inputFileDir + "\\" + videoName);

    # # Find OpenCV version
    major_ver = (cv2.__version__).split('.')[0]
    if int(major_ver) < 3:
        fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
        print videoName,"Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps)
    else:
        fps = video.get(cv2.CAP_PROP_FPS)
        print videoName,"Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps)

    c = 1
    print("Starting  processing " + videoName + " ...")
    rval, img = video.read()

    while rval:  # 循环读取视频帧
        imageVar = cv2.Laplacian(img, cv2.CV_64F).var() #拉普拉斯判断模糊度

        face_cascade = cv2.CascadeClassifier(r'.\haarcascade_frontalface_alt.xml')
        grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 人脸检测，1.2和2分别为图片缩放比例和需要检测的有效点数
        faces = face_cascade.detectMultiScale(grey, scaleFactor=1.2, minNeighbors=3, minSize=(32, 32))

        if(imageVar > 500 and (len(faces) > 0) ):
            cv2.imwrite(outputFileDir + "\\" + videoName + '.jpg', img)  # 存储为图像
            print(videoName," processing finished !")
            video.release()


        rval, img = video.read()

        c = c + 1

        cv2.waitKey(1)

    video.release()







