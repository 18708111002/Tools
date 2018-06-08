# # -*- coding:utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import datetime
import datetime
import os
import time
import sys
import pandas as pd
import random
import chardet
import win32com.client
reload(sys)
sys.setdefaultencoding("utf-8" )
import re

typeMap = {'明星':'娱乐','八卦':'娱乐'}
videoTypeList = ['明星', '八卦']


# autoit = win32com.client.Dispatch("AutoItX3.Control")

print('loading keyword.....')
keywordLib = pd.read_csv('keyword.csv')
defKeywordLib = pd.read_csv('defaultkeyword.csv')

keywordLib = keywordLib[keywordLib['label'] == typeMap[videoTypeList[0]]]
defKeywordLib = defKeywordLib[defKeywordLib['label'] == typeMap[videoTypeList[0]]]


# keywordLib['keyword'].apply(lambda x : x.decode(chardet.detect(x)['encoding']))
# defKeywordLib['keyword'].apply(lambda x : x.decode(chardet.detect(x)['encoding']))
print('loading keyword finished!')

rootdir = sys.argv[1]

videoNameList = []
def sleep(sec=1):
    time.sleep(sec)

import chardet

def getStrLen(s):
    gap = 3
    if (chardet.detect(s)['encoding'] == 'GB2312'):
        gap = 2

    i = 0;cnt = 0;
    while i < len(s):
        try:
            if s[i] >= u'u4e00' and s[i] <= u'u9fa5':
                pass
            cnt += 1;i += 1
        except:
            cnt += 1;i += gap
    return cnt

def isTimeOut(startTime):
    if datetime.datetime.now() - startTime > datetime.timedelta(minutes=5):
        return True
    return False

total = 0
for file in os.listdir(rootdir):
    canAppend = True
    cnt = 0
    try:
        if file.split('.')[-1] == u'mp4':
            name = file.split('.')[0]
            if os.path.exists(os.path.join(rootdir ,name + '.jpg')):
                for w in name:
                    if w.isspace():
                        canAppend = False
                cnt = getStrLen(name)
                if cnt < 30 and cnt > 8 and canAppend:
                    videoNameList.append(name)
    except:
        pass

random.shuffle(videoNameList)

username_pwd = []

with open('account','r') as f:
    for line in f:
        u = line.split()[0]
        p = line.split()[1]
        cnt = int(line.split()[2])
        while cnt > 0:
            username_pwd.append((u,p))
            cnt -= 1
total = 0
duplicateTotal  = 0
toolongTotal = 0

for videoName in videoNameList:
    try:
        kw = []
        code = chardet.detect(videoName)['encoding']
        if code is not None:
            try:
                for k in keywordLib['keyword']:
                    if k in videoName.decode(code):
                        kw.append(k)
                        if len(kw) >= 3:
                            break
            except:
                pass

        if len(kw) < 3:
            cnt = 3 - len(kw)
            kw.extend(random.sample(defKeywordLib['keyword'],cnt))
            kw = list(set(kw))

        if len(username_pwd) > 0:

            usename,pwd = username_pwd.pop(0)
            upvideoPath = os.path.join(rootdir ,videoName  + '.mp4')
            viodePicPath = os.path.join(rootdir ,videoName + '.jpg')

            driver = webdriver.Chrome()
            driver.maximize_window()
            driver.get("https://mp.qutoutiao.net/login")
            sleep()

            startTime = datetime.datetime.now()
            account=[]
            while len(account) == 0 and not isTimeOut(startTime):
                sleep()
                account = driver.find_elements_by_xpath('//*[@id="app"]/div[2]/div[11]/div/div[2]/form/div[1]/div/input')
            if len(account) > 0:
                account[0].send_keys(usename)

            passwd = []
            while len(passwd) == 0 and not isTimeOut(startTime):
                sleep()
                passwd = driver.find_elements_by_xpath('//*[@id="app"]/div[2]/div[11]/div/div[2]/form/div[2]/div/input')
            if len(passwd) > 0:
                passwd[0].send_keys(pwd)


            login = []
            while len(login) == 0 and not isTimeOut(startTime):
                sleep()
                login = driver.find_elements_by_xpath('//*[@id="submit-login"]')
            if len(login) > 0:
                login[0].send_keys(Keys.ENTER)


                    # know_diaglog = driver.find_elements_by_xpath('/html/body/div[4]/div')
                    # if len(know_diaglog) > 0:
                    #     know_diaglog = driver.find_elements_by_xpath('/html/body/div[4]/div/div[3]/button[2]')
                    #     sleep()
                    #     action = ActionChains(driver).move_to_element(know_diaglog[0]).click().perform()
            # print('click upcontentbutton!')
            task = []
            while len(task) == 0 and not isTimeOut(startTime):
                sleep()

                dialog_btn = driver.find_elements_by_xpath('/html/body/div[4]/div/div[1]/button')
                if len(dialog_btn) > 0:
                    action = ActionChains(driver).move_to_element(dialog_btn[0]).click().perform()
                    sleep()

                task = driver.find_elements_by_xpath('//*[@id="app"]/div[2]/div[1]/div/div[1]/div[2]/div[1]/div')

            print('click task button!')

            if len(task) > 0:
                sleep()
                dialog_btn = driver.find_elements_by_xpath('/html/body/div[4]/div/div[1]/button')
                if len(dialog_btn) > 0:
                    action = ActionChains(driver).move_to_element(dialog_btn[0]).click().perform()
                    sleep()
                action = ActionChains(driver).move_to_element(task[0]).click().perform()
                sleep()

                cnt = 3
                task = []
                while cnt > 0 and len(task) == 0  and not isTimeOut(startTime):
                    sleep()
                    task = driver.find_elements_by_xpath('//*[@id="app"]/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/div[1]/button')
                    cnt -= 1

                if len(task) > 0:
                    sleep()
                    action = ActionChains(driver).move_to_element(task[0]).click().perform()

                sleep()
                upcontentBtn = []
                while len(upcontentBtn) == 0 and not isTimeOut(startTime):
                    sleep()
                    upcontentBtn = driver.find_elements_by_xpath('//*[@id="app"]/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/div[2]/div/div[1]/button')
                    if len(upcontentBtn) > 0:
                        action = ActionChains(driver).move_to_element(upcontentBtn[0]).click().perform()
            else:
                upcontentBtn = []
                while len(upcontentBtn) == 0 and not isTimeOut(startTime):
                    sleep()
                    upcontentBtn = driver.find_elements_by_xpath('//*[@id="app"]/div[2]/div[2]/div/div[1]/div[2]/div[1]/span[2]')
                    if len(upcontentBtn) > 0:
                        action = ActionChains(driver).move_to_element(upcontentBtn[0]).click().perform()

            # print('start knowdialog')
            # sleep()
            # know_diaglog = []
            # while len(know_diaglog) == 0 and not isTimeOut(startTime):
            #     sleep()
            #     know_diaglog = driver.find_elements_by_xpath('/html/body/div[4]/div')
            #     if len(know_diaglog) > 0:
            #         know_diaglog = driver.find_elements_by_xpath('/html/body/div[4]/div/div[3]/button[2]')
            #         sleep()
            #         if len(know_diaglog) > 0:
            #             action = ActionChains(driver).move_to_element(know_diaglog[0]).click().perform()
            # print('click knowdialog!')
            #
            # upvideoBtn = []
            # while len(upvideoBtn) == 0 and not isTimeOut(startTime):
            #     sleep()
            #     upvideoBtn = driver.find_elements_by_xpath('//*[@id="app"]/div[2]/div[2]/div/div[2]/div/div[1]/div[1]/p[2]')
            # sleep()
            # try:
            #     upvideoBtn[0].click()  # upvideo
            # except:
            #     know_diaglog = driver.find_elements_by_xpath('/html/body/div[4]/div')
            #     if len(know_diaglog) > 0:
            #         know_diaglog = driver.find_elements_by_xpath('/html/body/div[4]/div/div[3]/button[2]')
            #         sleep()
            #         action = ActionChains(driver).move_to_element(know_diaglog[0]).click().perform()
            # print('click upvideobutton!')
            sleep()
            driver.get('https://mp.qutoutiao.net/publish-content/video')

            chooseVideoBtn=[]
            while len(chooseVideoBtn) == 0  and not isTimeOut(startTime) :
                sleep()
                chooseVideoBtn = driver.find_elements_by_xpath('//*[@id="inp-video-file"]')

                if len(chooseVideoBtn) > 0:

                    sleep()
                    dialog_btn = driver.find_elements_by_xpath('/html/body/div[3]/div/div[1]/button')
                    if len(dialog_btn) > 0:
                        action = ActionChains(driver).move_to_element(dialog_btn[0]).click().perform()
                        sleep()

                    canpublish = []
                    while len(canpublish) == 0 and not isTimeOut(startTime):
                        canpublish = driver.find_elements_by_xpath('//*[@id="app"]/div[2]/div[2]/div/div[2]/div/div[1]/div[2]')
                    if len(canpublish) > 0:
                        if int(re.findall("\d+", canpublish[0].text)[0]) > 0:
                            canUpfile = True
                        else:
                            canUpfile = False

                    action = ActionChains(driver).move_to_element(chooseVideoBtn[0]).click().perform()
                    os.system("upfile.exe " + upvideoPath)
            sleep()
            print('click chooseVideobutton!')

            if canUpfile:
                upVideoPic = []
                while len(upVideoPic) == 0  and not isTimeOut(startTime) :
                    sleep()
                    upVideoPic = driver.find_elements_by_xpath('//*[@id="app"]/div[2]/div[2]/div/div[2]/div/div[2]/div/div[1]/div/div[2]/div[1]/form/div[4]/div/div[1]')
                if (len(upVideoPic) > 0):
                    action = ActionChains(driver).move_to_element(upVideoPic[0]).click().perform()
                print('click  upvideoPicbutton!')

                customPic = []
                while len(customPic) == 0 and not isTimeOut(startTime):
                    sleep()
                    customPic = driver.find_elements_by_xpath('//*[@id="app"]/div[2]/div[2]/div/div[2]/div/div[2]/div/div[2]/div/div[1]/div/p[1]')
                if (len(customPic) > 0):
                    action = ActionChains(driver).move_to_element(customPic[0]).click().perform()
                print('click customPicbutton!')

                choosePicBtn = []
                while len(choosePicBtn) == 0 and not isTimeOut(startTime):
                    sleep()
                    choosePicBtn = driver.find_elements_by_xpath('//*[@id="app"]/div[2]/div[2]/div/div[2]/div/div[2]/div/div[2]/div/div[2]/div[1]/div/div[2]/div/button')
                if (len(choosePicBtn) > 0):
                    action = ActionChains(driver).move_to_element(choosePicBtn[0]).click().perform()
                    os.system("upfile.exe " + viodePicPath)
                print('click choosePicbutton!')

                picOkbtn = []
                while len(picOkbtn) == 0 and not isTimeOut(startTime):
                    sleep()
                    picOkbtn = driver.find_elements_by_xpath('//div[@class="dialog-footer"]/button[@class="el-button el-button--primary"]/span')
                    if (len(picOkbtn) > 0):
                        for btn in picOkbtn:
                            action = ActionChains(driver).move_to_element(btn).click().perform()
                print('click okButton!')

                keyword = []
                while len(keyword) == 0 and not isTimeOut(startTime):
                    keyword = driver.find_elements_by_xpath('//*[@id="app"]/div[2]/div[2]/div/div[2]/div/div[2]/div/div[1]/div/div[2]/div[1]/form/div[3]/div/div[1]/div/input')
                    sleep(1)
                    if len(keyword) > 0:
                        action = ActionChains(driver).move_to_element(keyword[0]).click().perform()
                        for k in kw:
                            keyword[0].send_keys(k.decode(chardet.detect(k)['encoding']))
                            keyword[0].send_keys(Keys.ENTER)
                            sleep(1)
                print('Enter keyword!')

                sleep()
                clickType = []
                while len(clickType) == 0 and not isTimeOut(startTime):
                    sleep()
                    clickType = driver.find_elements_by_xpath('//*[@id="app"]/div[2]/div[2]/div/div[2]/div/div[2]/div/div[1]/div/div[2]/div[1]/form/div[2]/div/div[1]/div[2]/div/input')
                sleep(3)
                if (len(clickType) > 0):
                    action = ActionChains(driver).move_to_element(clickType[0]).click().perform()
                print('click typyinput!')

                typeSelect = []
                while len(typeSelect) == 0 and not isTimeOut(startTime):
                    sleep()
                    typeSelect = driver.find_elements_by_class_name('category-items')

                for t in typeSelect:
                    if typeMap[videoTypeList[0]] in t.text:
                        t = t.find_elements_by_tag_name('dd')
                        for tt in t:
                            if tt.text in videoTypeList:
                                print('choose type ' + tt.text)
                                sleep()
                                tt.click()

                progress_bar = []
                while len(progress_bar) == 0 and not isTimeOut(startTime):
                    progress_bar = driver.find_elements_by_xpath('//*[@id="app"]/div[2]/div[2]/div/div[2]/div/div[2]/div/div[1]/div/div[1]/div[3]')
                while True and not isTimeOut(startTime):
                    if len(progress_bar) > 0:
                        if u'上传成功' in progress_bar[0].text:
                            break
                sleep(3)
                print('upload bar successful!')

                publish = []
                while len(publish) == 0 and not isTimeOut(startTime):
                    publish = driver.find_elements_by_xpath('//*[@id="app"]/div[2]/div[2]/div/div[2]/div/div[2]/div/div[1]/div/div[3]/button[1]')
                    sleep()
                sleep()
                if(len(publish) > 0):
                    action = ActionChains(driver).move_to_element(publish[0]).click().perform()
                sleep()
                print('click publish video !')


                publish = []
                msg = []
                while len(publish) == 0 and not isTimeOut(startTime):
                    msg = driver.find_elements_by_xpath('/html/body/div[5]/div/div[3]/button[2]')
                    if len(msg) > 0 :
                        action = ActionChains(driver).move_to_element(msg[0]).click().perform()
                        sleep()
                    sleep()
                    publish = driver.find_elements_by_xpath('//*[@id="app"]/div[2]/div[2]/div/div[2]/div/div[2]/div/div[3]/div/div[3]/div/button[2]')
                    sleep()
                sleep()
                if(len(publish) > 0):
                    action = ActionChains(driver).move_to_element(publish[0]).click().perform()
                print('click publish video !')

                error = False

                if isTimeOut(startTime):
                    videoNameList.append(videoName)
                    driver.quit()
                    continue
                driver.quit()

                os.remove(upvideoPath)
                os.remove(viodePicPath)
        #
                if error is False:
                    with open('published','a') as f:
                        f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\t' + usename + "\tpublished:\t" + videoName + '\n')
                        total += 1
                else:
                     pass
                     # with open('error','a') as f:
                     #     f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\t' + usename +"\tpublished:\t" +  videoName + '\t' + errLog +  '\n')
                     # username_pwd.append((usename,pwd))
                     # pass
            else:
                driver.quit()
                videoNameList.append(videoName)

                if not isTimeOut(startTime):
                    temp = []
                    for e in username_pwd:
                        if e[0] != usename:
                            temp.append(e)
                    username_pwd = temp
    #     else:
    #         break
    except:
        driver.quit()
        username_pwd.append((usename,pwd))
        videoNameList.append(videoName)
        pass

with open('finished', 'a') as f:
    f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\t' + "published:\t" + str(total) + "\tviodes" + '\n')
    # f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\t' + "title duplicate:\t" + str(duplicateTotal) + "\tviodes" + '\n')
    # f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\t' + "title too long :\t" + str(toolongTotal) + "\tviodes" + '\n')







