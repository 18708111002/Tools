#coding=utf-8
import cv2
import numpy as np
import numpy
from PIL import Image
import time

def getMatchPearLogoCnt(templeImg, img,videoName):
    img1 = img[0:400, 0:400]

    # Initiate SIFT detector
    sift = cv2.SIFT()

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(templeImg, None)

    # FLANN parameters
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)  # or pass empty dictionary
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)

    good = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good.append(m)

    return  len(good)

def getLeftTopArea(img):

    rect = (15, 20, 100, 50)
    mask = np.zeros(img.shape[:2], np.uint8)
    bgModel = np.zeros((1,65), np.float64)
    fgModel = np.zeros((1,65), np.float64)
    cv2.grabCut(img, mask, rect, bgModel, fgModel, 5, cv2.GC_INIT_WITH_RECT)
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype(np.uint8)
    out = img * mask2[:, :, np.newaxis]
    return out

def getMeanMatch(video):
    cnt = 0
    matches = 0

    randomList = []

    randomList.append(5)
    for i in range(4):
        randomList.append(random.randint(5, 30))

    for i in randomList:
        video.set(cv2.cv.CV_CAP_PROP_POS_MSEC, i * 1000)  # 设置时间标记
        rval, img = video.read()

        if rval:
            mCnt = getMatchLeftTopPearVideoCnt(img, videoName)
            # print(videoName,i,mCnt)
            matches += mCnt
            cnt += 1

    return  matches / cnt

def getMatchLeftTopPearVideoCnt(frame,videoName):

    temple = cv2.imread('./temple.jpg')
    img = frame

    # print(videoName,likely)
    return getMatchPearLogoCnt(temple,img,videoName)


import sys
import os
import random

inputFileDir = sys.argv[1]
outputFileDir = sys.argv[2]
videoTime = int(sys.argv[3])


print("inputFileDir  : " + inputFileDir)
print("outputFileDir : " + outputFileDir)
videoList = []
for videoName in os.listdir(inputFileDir):
    videoList.append(videoName)

moveVedioCmd = []
for videoName in videoList:

    video = cv2.VideoCapture(inputFileDir + "\\" + videoName);
    length = int(video.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
    fps = int(video.get(cv2.cv.CV_CAP_PROP_FPS))
    time = length / fps

    if video.isOpened():
        if time >= videoTime:
            meanMatch = getMeanMatch(video)
            if( meanMatch > 1):

                print(videoName + " has left-top Logo will move to " + outputFileDir)
                cmd = "move " + '"' + inputFileDir + "\\" + videoName + '"  ' + outputFileDir + "\\"
                # print(cmd)
                # os.system(cmd)
                moveVedioCmd.append(cmd)
        else:
            cmd = "move " + '"' + inputFileDir + "\\" + videoName + '"  ' + outputFileDir + "\\"
            print(cmd)
            # print(cmd)
            # os.system(cmd)
            moveVedioCmd.append(cmd)


    cv2.waitKey(1)
    video.release()
# print(moveVedioCmd)
for cmd in moveVedioCmd:
	os.system(cmd)


