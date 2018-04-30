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

from PIL import Image, ImageDraw,ImageFont

print("inputFileDir  : " + inputFileDir)
print("outputFileDir : " + outputFileDir)
videoList = []
for videoName in os.listdir(inputFileDir):
    videoList.append(videoName)
import time as pyTime
for videoName in videoList:

    print("Starting  processing " + videoName + " ...")


    video = cv2.VideoCapture(inputFileDir + "\\" + videoName);
    frameCount = video.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)
    fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
    print(fps)
    maxTime = frameCount / fps

    size = (int(video.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)),
            int(video.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)))

    # randTime = random.randint(int(startTime),int(maxTime))
    # video.set(cv2.cv.CV_CAP_PROP_POS_MSEC, randTime * 1000)  # 设置时间标记
    # rval, img = video.read()
    # cv2.imwrite(outputFileDir + "\\" + videoName.split(".")[0] + '.png', img)  # 存储为图像
    fourcc = cv2.cv.FOURCC('D', 'I', 'V', 'X')
    # out = cv2.VideoWriter('d:/outputvideo/output.avi', fourcc, fps, size)

    if video.isOpened():
        rval = True
        img = None
        time_start = pyTime.time()
        count = 0
        while rval:  # 循环读取视频帧
            rval, img = video.read()
            time_end = int(pyTime.time())
            # count = time_end - time_start
            count += 1


            cv2.putText(img, str(count), (20, 100)
                        , cv2.FONT_HERSHEY_PLAIN, 3.0, (255, 255, 255), thickness=5)


            cv2.imwrite(outputFileDir + "\\" + videoName.split(".")[0] + str(count) + '.png', img)  # 存储为图像

            # out.write(img)  # 写视频帧

            # pyTime.sleep(2)

            cv2.waitKey(1)








