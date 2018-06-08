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
import shutil

inputDir = sys.argv[1]
outputDir = sys.argv[2]
needSuff = int(sys.argv[3])

if needSuff == 1:
    needSuff = True
else:
    needSuff =False


punctuation = pun + string.punctuation

punctuation = u"＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｢｣､　、〃〈〉「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏﹑﹔·！？｡。!#$%&'()*+,-./:;<=>?@[\]^_`{|}"


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

def delMinEle(list):
    min = list[0]
    if sf.find_sensitive_words(min):
        min = ""
    for i in list:
        if len(i) < len(min) and  (not sf.find_sensitive_words(i)):
            min = i
    list.remove(min)
    return list

def getStrLen(s):

    i = 0;cnt = 0;
    while i < len(s):
        try:
            if s[i] >= u'u4e00' and s[i] <= u'u9fa5':
                pass
            cnt += 1;i += 1
        except:
            cnt += 1;i += 3
    return cnt


for videoName in os.listdir(inputDir):
    try:
        originName = videoName
        newName = []

        # newName.append(pre)
        encoding = chardet.detect(videoName)['encoding']

        videoName,type = os.path.splitext(unicode(videoName, encoding,'ignore'))
        oldName = videoName

        videoName = re.sub(ur"[%s]+" % punctuation, " ", videoName).split()

        if len(videoName) < 3: #1.2
            for i in range(len(suffix)):
                s = random.sample(suffix, 1)[0]
                if getStrLen(name + u'，' + s) < 30:
                    name = name + u'，' + s
                    break
        else:
            newName = delMinEle(videoName)
            while getStrLen(u"，".join(newName)) > 30 and len(videoName) > 1:
                newName = delMinEle(newName)

            if needSuff:
                for i in range(len(suffix)):
                    s = random.sample(suffix, 1)[0]
                    if getStrLen(name + u'，' + s) < 30:
                        name = name + u'，' + s
                        break

        os.chdir(inputDir)
        name = name + type
        os.rename(originName,name)
        shutil.move(name, os.path.join(outputDir,name))
        print (name)
    except:
        # os.chdir(inputDir)
        # os.remove(originName)
        pass
        # os.chdir(inputDir)
        # os.remove(originName)






