#! /usr/bin/env python
#coding=utf-8

import os
import cv2
import sys
import numpy
from PIL import Image
import random
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

startTime = int(sys.argv[5])


print("inputFileDir  : " + inputFileDir)
print("outputFileDir : " + outputFileDir)
videoList = []
for videoName in os.listdir(inputFileDir):
    videoList.append(videoName)

for videoName in videoList:
    moveVedioCmd = []
    isCut = False
    import time as pyTime
    print("Starting  processing " + videoName + " ...")

    time_start = int(pyTime.time())
    degree = int(sys.argv[4])

    video = cv2.VideoCapture(inputFileDir + "\\" + videoName);
    frameCount = video.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)
    fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
    maxTime = frameCount / fps

    # randTime = random.randint(int(startTime),int(maxTime))
    # video.set(cv2.cv.CV_CAP_PROP_POS_MSEC, randTime * 1000)  # 设置时间标记
    # rval, img = video.read()
    # cv2.imwrite(outputFileDir + "\\" + videoName.split(".")[0] + '.png', img)  # 存储为图像

    if video.isOpened():

        while degree >= 100:
            time = startTime
            # # Find OpenCV version
            major_ver = (cv2.__version__).split('.')[0]

            rval = True
            img  = None

            while rval :  # 循环读取视频帧

                if time < maxTime:
                    video.set(cv2.cv.CV_CAP_PROP_POS_MSEC, time * 1000)  # 设置时间标记
                    rval, img = video.read()
                else:
                    break

                imageVar = cv2.Laplacian(img, cv2.CV_64F) #拉普拉斯判断模糊度
                if imageVar is not None:
                    imageVar = imageVar.var()
                    face_cascade = cv2.CascadeClassifier(r'.\haarcascade_frontalface_alt.xml')
                    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    # 人脸检测，1.2和2分别为图片缩放比例和需要检测的有效点数
                    faces = face_cascade.detectMultiScale(grey, scaleFactor=1.2, minNeighbors=2, minSize=(32, 32))
                else:
                    imageVar = 0
                    facess = 0

                time_end = int(pyTime.time())
                # print((time_end - time_start))
                if ((time_end - time_start) > 30 ):

                    degree = 0
                    # video.release()
                    break
                    print(videoName, " processing finished !")

                elif (imageVar > degree and len(faces) > 0):

                    cv2.imwrite(outputFileDir + "\\" + videoName.split(".")[0] + '.png', img)  # 存储为图像
                    isCut = True

                    print(videoName," processing finished !")
                    degree = 0
                    # video.release()
                    break

                time += samplingTime
                cv2.waitKey(1)

            degree -= 100
            video.release()

        if isCut is False:
            cmd = "del " + '"' + inputFileDir + "\\" + videoName + '"  '
            print(cmd)
            os.system(cmd)







