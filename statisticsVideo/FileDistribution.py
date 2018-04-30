from SqliteOperator import *
import os
import sys
import difflib
import time
import cv2
import ConfigParser
import chardet
# this is a simple example



def isExist(results,videoName):
    videoName = videoName.encode('utf-8')
    for item in results:
        name = item[0]
        ratio = difflib.SequenceMatcher(None,name,videoName ).quick_ratio()

        if ratio > 0.75:
            return True

    return False


cf = ConfigParser.ConfigParser()
cf.read("config.conf")
sections = cf.sections()
resolutionConfig = {}
bias = int(20)
dstFile = []
dstFileCnt = None

picSuffix = ['.PNG']
videoSuffix = ['.MP4']
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
        if os.path.isdir(os.path.join(inputFileDir,fileName)):
            dir.append(os.path.join(inputFileDir,fileName))

    for inputFileDir in dir :
        for videoName in os.listdir(inputFileDir):
            os.chdir(inputFileDir)
            vSuffix = os.path.splitext(videoName)[1]
            videoName = os.path.splitext(videoName)[0]
            outputFileDir = dstFile.pop(0)
            dstFile.append(outputFileDir)

            if (vSuffix.upper() in videoSuffix) or (vSuffix.lower() in videoSuffix):
                for suffix in picSuffix:
                    if os.path.exists(videoName + suffix.upper()) or os.path.exists(videoName + suffix.lower()):
                        cmd = "move " + '"' + videoName + vSuffix + '"  ' + outputFileDir + "\\"
                        print(cmd)
                        os.system(cmd)

                        cmd = "move " + '"' + videoName + suffix + '"  ' + outputFileDir + "\\"
                        print(cmd)
                        os.system(cmd)

    dir = []
    print("please wating ....")
    time.sleep(5)
