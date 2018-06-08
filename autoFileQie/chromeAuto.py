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

videoType = '娱乐'
selectVideoType = '明星资讯'
# autoit = win32com.client.Dispatch("AutoItX3.Control")

print('loading keyword.....')
keywordLib = pd.read_csv('keyword.csv')
defKeywordLib = pd.read_csv('defaultkeyword.csv')

keywordLib = keywordLib[keywordLib['label'] == videoType]
defKeywordLib = defKeywordLib[defKeywordLib['label'] == videoType]

# keywordLib['keyword'].apply(lambda x : x.decode(chardet.detect(x)['encoding']))
# defKeywordLib['keyword'].apply(lambda x : x.decode(chardet.detect(x)['encoding']))
print('loading keyword finished!')

rootdir = sys.argv[1]

videoNameList = []
def sleep(sec=1):
    time.sleep(sec)

def isTimeOut(startTime):
    if datetime.datetime.now() - startTime > datetime.timedelta(minutes=10):
        return True
    return False

for file in os.listdir(rootdir):
    if file.split('.')[-1] == u'mp4':
        name = file.split('.')[0]
        if os.path.exists(os.path.join(rootdir ,name + '.jpg')):
            name = file.split('.')[0]
            videoNameList.append(name)

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
keywordCnt = 3

for videoName in videoNameList:
    kw = []
    code = chardet.detect(videoName)['encoding']
    if code is not None:
        try:
            for k in keywordLib['keyword']:
                if k in videoName.decode(code):
                    kw.append(k)
                    if len(kw) >= keywordCnt:
                        break
        except:
            pass

    if len(kw) < keywordCnt:
        cnt = keywordCnt - len(kw)
        kw.extend(random.sample(defKeywordLib['keyword'],cnt))
        kw = list(set(kw))

    if len(username_pwd) > 0:

        usename,pwd = username_pwd.pop(0)
        upvideoPath = os.path.join(rootdir ,videoName  + '.mp4')
        viodePicPath = os.path.join(rootdir ,videoName + '.jpg')

        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get("https://om.qq.com/userAuth/index")
        sleep()

        startTime = datetime.datetime.now()
        account=[]
        while len(account) == 0 and not isTimeOut(startTime):
            sleep()
            account = driver.find_elements_by_xpath('//*[@id="screens"]/div[2]/div[4]/div[2]/div[2]/form/div[1]/input')
        if len(account) > 0:
            account[0].send_keys(usename)

        passwd = []
        while len(passwd) == 0 and not isTimeOut(startTime):
            sleep()
            passwd = driver.find_elements_by_xpath('//*[@id="screens"]/div[2]/div[4]/div[2]/div[2]/form/div[2]/input')
        if len(passwd) > 0:
            passwd[0].send_keys(pwd)


        login = []
        while len(login) == 0 and not isTimeOut(startTime):
            sleep()
            login = driver.find_elements_by_xpath('//*[@id="screens"]/div[2]/div[4]/div[2]/div[2]/div[1]/button[1]')
        if len(login) > 0:
            login[0].send_keys(Keys.ENTER)


        sleep(3)
        driver.get('https://om.qq.com/article/articlePublish#/!/view:article?typeName=multivideos')
        # upcontentBtn = []
        # while len(upcontentBtn) == 0 and not isTimeOut(startTime):
        #     sleep()
        #     upcontentBtn = driver.find_elements_by_xpath('/html/body/div[1]/div[2]/div/div/div[1]/ul/li[1]/ul/li[1]')
        #     if (len(upcontentBtn) == 0):
        #         upcontentBtn = driver.find_elements_by_xpath('/html/body/div[1]/div[2]/div/div/div[2]/div[3]/ul/li[3]/span')
        # sleep()
        # if len(upcontentBtn) > 0:
        #     action = ActionChains(driver).move_to_element(upcontentBtn[0]).click().perform()
        # print('click upcontenBtn')

        # publishVideo = []
        # while len(publishVideo) == 0 and not isTimeOut(startTime):
        #     sleep()
        #     publishVideo = driver.find_elements_by_xpath('/html/body/div[1]/div[2]/div/div/div[2]/div[2]/ul/li[3]')
        #     print(publishVideo)
        # sleep()
        # if len(publishVideo) > 0:
        #     action = ActionChains(driver).move_to_element(publishVideo[0]).click().perform()
        # print('click publish')

        chooseVideoBtn=[]
        while len(chooseVideoBtn) == 0  and not isTimeOut(startTime) :
            sleep()
            chooseVideoBtn = driver.find_elements_by_xpath('//*[@id="btn-upload-video"]')

            if len(chooseVideoBtn) > 0:
                action = ActionChains(driver).move_to_element(chooseVideoBtn[0]).click().perform()
                os.system("upfile.exe " + upvideoPath)
        sleep()
        print('click chooseVideo')

        profile = []
        while len(profile) == 0 and not isTimeOut(startTime):
            sleep()
            profile = driver.find_elements_by_xpath('//*[contains(@id,"videoform")]/div[1]/div[2]/div[1]/div/div/div[3]/div/label/textarea')
        if len(profile) > 0:
            action = ActionChains(driver).move_to_element(profile[0]).click().perform()

        sleep()
        clickType = []
        while len(clickType) == 0 and not isTimeOut(startTime):
            try:
                sleep()
                clickType = driver.find_elements_by_tag_name('span')
                for t in clickType:
                    if t.text == '请选择分类':
                        sleep()
                        action = ActionChains(driver).move_to_element(t).click().perform()
                        break
            except:
                pass
        sleep()

        clickType = []
        while len(clickType) == 0 and not isTimeOut(startTime):
            sleep()
            clickType = driver.find_elements_by_xpath('//*[contains(@id,"chosen")]/div/div/input')
            print(clickType)

        if len(clickType) > 0:
            sleep()
            action = ActionChains(driver).move_to_element(clickType[0]).send_keys(videoType.decode(chardet.detect(videoType)['encoding'])).perform()
        sleep()
        print('click type')

        typeSelect = []
        selected = False
        while selected is False and not isTimeOut(startTime):
            sleep()
            typeSelect = driver.find_elements_by_class_name('group-option')

            for t in typeSelect:
                if t.text == selectVideoType:
                    print(t.text)
                    sleep()
                    # t.click()
                    action = ActionChains(driver).move_to_element(t).click().perform()
                    selected = True
                    break
        sleep()

        keyword = []
        while len(keyword) == 0 and not isTimeOut(startTime):
            keyword = driver.find_elements_by_xpath('//*[contains(@id,"videoTags")]')
            sleep()

        if len(keyword) > 0:
            action = ActionChains(driver).move_to_element(keyword[0]).click().perform()
            for k in kw:
                action = ActionChains(driver).move_to_element(keyword[0]).send_keys(k.decode(chardet.detect(k)['encoding'])).perform()
                # keyword[0].send_keys(k.decode(chardet.detect(k)['encoding']))
                # keyword[0].send_keys(Keys.ENTER)
                sleep()

        # keyword = []
        # while len(keyword) == 0 and not isTimeOut(startTime):
        #     keyword = driver.find_elements_by_xpath('//*[contains(@id,"videoform")]/div[1]/div[2]/div[1]/div/div/div[2]/div/ul[2]/li')
        #     cnt = 0
        #     for t in keyword[1:]:
        #         action = ActionChains(driver).move_to_element(t).click().perform()
        #         cnt += 1
        #         if cnt >= 3 :
        #             break
        #         sleep()
        print('Enter keyword!')

        uploadPic = []

        while len(uploadPic) == 0 and not isTimeOut(startTime):
            uploadPic = driver.find_elements_by_xpath('//*[contains(@id,"videoform")]/div[1]/div[2]/div[2]/div/div[3]/button')
            print(uploadPic)
        if len(uploadPic) > 0:
            action = ActionChains(driver).move_to_element(uploadPic[0]).click().perform()

        sleep()
        uploadPic = []
        while len(uploadPic) == 0 and not isTimeOut(startTime):
            uploadPic = driver.find_elements_by_xpath('//*[@id="layui-layer1"]/div[2]/span/div[1]/div/ul/li[2]/span')
        if len(uploadPic) > 0:
            action = ActionChains(driver).move_to_element(uploadPic[0]).click().perform()

        sleep()
        uploadPic = []
        while len(uploadPic) == 0 and not isTimeOut(startTime):
            uploadPic = driver.find_elements_by_xpath('//*[contains(@id,"rt_rt")]/label')
        if len(uploadPic) > 0:
            action = ActionChains(driver).move_to_element(uploadPic[0]).click().perform()
            os.system("upfile.exe " + viodePicPath)

        sleep()
        uploadPic = []
        while len(uploadPic) == 0 and not isTimeOut(startTime):
            uploadPic = driver.find_elements_by_xpath('//*[@id="layui-layer1"]/div[2]/span/div[2]/button[1]')
        if len(uploadPic) > 0:
            action = ActionChains(driver).move_to_element(uploadPic[0]).click().perform()

        sleep()
        publish = []
        published = False
        while True and not isTimeOut(startTime):
            sleep()
            try:
                publish = driver.find_element_by_xpath('//*[@id="mod-actions"]/div/button')
                print(publish)
                if publish :
                    published = True
                    action = ActionChains(driver).move_to_element(publish).click().perform()
                    sleep(10)
            except:
                if published:
                    break;
        print('click publish video !')

        sleep()
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

with open('finished', 'a') as f:
    f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\t' + "published:\t" + str(total) + "\tviodes" + '\n')

