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
    if datetime.datetime.now() - startTime > datetime.timedelta(minutes=1):
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

for videoName in videoNameList:
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
        driver.get("http://creator.miaopai.com/login")
        sleep()

        startTime = datetime.datetime.now()
        account=[]
        while len(account) == 0 and not isTimeOut(startTime):
            sleep()
            account = driver.find_elements_by_xpath('/html/body/div/div/span/main/main/div/section/div/div[2]/div[4]/form/div[1]/input')
        if len(account) > 0:
            account[0].send_keys(usename)

        passwd = []
        while len(passwd) == 0 and not isTimeOut(startTime):
            sleep()
            passwd = driver.find_elements_by_xpath('/html/body/div/div/span/main/main/div/section/div/div[2]/div[4]/form/div[2]/input')
        if len(passwd) > 0:
            passwd[0].send_keys(pwd)


        login = []
        while len(login) == 0 and not isTimeOut(startTime):
            sleep()
            login = driver.find_elements_by_xpath('/html/body/div/div/span/main/main/div/section/div/div[2]/div[4]/form/button')
        if len(login) > 0:
            login[0].send_keys(Keys.ENTER)

        upvideoBtn = []
        while len(upvideoBtn) == 0 and not isTimeOut(startTime):
            sleep()
            upvideoBtn = driver.find_elements_by_xpath('//*[@id="creator-main"]/div[1]/div[2]/ul/li[2]/ul/li')
        sleep()
        try:
            upvideoBtn[0].click()  # upvideo
        except:
            dialog_btn = driver.find_elements_by_xpath('//*[@id="creator-home"]/div[3]/div/div[3]/span/button')
            if len(dialog_btn) > 0:
                action = ActionChains(driver).move_to_element(dialog_btn[0]).click().perform()
                sleep()
            # upvideoBtn = []
            # while len(upvideoBtn) == 0 and not isTimeOut(startTime):
            #     sleep()
            #     upvideoBtn = driver.find_elements_by_xpath('/html/body/div/div/span/main/div/div[1]/div[2]/ul/li[2]')
            # sleep()
            # upvideoBtn[0].click()  # upvideo

        chooseVideoBtn=[]
        while len(chooseVideoBtn) == 0  and not isTimeOut(startTime) :
            sleep()
            chooseVideoBtn = driver.find_elements_by_xpath('//*[@id="uploadVideo"]')
        sleep()
        if len(chooseVideoBtn) > 0:
            action = ActionChains(driver).move_to_element(chooseVideoBtn[0]).click().perform()

        # autoit.Run("upfile.exe " + upvideoPath)
        os.system("upfile.exe " + upvideoPath)

        sleep()
        canUpfile = True
        upVideoPic = []
        cnt = 10
        while len(upVideoPic) == 0  and not isTimeOut(startTime) :
            cnt -= 1
            try:
                msg = driver.find_element_by_class_name('el-message-box__message')
                print(msg.text)
                if msg is not None or cnt < 0:
                    canUpfile = False
                    break
            except:
                print('not found')
                upVideoPic = driver.find_elements_by_xpath('//*[@id="uploadMyMark"]')

            sleep()

        sleep()

        if isTimeOut(startTime):
            canUpfile = False

        if canUpfile:
            sleep()
            if(len(upVideoPic) > 0):
                action = ActionChains(driver).move_to_element(upVideoPic[0]).click().perform()
                # autoit.Run("upfile.exe " + viodePicPath)
                os.system("upfile.exe " + viodePicPath)
            sleep()


            # pubulishCheck = []
            # while len(pubulishCheck) == 0 and not isTimeOut(startTime):
            #     pubulishCheck = driver.find_elements_by_xpath('//*[@id="upload_info"]/div/div[2]/div[2]/label/span[1]/input')
            # sleep()
            # if len(pubulishCheck) > 0:
            #     # pubulishCheck[0].send_keys(Keys.SPACE)
            #     action = ActionChains(driver).move_to_element(pubulishCheck[0]).click().perform()
            # sleep()

            picFinishBtn = []

            while len(picFinishBtn) == 0 and not isTimeOut(startTime) :
                picFinishBtn = driver.find_elements_by_xpath('//*[@id="cutMark"]/div/div[3]/span/button')
            sleep()
            if len(picFinishBtn) > 0:
                picFinishBtn[0].click()


            typeInput = []
            while len(typeInput) == 0 and not isTimeOut(startTime):
                sleep()
                typeInput = driver.find_elements_by_xpath('/html/body/div[1]/div/span/main/div/div[3]/div/div/div[2]/div/div[3]/div[2]/div[2]/form/div[3]/div/div/div[1]/div[1]/input')
            if len(typeInput) > 0:
                typeInput[0].click()

            typeSelect = []
            while len(typeSelect) == 0 and not isTimeOut(startTime):
                sleep()
                typeSelect = driver.find_elements_by_xpath('//ul[@class="el-select-group"]/li')

            for t in typeSelect:
                if t.text == videoType:
                    sleep()
                    t.click()
                    break

            keyword = []
            while len(keyword) == 0  and not isTimeOut(startTime) :
                keyword = driver.find_elements_by_xpath('//*[@id="upload_info"]/div/div[3]/div[2]/div[2]/form/div[6]/div')
                sleep()

            if len(keyword) > 0:
                action = ActionChains(driver).move_to_element(keyword[0]).click().perform()

            keyword = []
            while len(keyword) == 0  and not isTimeOut(startTime) :
                keyword = driver.find_elements_by_xpath('//*[@id="upload_info"]/div/div[3]/div[2]/div[2]/form/div[7]/div[1]/div/div/ul/li/div/input')
                sleep()

            if len(keyword) > 0:
                action = ActionChains(driver).move_to_element(keyword[0]).click().perform()
                for k in kw:
                    keyword[0].send_keys(k.decode(chardet.detect(k)['encoding']))
                    keyword[0].send_keys(Keys.ENTER)
                    sleep()

            keyword = []
            while len(keyword) == 0 and not isTimeOut(startTime):
                keyword = driver.find_elements_by_xpath('//*[@id="upload_info"]/div/div[3]/div[2]/div[2]/form/div[7]/div[2]/div/div/input')
                sleep(1)
            if len(keyword) > 0:
                action = ActionChains(driver).move_to_element(keyword[0]).click().perform()
                for k in kw:
                    keyword[0].send_keys(k.decode(chardet.detect(k)['encoding']))
                    keyword[0].send_keys(Keys.ENTER)
                    sleep(1)

            progress_bar = []
            while len(progress_bar) == 0 and not isTimeOut(startTime):
                progress_bar = driver.find_elements_by_xpath('/html/body/div[1]/div/span/main/div/div[3]/div/div/div[2]/div/div[3]/div[2]/div[2]/div/div[2]')
            while True and not isTimeOut(startTime):
                if len(progress_bar) > 0:
                    if u'上传成功' in progress_bar[0].text:
                        break
            sleep(3)

            # publish = []
            # while len(publish) == 0 and not isTimeOut(startTime):
            #     publish = driver.find_elements_by_xpath('//*[@id="upload_info"]/div/div[2]/div[2]/button')
            #     sleep()
            # sleep()
            # if(len(publish) > 0):
            #     action = ActionChains(driver).move_to_element(publish[0]).click().perform()
            # sleep()

            titleError = False
            while True and not isTimeOut(startTime):
                try:
                    if driver.find_elements_by_xpath('//*[@id="upload_info"]/div/div[2]/div[2]/button')[0].text != '全部发布':
                        break
                    else:
                        publish = driver.find_elements_by_xpath('//*[@id="upload_info"]/div/div[2]/div[2]/button')
                        sleep()
                        if (len(publish) > 0):
                            action = ActionChains(driver).move_to_element(publish[0]).click().perform()

                            err = driver.find_elements_by_xpath('//*[@id="upload_info"]/div/div[3]/div[2]/div[2]/form/div[1]/div/div[2]')[0]
                            if err:
                                errLog = err.text

                                if '重复'in errLog:
                                    errLog = 'title is duplicate!'
                                    duplicateTotal += 1
                                elif'短标题' in errLog:
                                    errLog = 'title too long!'
                                    toolongTotal += 1
                                elif '占用' in errLog:
                                    errLog = 'title be occupied'
                                    duplicateTotal += 1
                                else:
                                    errLog = 'title error'
                                    duplicateTotal += 1

                                print(errLog)
                                titleError = True
                                break

                        sleep()

                except:
                    pass
            sleep(5)

            if isTimeOut(startTime):
                videoNameList.append(videoName)
                driver.quit()
                continue
            driver.quit()

            os.remove(upvideoPath)
            os.remove(viodePicPath)

            if titleError is False:

                with open('published','a') as f:
                    f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\t' + usename +"\tpublished:\t" +  videoName +  '\n')
                total +=1
            else:
                with open('error','a') as f:
                    f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\t' + usename +"\tpublished:\t" +  videoName + '\t' + errLog +  '\n')
                username_pwd.append((usename,pwd))
                pass
        else:
            driver.quit()
            videoNameList.append(videoName)

            if not isTimeOut(startTime):
                temp = []
                for e in username_pwd:
                    if e[0] != usename:
                        temp.append(e)
                username_pwd = temp
    else:
        break

with open('finished', 'a') as f:
    f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\t' + "published:\t" + str(total) + "\tviodes" + '\n')
    f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\t' + "title duplicate:\t" + str(duplicateTotal) + "\tviodes" + '\n')
    f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\t' + "title too long :\t" + str(toolongTotal) + "\tviodes" + '\n')







