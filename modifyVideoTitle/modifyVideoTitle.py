# -*- coding: utf8 -*-
import re
import os
import chardet
import random
from suffix import suffix
from preffix import  preffix
from zhon.hanzi import punctuation as pun
import sys

punctuation = pun + u'_'
def deleteMinLen(list):

    min = list[0]
    for i in list:
        if len(i) < len(min):
            min = i

    list.remove(min)
    return list

inputDir = sys.argv[1]

for videoName in os.listdir(inputDir):

    newName = []

    pre = random.sample(preffix, 1)[0]
    suff = random.sample(suffix, 1)[0]
    newName.append(pre)

    encoding = chardet.detect(videoName)['encoding']
    # videoName, type = os.path.splitext(videoName)
    videoName,type = os.path.splitext(unicode(videoName, encoding,'ignore'))
    oldName = videoName

    videoName = re.sub(ur"[%s]+" %punctuation, " ", videoName).split()
    if len(videoName) > 1:
        newName.extend( deleteMinLen(videoName))
    else:
        newName.append(oldName)

    newName.append(suff)

    name = ",".join(newName)
    print(inputDir + "\\" + oldName)
    print(inputDir + "\\"+ name + type)

    # os.rename(inputDir + "\\" + oldName + type, inputDir + "\\"+ name + type)

