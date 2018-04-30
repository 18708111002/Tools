from SqliteOperator import *
import os
import sys
import difflib
import time
import cv2
import ConfigParser
import chardet
# this is a simple example

cf = ConfigParser.ConfigParser()
cf.read("config.conf")
sections = cf.sections()
resolutionConfig = {}
bias = int(20)
dstFile = []
dstFileCnt = None

picSuffix = ['PNG']
videoSuffix = ['MP4']
for sec in sections:
    if not sec == "file_address":
        resolutionConfig[sec] = {}
        resolutionConfig[sec]['x'] = cf.get(sec, "x")
        resolutionConfig[sec]['y'] = cf.get(sec, "y")
        resolutionConfig[sec]['w'] = cf.get(sec, "w")
        resolutionConfig[sec]['h'] = cf.get(sec, "h")
        resolutionConfig[sec]['width'] = cf.get(sec, "width")
        resolutionConfig[sec]['height'] = cf.get(sec, "height")
    else:
        dstFileCnt = int(cf.get(sec, "address_count"))
        for i in range(0,dstFileCnt):
            dstFile.append(cf.get(sec, "address_"+str(i)))



while True:

    inputFileDir = sys.argv[1]
    dir = []

    for fileName in os.listdir(inputFileDir):
        if os.path.isdir(os.path.join(inputFileDir, fileName)):
            dir.append(os.path.join(inputFileDir, fileName))

    for inputFileDir in dir:
        for file in os.listdir(inputFileDir) :

            outputFileDir = dstFile.pop(0)
            dstFile.append(outputFileDir)
            os.chdir(inputFileDir)
            cmd = "move " + '"' + file  + '"  ' + outputFileDir + "\\"
            print(cmd)
            os.system(cmd)

    dir = []
    print("please wating ....")
    time.sleep(5)
