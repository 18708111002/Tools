from ffmpy import FFmpeg
import ffmpy
import subprocess
import sys
import os
import cv2
import ConfigParser
import string, os, sys

def removeVideoLogo(ffmpegPath,input,output,delogo):
    ff = FFmpeg(ffmpegPath,
        inputs={input: None},
        outputs={output: '-vf ' + '"' + delogo + '"'}
    )
    print(ff.cmd)
    try:
        stdout,stderr = ff.run(stdout=subprocess.PIPE)
        print(videoName + " remove logo is  successful!")
    except ffmpy.FFRuntimeError as e:
        subprocess.call(r"del  " + output,shell=True)
        print(videoName + " remove logo is fail!")
        pass

cf = ConfigParser.ConfigParser()
cf.read("config.conf")

resolutionConfig = {}

resolutionConfig['360P'] = {}
resolutionConfig['360P']['x'] = cf.get("360P", "x")
resolutionConfig['360P']['y'] = cf.get("360P", "y")
resolutionConfig['360P']['w'] = cf.get("360P", "w")
resolutionConfig['360P']['h'] = cf.get("360P", "h")

resolutionConfig['480P'] = {}
resolutionConfig['480P']['x'] = cf.get("480P", "x")
resolutionConfig['480P']['y'] = cf.get("480P", "y")
resolutionConfig['480P']['w'] = cf.get("480P", "w")
resolutionConfig['480P']['h'] = cf.get("480P", "h")

resolutionConfig['504P'] = {}
resolutionConfig['504P']['x'] = cf.get("504P", "x")
resolutionConfig['504P']['y'] = cf.get("504P", "y")
resolutionConfig['504P']['w'] = cf.get("504P", "w")
resolutionConfig['504P']['h'] = cf.get("504P", "h")

resolutionConfig['720P'] = {}
resolutionConfig['720P']['x'] = cf.get("720P", "x")
resolutionConfig['720P']['y'] = cf.get("720P", "y")
resolutionConfig['720P']['w'] = cf.get("720P", "w")
resolutionConfig['720P']['h'] = cf.get("720P", "h")

resolutionConfig['1080P'] = {}
resolutionConfig['1080P']['x'] = cf.get("1080P", "x")
resolutionConfig['1080P']['y'] = cf.get("1080P", "y")
resolutionConfig['1080P']['w'] = cf.get("1080P", "w")
resolutionConfig['1080P']['h'] = cf.get("1080P", "h")

inputFileDir = sys.argv[1]
outputFileDir = sys.argv[2]
ffmpegPath = sys.argv[3]

print("inputFileDir  : " + inputFileDir)
print("outputFileDir : " + outputFileDir)

videoList = []
for videoName in os.listdir(inputFileDir):
    videoList.append(videoName)

for videoName in videoList:
    input = inputFileDir + "\\" + videoName
    output = outputFileDir + "\\" + videoName

    video = cv2.VideoCapture(inputFileDir + "\\" + videoName);
    if video.isOpened():
        resolution = str(int(video.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))) + "P"

        if resolutionConfig.has_key(resolution):
            video.release()
            print(videoName + " is " + resolution + " start removing watermark...")
            x = resolutionConfig[resolution]['x']
            y = resolutionConfig[resolution]['y']
            w = resolutionConfig[resolution]['w']
            h = resolutionConfig[resolution]['h']
            delogo = "delogo=x=" + x + ":y=" + y + ":w=" + w + ":h=" + h

            removeVideoLogo(ffmpegPath,input,output,delogo)
        else:
            video.release()
            print(videoName + " Video resolution error! shoule be (360P/480P/504P/720P/1080P)")


    # print("delogo=x=" + x + ":y=" + y + ":w=" + ":h=" + h)
    # delogo = "delogo=x=" + x + ":y=" + y + ":w=" + ":h=" + h





