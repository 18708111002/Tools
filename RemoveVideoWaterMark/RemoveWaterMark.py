#encode-UTF-8
import os
import sys

inputFileDir = sys.argv[1]
outputFileDir = sys.argv[2]

print("inputFileDir  : " + inputFileDir)
print("outputFileDir : " + outputFileDir)
videoList = []
for videoName in os.listdir(inputFileDir):
    videoList.append(videoName)

for videoName in videoList:

    print("Starting processing " + videoName)
    cmd = (r"D:\ffmpeg\bin\ffmpeg  -i  " + inputFileDir + "\\" + videoName +
              r" -vf delogo=x=650:y=32:w=160:h=65 " +  outputFileDir + "\\" + videoName)

    os.system(cmd)
    print(videoName + " Process finished")