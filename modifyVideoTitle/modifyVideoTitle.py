# -*- coding: utf8 -*-
import re
import os
import chardet
import random
from suffix import suffix
from preffix import  preffix
from zhon.hanzi import punctuation as pun
import sys
from sensitive_filter import SensitiveFilter
import string

punctuation = pun + string.punctuation

sf = SensitiveFilter(excludes=["&"])
# print(punctuation)
def getMaxEle(list):
    max = list[0]
    if sf.find_sensitive_words(max):
        max = ""
    for i in list:
        if len(i) > len(max) and  (not sf.find_sensitive_words(i)):
            max = i
    # list.remove(min)
    return max

inputDir = sys.argv[1]


for videoName in os.listdir(inputDir):
    originName = videoName
    newName = []

    pre = random.sample(preffix, 1)[0]
    suff = random.sample(suffix, 1)[0]
    # newName.append(pre)

    encoding = chardet.detect(videoName)['encoding']
    # videoName, type = os.path.splitext(videoName)
    videoName,type = os.path.splitext(unicode(videoName, encoding,'ignore'))
    oldName = videoName

    videoName = re.sub(ur"[%s]+" % punctuation, " ", videoName).split()
    if len(videoName) > 1:
        newName.append(getMaxEle(videoName))
    else:
        newName.append(videoName[0])

    name = u"，".join(newName)

    tryCnt = min(min(len(suffix),len(preffix)),100)
    cnt = 0
    success = False

    while cnt < tryCnt:
        if len(pre + name + suff) < 30:
            name = pre + name + u'，' + suff
            success = True
            break
        else:
            pre = random.sample(preffix, 1)[0]
            suff = random.sample(suffix, 1)[0]

        cnt += 1

    if success is False:
        cnt = 0
        while cnt < tryCnt:
            if len(pre + name) < 30:
                name = pre + name
                success = True
                break
            else:
                pre = random.sample(preffix, 1)[0]

            cnt += 1



    # print(inputDir + "\\" + oldName)
    # print(inputDir + "\\"+ name + type)

    try:
        # os.rename(inputDir + "\\" + oldName + type, inputDir + "\\"+ name + type)
        os.chdir(inputDir)
        os.rename(originName,name + type)
    except Exception, detail:
        os.chdir(inputDir)
        os.remove(originName)

        # cmd = "del " + '"' + inputDir + "\\" + videoName + '"  '
        # os.system(cmd)


