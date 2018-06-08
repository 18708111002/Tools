#encode-UTF-8
import os
import sys
import cv2

inputFileDir = sys.argv[1]
delFinegrained = 0.1
delCnt = 10
print("inputFileDir : " + inputFileDir)
videoList = ['1.mp4']
# for videoName in os.listdir(inputFileDir):
#     videoList.append(videoName)

def delVideoXsecond(cutTime,maxTime):
    starTime = 0
    endTime = cutTime
    cmd = (r"D:\ffmpeg\bin\ffmpeg  -ss "+ str(starTime)  +" -i  " + inputFileDir + "\\" + videoName +
           r" -t "+ str(endTime) +" -acodec copy -vcodec copy tmp1.mp4  -y" )
    os.system(cmd)

    starTime = endTime + delFinegrained
    endTime = maxTime

    cmd = (r"D:\ffmpeg\bin\ffmpeg  -ss " + str(starTime) + " -i  " + inputFileDir + "\\" + videoName +
           r" -t " + str(endTime) + " -acodec copy -vcodec copy tmp2.mp4 -y")
    os.system(cmd)

    cmd = 'ffmpeg -f concat -i list.txt -c copy ' + inputFileDir + "\\" + videoName + " -y"
    os.system(cmd)


import random

for videoName in videoList:

    video = cv2.VideoCapture(inputFileDir + "\\" + videoName)
    print(inputFileDir + "\\" + videoName)
    frameCount = video.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)
    fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
    maxTime = int(frameCount / fps)

    while delCnt > 0 :
        cutTime = -1
        while cutTime <= 0:
            cutTime = int(random.random() * maxTime) - 2
        delVideoXsecond(cutTime,maxTime)

        delCnt -= 1

    print(videoName + " Process finished")