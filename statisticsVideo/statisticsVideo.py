from SqliteOperator import *
import os
import sys
import difflib
import time
import cv2

def isExist(results,videoName):
    for item in results:
        name = item[0]
        ratio = difflib.SequenceMatcher(None,name,videoName ).quick_ratio()

        if ratio > 0.75:
            return True

    return False


conn = sqlite3.connect('processedVideo')
table = 'processedVideo'
fields = ('videoName', 'saveTime')
conn.text_factory=str

inputFileDir = sys.argv[1]
minTime = int(sys.argv[2])

if not db_has_table(conn, table):
    db_create_table(conn, table, fields, 'videoName')

for videoName in os.listdir(inputFileDir):
    # videoName = unicode(videoName)
    video = cv2.VideoCapture(inputFileDir + "\\" + videoName);
    length = int(video.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
    fps = int(video.get(cv2.cv.CV_CAP_PROP_FPS))
    videoTime = int(length / fps)
    print(videoName,videoTime)
    video.release()

    results = db_get_results(conn,table)
    if (videoTime >= minTime) and (not isExist(results,videoName)):
        rows = [fields]
        rows.append((videoName, time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))))
        db_table_add_rows(conn, table, rows, ['videoName'])
        print(inputFileDir + "\\" + videoName  + "  is saved in database")

    else:
        if videoTime < minTime:
            print(inputFileDir + "\\" + videoName  + "  is too short will be deleted")
        else:
            print(inputFileDir + "\\" + videoName  + "  is existing will be deleted")
        cmd = "del " + '"' + inputFileDir + "\\" + videoName + '"  '
        os.system(cmd)