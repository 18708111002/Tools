
import sys
import os
from modifyVideoTitle.modifyVideoTitle import *
from videoCut.VideoRoughCut import *

inputFileDir = sys.argv[1]
outputFileDir = sys.argv[2]
samplingTime = int(sys.argv[3])
startTime = int(sys.argv[5])
degree = int(sys.argv[4])


print("inputFileDir  : " + inputFileDir)
print("outputFileDir : " + outputFileDir)

for videoName in os.listdir(inputFileDir):
    modifyTitle(videoName)

for videoName in os.listdir(inputFileDir):
    roughCutVideo(videoName, inputFileDir, outputFileDir, samplingTime, startTime,degree)
