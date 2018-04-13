# coding=utf-8
from ffmpy import FFmpeg
import ffmpy
import subprocess
import sys
import os
import cv2
import ConfigParser
import string, os, sys
from SqliteOperator import *

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
sections = cf.sections()
resolutionConfig = {}
bias = int(20)

conn = sqlite3.connect('processedVideo')
table = 'processedVideo'
fields = ('videoName', 'successful')
conn.text_factory=str

if not db_has_table(conn, table):
    db_create_table(conn, table, fields, 'videoName')

for sec in sections:
    resolutionConfig[sec] = {}
    resolutionConfig[sec]['x'] = cf.get(sec, "x")
    resolutionConfig[sec]['y'] = cf.get(sec, "y")
    resolutionConfig[sec]['w'] = cf.get(sec, "w")
    resolutionConfig[sec]['h'] = cf.get(sec, "h")
    resolutionConfig[sec]['width'] = cf.get(sec, "width")
    resolutionConfig[sec]['height'] = cf.get(sec, "height")

def isCorrectFormat(bias,height,resolutionConfig):
    for resolution in resolutionConfig.keys():
        h = int(resolutionConfig[resolution]['height'])
        height = int(height)
        if height <= (h + bias) and height >= (h - bias):
            return resolution,True

    return None,False


inputFileDir = sys.argv[1]
outputFileDir = sys.argv[2]
ffmpegPath = sys.argv[3]

print("inputFileDir  : " + inputFileDir)
print("outputFileDir : " + outputFileDir)



while True:
    videoList = []

    for videoName in os.listdir(inputFileDir):
        # videoName = unicode(videoName)
        if db_table_get_count(conn, table, ('videoName=?', [videoName])) == 0:
            videoList.append(videoName)

    for videoName in videoList:
        input = inputFileDir + "\\" + videoName
        output = outputFileDir + "\\" + videoName

        video = cv2.VideoCapture(inputFileDir + "\\" + videoName);
        if video.isOpened():
            resolution,correct = isCorrectFormat(bias,video.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT),resolutionConfig)
            if correct:
                video.release()
                print(videoName + " is " + resolution + " start removing watermark...")
                x = resolutionConfig[resolution]['x']
                y = resolutionConfig[resolution]['y']
                w = resolutionConfig[resolution]['w']
                h = resolutionConfig[resolution]['h']
                delogo = "delogo=x=" + x + ":y=" + y + ":w=" + w + ":h=" + h

                removeVideoLogo(ffmpegPath,input,output,delogo)

                rows = [fields]
                rows.append((videoName, 'successful'))
                db_table_add_rows(conn, table, rows, ['videoName'])
            else:
                video.release()
                print(videoName + " Video resolution error! shoule be (360P/480P/504P/720P/1080P)")
                rows = [fields]
                rows.append((videoName, 'fail'))
                db_table_add_rows(conn, table, rows, ['videoName'])

        cmd = "del " + '"' + inputFileDir + "\\" + videoName + '"  '
        os.system(cmd)


    # print("delogo=x=" + x + ":y=" + y + ":w=" + ":h=" + h)
    # delogo = "delogo=x=" + x + ":y=" + y + ":w=" + ":h=" + h





