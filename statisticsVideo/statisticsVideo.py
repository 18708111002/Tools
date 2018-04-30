from SqliteOperator import *
import os
import sys
import difflib
import time
import cv2
import ConfigParser
import chardet
import logging
# define the log file, file mode and logging level
logging.basicConfig(filename='stat.log', filemode="w", level=logging.DEBUG)
# logging.info('So should this')

def isExist(results,videoName):
    videoName = videoName.encode('utf-8')
    for item in results:
        name = item[0]
        ratio = difflib.SequenceMatcher(None,name,videoName ).quick_ratio()

        if ratio > 0.75:
            return True,name

    return False,None


cf = ConfigParser.ConfigParser()
cf.read("config.conf")
sections = cf.sections()
resolutionConfig = {}
bias = int(20)
dstFile = []
dstFileCnt = None

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




def isCorrectFormat(bias,height,resolutionConfig):
    for resolution in resolutionConfig.keys():
        h = int(resolutionConfig[resolution]['height'])
        height = int(height)
        if height <= (h + bias) and height >= (h - bias):
            return resolution,True

    return None,False

while True:
    conn = sqlite3.connect('processedVideo')
    table = 'processedVideo'
    fields = ('videoName', 'saveTime')
    conn.text_factory=str

    inputFileDir = sys.argv[1]
    minTime = int(sys.argv[2])
    maxTime = int(sys.argv[3])
    isCheckResolution = int(sys.argv[4])

    db_create_table(conn, table, fields)

    if isCheckResolution == 1:
        isCheckResolution = True
    else:
        isCheckResolution = False

    dir = []
    for fileName in os.listdir(inputFileDir):
        if os.path.isdir(os.path.join(inputFileDir,fileName)):
            dir.append(os.path.join(inputFileDir,fileName))

    for inputFileDir in dir :
        for videoName in os.listdir(inputFileDir):

            originName = videoName
            video = cv2.VideoCapture(inputFileDir + '\\' + videoName)

            encoding = chardet.detect(videoName)['encoding']

            if encoding is None  or (not video.isOpened()):
                video.release()
                logging.info(originName + "can't encoding ")
                cmd = "del " + '"' + inputFileDir + "\\" + originName + '"  '
                os.system(cmd)

            else:
                videoName = unicode(videoName, encoding,'ignore')
                length = int(video.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
                fps = int(video.get(cv2.cv.CV_CAP_PROP_FPS))

                if fps > 0 :
                    videoTime = int(length / fps)
                else:
                    videoTime = 0

                if isCheckResolution:
                    resolution, correct = isCorrectFormat(bias, video.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT), resolutionConfig)
                else:
                    correct = True
                    resolution = 0

                video.release()
                results = db_get_results(conn,table)
                exist,existName = isExist(results,videoName)
                if (videoTime >= minTime) and (not exist) and (videoTime <= maxTime) and correct:
                    rows = [fields]
                    rows.append((videoName, time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))))
                    db_table_add_rows(conn, table, rows, ['videoName'])
                    outputFileDir = dstFile.pop(0)
                    dstFile.append(outputFileDir)
                    print(inputFileDir + u"\\" + originName  + u"  is saved in database will move to " + outputFileDir + u"\\")
                    cmd = "move " + '"' + inputFileDir + "\\" + originName + '"  ' + outputFileDir + "\\"
                    print(cmd)
                    os.system(cmd)

                else:
                    if correct is False:
                        logging.info(inputFileDir + u"\\" + originName + u"  Video resolution error! ")
                        print(inputFileDir + u"\\" + originName + u"  Video resolution error! ")
                    elif videoTime > maxTime:
                        logging.info(inputFileDir + u"\\" + originName + u"  is too long will be deleted")
                        print(inputFileDir + u"\\" + originName + u"  is too long will be deleted")
                    elif videoTime < minTime:
                        logging.info(inputFileDir + u"\\" + originName  + u"  is too short will be deleted")
                        print(inputFileDir + u"\\" + originName  + u"  is too short will be deleted")
                    elif exist and (existName is not None):
                        logging.info(existName + u" is existed "+inputFileDir + u"\\" + videoName  + u" will be deleted")
                        print(inputFileDir + u"\\" + originName  + u"  is existing will be deleted")
                    cmd = "del " + '"' + inputFileDir + "\\" + originName + '"  '
                    os.system(cmd)
    dir = []
    print("please wating ....")
    time.sleep(5)
