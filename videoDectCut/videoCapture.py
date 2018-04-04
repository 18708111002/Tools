#! /usr/bin/env python
#coding=utf-8


import cv2
from pictureDiff import *
video = cv2.VideoCapture("d:/test2.mp4");


# # Find OpenCV version
major_ver = (cv2.__version__).split('.')[0]

if int(major_ver) < 3:
    fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
    print "Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps)
else:
    fps = video.get(cv2.CAP_PROP_FPS)
    print "Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps)

c = 1

lastPath = None
nowPath  = None


img1 = None
img2 = None
rval = True
likelyRate = 0.5 # 相似率小于0.5

while rval:  # 循环读取视频帧

    if img1 is None:
        rval, img1 = video.read()
        rval, img2 = video.read()
    else:
        img1 = img2
        rval,img2 = video.read()

    if(rval):
        likely = classify_gray_hist(img1, img2)

        if(likely < likelyRate):
            cv2.imwrite('d:/PICTURE/' + str(c / (fps) ) + " s (1)" + '.jpg', img1)  # 存储为图像
            cv2.imwrite('d:/PICTURE/' + str(c / (fps)) + " s (2)" + '.jpg', img2)  # 存储为图像

    c = c + 1

    cv2.waitKey(1)

video.release()


