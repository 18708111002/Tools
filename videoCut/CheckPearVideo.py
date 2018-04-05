#coding=utf-8
import cv2
import numpy as np
import numpy
from PIL import Image

def getLeftTopArea(img):

    rect = (15, 20, 100, 50)
    mask = np.zeros(img.shape[:2], np.uint8)
    bgModel = np.zeros((1,65), np.float64)
    fgModel = np.zeros((1,65), np.float64)
    cv2.grabCut(img, mask, rect, bgModel, fgModel, 5, cv2.GC_INIT_WITH_RECT)
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype(np.uint8)
    out = img * mask2[:, :, np.newaxis]
    return out

def isLeftTopPearVideo(frame):

    temple = cv2.imread('./temple.jpg')
    temple = temple[23:46, 25:54]
    cv2.imshow('test win', temple)
    img = frame[23:46, 25:54]

    if numpy.sum(img - temple) <= 1000:
        return True
    return False


import sys
import os

inputFileDir = sys.argv[1]
outputFileDir = sys.argv[2]

print("inputFileDir  : " + inputFileDir)
print("outputFileDir : " + outputFileDir)
videoList = []
for videoName in os.listdir(inputFileDir):
    videoList.append(videoName)

for videoName in videoList:
    video = cv2.VideoCapture(inputFileDir + "\\" + videoName);
    if video.isOpened():

        video.set(cv2.cv.CV_CAP_PROP_POS_MSEC, 10 * 1000)  # 设置时间标记
        rval, img = video.read()

        if(isLeftTopPearVideo(img)):
            print(videoName + " has left-top Logo will move to " + outputFileDir)
            cmd = "move " + inputFileDir + "\\" + videoName + "  " + outputFileDir + " \\ " + videoName
            os.system(cmd)

cmd = "move " + inputFileDir + "\\" + videoName + "  " + outputFileDir + "\\" + videoName
print(cmd)
