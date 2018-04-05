#! /usr/bin/env python
#coding=utf-8

import os
import cv2
import sys
import numpy
from PIL import Image

def getLeftTopArea(img):

    rect = (15, 20, 100, 50)
    mask = numpy.zeros(img.shape[:2], numpy.uint8)
    bgModel = numpy.zeros((1,65), numpy.float64)
    fgModel = numpy.zeros((1,65), numpy.float64)
    cv2.grabCut(img, mask, rect, bgModel, fgModel, 5, cv2.GC_INIT_WITH_RECT)
    mask2 = numpy.where((mask == 2) | (mask == 0), 0, 1).astype(numpy.uint8)
    out = img * mask2[:, :, numpy.newaxis]
    return out

def isLeftTopPearVideo(frame):

    temple = getLeftTopArea(frame)
    temple = temple[23:46, 25:54]
    img = cv2.imread('d:/PICTURE/sy.jpg')
    img = img[23:46, 25:54]

    if numpy.sum(img - temple) <= 1000:
        return True
    return False

def isCrust(pix):
    return sum(pix) < 25

def hCheck(img, y, step = 50):
    count = 0
    width = img.size[0]
    for x in xrange(0, width, step):
        if isCrust(img.getpixel((x, y))):
            count += 1
        if count > width / step / 2:
            return True
    return False

def vCheck(img, x, step = 50):
    count = 0
    height = img.size[1]
    for y in xrange(0, height, step):
        if isCrust(img.getpixel((x, y))):
            count += 1
        if count > height / step / 2:
            return True
    return False

def boundaryFinder(img,crust_side,core_side,checker):
    if not checker(img,crust_side):
        return crust_side
    if checker(img,core_side):
        return core_side

    mid = (crust_side + core_side) / 2
    while  mid != core_side and mid != crust_side:
        if checker(img,mid):
            crust_side = mid
        else:
            core_side = mid
        mid = (crust_side + core_side) / 2
    return core_side
    pass

def handleImage(img):

    if img.mode != "RGB":
        img = img.convert("RGB")

    width, height = img.size

    left = boundaryFinder(img, 0, width/2, vCheck)
    right = boundaryFinder(img, width-1, width/2, vCheck)
    top = boundaryFinder(img, 0, height/2, hCheck)
    bottom = boundaryFinder(img, height-1, width/2, hCheck)
    rect = (left, top, right, bottom)
    img = img.crop(rect)
    img = img.resize((width, height), Image.ANTIALIAS)
    return img


inputFileDir = sys.argv[1]
outputFileDir = sys.argv[2]
samplingTime = int(sys.argv[3])
degree = int(sys.argv[4])
startTime = int(sys.argv[5])


print("inputFileDir  : " + inputFileDir)
print("outputFileDir : " + outputFileDir)
videoList = []
for videoName in os.listdir(inputFileDir):
    videoList.append(videoName)

for videoName in videoList:

    video = cv2.VideoCapture(inputFileDir + "\\" + videoName);
    if video.isOpened():
        time = startTime
        # # Find OpenCV version
        major_ver = (cv2.__version__).split('.')[0]
        if int(major_ver) < 3:
            fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
            print videoName,"Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps)
        else:
            fps = video.get(cv2.CAP_PROP_FPS)
            print videoName,"Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps)


        print("Starting  processing " + videoName + " ...")
        rval, img = video.read()
        print(img)

        while rval:  # 循环读取视频帧
            imageVar = cv2.Laplacian(img, cv2.CV_64F).var() #拉普拉斯判断模糊度

            face_cascade = cv2.CascadeClassifier(r'.\haarcascade_frontalface_alt.xml')
            grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # 人脸检测，1.2和2分别为图片缩放比例和需要检测的有效点数
            faces = face_cascade.detectMultiScale(grey, scaleFactor=1.2, minNeighbors=3, minSize=(32, 32))

            if(imageVar > degree and (len(faces) > 0) ):
                img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                img = handleImage(img)
                img = cv2.cvtColor(numpy.asarray(img), cv2.COLOR_RGB2BGR)
                cv2.imwrite(outputFileDir + "\\" + videoName.split(".")[0] + '.jpg', img)  # 存储为图像

                print(videoName," processing finished !")
                video.release()

            video.set(cv2.cv.CV_CAP_PROP_POS_MSEC, time * 1000)  # 设置时间标记
            rval, img = video.read()


            time += samplingTime

            cv2.waitKey(1)

        video.release()







