from SqliteOperator import *
import os
import sys
import difflib
import time
import cv2
import ConfigParser

def isExist(results,videoName):
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


conn = sqlite3.connect('processedVideo')
table = 'processedVideo'
fields = ('videoName', 'saveTime')
conn.text_factory=str

inputFileDir = sys.argv[1]
outputFileDir = sys.argv[2]
minTime = int(sys.argv[3])
maxTime = int(sys.argv[4])
db_create_table(conn, table, fields)

for videoName in os.listdir(inputFileDir):
    # videoName = unicode(videoName)
    video = cv2.VideoCapture(inputFileDir + "\\" + videoName);
    length = int(video.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
    fps = int(video.get(cv2.cv.CV_CAP_PROP_FPS))
    
    if fps > 0 :
        videoTime = int(length / fps)
    else:
        videoTime = 0

    resolution, correct = isCorrectFormat(bias, video.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT), resolutionConfig)
    video.release()
    results = db_get_results(conn,table)
    if (videoTime >= minTime) and (not isExist(results,videoName)) and (videoTime <= maxTime) and correct:
        rows = [fields]
        rows.append((videoName, time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))))
        db_table_add_rows(conn, table, rows, ['videoName'])
        print(inputFileDir + "\\" + videoName  + "  is saved in database will move to " + outputFileDir + "\\")
        cmd = "move " + '"' + inputFileDir + "\\" + videoName + '"  ' + outputFileDir + "\\"
        # print(cmd)
        os.system(cmd)

    else:
        if correct is False:
            print(inputFileDir + "\\" + videoName + "  Video resolution error! ")
        elif videoTime > maxTime:
            print(inputFileDir + "\\" + videoName + "  is too long will be deleted")
        elif videoTime < minTime:
            print(inputFileDir + "\\" + videoName  + "  is too short will be deleted")
        else:
            print(inputFileDir + "\\" + videoName  + "  is existing will be deleted")
        cmd = "del " + '"' + inputFileDir + "\\" + videoName + '"  '
        os.system(cmd)