# # -*- coding:utf-8 -*-
import requests
import math
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
import cv2
import scipy as sp
import win32com.client
reload(sys)
sys.setdefaultencoding("utf-8" )
import re
from PIL import Image


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
    if datetime.datetime.now() - startTime > datetime.timedelta(minutes=5):
        return True
    return False

def realign(imgpath,x1,x2,height,width,w,h):
    i = 0
    im = Image.open(imgpath)
    # im.show()
    nim = Image.new('RGB',(w,h))
    for x,y in zip(x1,y1):
        # print(x,y)
        box = (x,y,width+x,height+y)
        pastebox = (i,0,width+i,height)
        imx = im.crop(box)
        # imx.show()
        nim.paste(imx,pastebox)
        i = i + width
    # nim.show()
    i = 0
    #
    for x,y in zip(x2,y2):
        box = (x,y,x+width,height+y)
        pastebox = (i,height,i+width,h)
        imx = im.crop(box)
        nim.paste(imx,pastebox)
        i = i +width
    # nim.show()
    return nim

def getint(a):
    p = []
    while sum(p)< a:
        v = random.randint(1,5)
        p.append(v)
    p[-1] = p[-1]-3
    return p

def getOffset():
    img1 = cv2.imread('jigsaw.png', 0)  # queryImage
    img2 = cv2.imread('train.jpg', 0)  # trainImage

    # Initiate SIFT detector
    sift = cv2.SIFT()

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)

    # FLANN parameters
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)  # or pass empty dictionary
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)

    # print 'matches...', len(matches)
    # Apply ratio test
    good = []
    for m, n in matches:
        if m.distance < 0.8 * n.distance:
            good.append(m)
    # print 'good', len(good)
    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]

    view = sp.zeros((max(h1, h2), w1 + w2, 3), sp.uint8)
    view[:h1, :w1, 0] = img1
    view[:h2, w1:, 0] = img2
    view[:, :, 1] = view[:, :, 0]
    view[:, :, 2] = view[:, :, 0]
    total  = 0
    distance = 0
    for m in good:
        total += 1
        # draw the keypoints
        # print m.queryIdx, m.trainIdx, m.distance
        color = tuple([sp.random.randint(0, 255) for _ in xrange(3)])
        # print 'kp1,kp2',kp1,kp2
        # print(kp2)
        # print(int(kp2[m.trainIdx].pt[0]), int(kp2[m.trainIdx].pt[1]))
        # print((int(kp1[m.queryIdx].pt[0]), int(kp1[m.queryIdx].pt[1])))
        cv2.line(view, (int(kp1[m.queryIdx].pt[0]), int(kp1[m.queryIdx].pt[1])),
                 (int(kp2[m.trainIdx].pt[0] + w1), int(kp2[m.trainIdx].pt[1])), color)
        distance += (int(kp2[m.trainIdx].pt[0])) - (int(kp1[m.queryIdx].pt[0]))

    # cv2.imshow("view", view)
    if total == 0:
        distance = random.randint(100,214)
    else:
        distance = distance / total
    return distance



def downloadimage(image_url,path):
    dir_path = path
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    us = image_url[image_url.rfind('/'):]
    image_file_path = dir_path
    with open(image_file_path, 'wb') as handle:
        response = requests.get(image_url, stream=True)
        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)
        return image_file_path

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
        driver.get("http://www.iqiyi.com/iframe/loginreg")
        current_handle = driver.current_window_handle
        sleep()

        startTime = datetime.datetime.now()

        change = []
        while len(change) == 0 and not isTimeOut(startTime):
            sleep()
            change = driver.find_elements_by_xpath('/html/body/div[2]/div[1]/div/div/div[6]/div[2]/p/span/a[1]')
        if len(change) > 0:
            action = ActionChains(driver).move_to_element(change[0]).click().perform()

        account=[]
        while len(account) == 0 and not isTimeOut(startTime):
            sleep()
            account = driver.find_elements_by_xpath('/html/body/div[2]/div[1]/div/div/div[1]/div[1]/div/div[1]/div[2]/input')
        if len(account) > 0:
            account[0].send_keys(usename)

        passwd = []
        while len(passwd) == 0 and not isTimeOut(startTime):
            sleep()
            passwd = driver.find_elements_by_xpath('/html/body/div[2]/div[1]/div/div/div[1]/div[1]/div/div[2]/div/input[1]')
        if len(passwd) > 0:
            passwd[0].send_keys(pwd)


        login = []
        while len(login) == 0 and not isTimeOut(startTime):
            sleep()
            login = driver.find_elements_by_xpath('/html/body/div[2]/div[1]/div/div/div[1]/div[1]/div/a[2]')
        if len(login) > 0:
            action = ActionChains(driver).move_to_element(login[0]).click().perform()


#####破解滑块验证码######
        while True:
            if  'login' not in driver.current_url:
                break
            try:
                if driver.find_element_by_xpath('//*[@id="nav_uploadHref"]').text == '上传':
                    print('find upload')
                    break
            except:
                try:
                    bg_slice = []
                    while len(bg_slice) == 0 and not isTimeOut(startTime):
                        sleep()
                        bg_slice = driver.find_elements_by_xpath('//*[@id="slidePiccode"]/div/div[1]/div[1]/div/div')

                    urlPattern = re.compile(r'"(.+)"')
                    pattern = re.compile(r'([-0-9]+)px')
                    x1 = [];y1 = [];x2 = [];y2 = []
                    # print(bg_slice[-1])
                    jigsawUrl = urlPattern.findall(bg_slice[-1].get_attribute('style'))[0]
                    # print(jigsawUrl)
                    bgurl = None
                    for bg in bg_slice[:-1]:
                        line = bg.get_attribute('style')
                        if bgurl is None:
                            bgurl = urlPattern.findall(line)[0]

                        x1.append(abs(int(pattern.findall(line)[0])))
                        y1.append(abs(int(pattern.findall(line)[1])))
                        width = int(pattern.findall(line)[2])
                        height = int(pattern.findall(line)[3])

                    x2 = x1[len(x1) / 2:]; y2 = y1[len(y1) / 2:]
                    x1 = x1[:len(x1) / 2]; y1 = y1[:len(y1) / 2]

                    downloadimage(bgurl,'./bg.jpg')
                    downloadimage(jigsawUrl, './jigsaw.png')
                    realign('bg.jpg', x1, x2, height, width, 360, 214).save('train.jpg')
                    distance = getOffset()

                    slider = []
                    while len(slider) == 0 and not isTimeOut(startTime):
                        sleep()
                        slider = driver.find_elements_by_xpath('//*[@id="slidePiccode"]/div/div[2]/div[2]')
                    if len(slider) > 0:
                        slider = slider[0]
                        actions = ActionChains(driver)
                        actions.click_and_hold(slider).perform()  # 按住滑块
                        p = getint(distance)

                        for i in p:
                            actions = ActionChains(driver)
                            actions.move_by_offset(i, int(math.sin(i) * 10)).perform()
                            time.sleep(0.05 + 0.001 * abs(math.sin(i)))
                        actions = ActionChains(driver)
                        actions.release().perform()
                        time.sleep(0.1)
                        actions = ActionChains(driver)
                        actions.move_by_offset(0, 200).perform()

                        sleep(2)
                        refreash = driver.find_elements_by_xpath('//*[@id="slidePiccode"]/div/div[1]/div[1]/button[1]')
                        if len(refreash) > 0:
                            refreash[0].click()
                except:
                    pass
#####破解滑块验证码######
        sleep()
        driver.get('http://mp.iqiyi.com/publish/videoUpload')

#         upcontentBtn = []
#         while len(upcontentBtn) == 0 and not isTimeOut(startTime):
#             sleep()
#             upcontentBtn = driver.find_elements_by_xpath('//*[@id="appEntry"]/div/div[2]/section/div/div[1]/div/a/span')
#         sleep()
#         if len(upcontentBtn) > 0:
#             sleep()
#             action = ActionChains(driver).move_to_element(upcontentBtn[0]).click().perform()
#         print('click upcontenBtn')
# #
# #

        # uploadVideo = []
        # while len(uploadVideo) == 0 and not isTimeOut(startTime):
        #     sleep()
        #     uploadVideo = driver.find_elements_by_xpath('//*[@id="appEntry"]/div/div[2]/section/div/div[1]/ul/li[2]/a')
        #     print(uploadVideo)
        # sleep()
        # if len(uploadVideo) > 0:
        #     sleep()
        #     action = ActionChains(driver).move_to_element(uploadVideo[0]).click().perform()
        # print('click uploadVideo')

        uploadVideoBtn = []
        while len(uploadVideoBtn) == 0 and not isTimeOut(startTime):
            sleep()
            uploadVideoBtn = driver.find_elements_by_xpath('//*[@id="appEntry"]/div/div[2]/section/div/div[2]/div/div/div[1]')
            print(uploadVideoBtn)
        sleep()
        if len(uploadVideoBtn) > 0:
            sleep()
            action = ActionChains(driver).move_to_element(uploadVideoBtn[0]).click().perform()
            os.system("upfile.exe " + upvideoPath)
        print('click uploadVideoBtn')

        clickType = []
        while len(clickType) == 0 and not isTimeOut(startTime):
            sleep()
            clickType = driver.find_elements_by_xpath('//*[@id="appEntry"]/div/div[2]/section/div[2]/div[1]/div[2]/div/section[1]/ul/li[2]/div/div[1]')

        if len(clickType) > 0:
            sleep()
            action = ActionChains(driver).move_to_element(clickType[0]).click().perform()
        sleep()
        #
        selectType = []
        while len(selectType) == 0 and not isTimeOut(startTime):
            sleep()
            selectType = driver.find_elements_by_xpath('//*[@id="appEntry"]/div/div[2]/section/div[2]/div[1]/div[2]/div/section[1]/ul/li[2]/div/div[1]/div/ul/li')
            if len(selectType) > 0:
                for t in selectType:
                    print(t.text)
                    if t.text == videoType:
                        sleep()
                        t.click()
        sleep()
        tagBtn = []
        while len(tagBtn) == 0 and not isTimeOut(startTime):
            sleep()
            tagBtn = driver.find_elements_by_xpath('//*[@id="appEntry"]/div/div[2]/section/div[2]/div[1]/div[2]/div/section[1]/ul/li[3]/div/div[3]/div/p/span')
            if len(tagBtn) > 0:
                for tag in tagBtn:
                    sleep()
                    tag.click()

        move= []
        while len(move) == 0 and not isTimeOut(startTime):
            sleep()
            move = driver.find_elements_by_xpath('//*[@id="appEntry"]/div/div[2]/section/div[2]/div[1]/div[2]/a')
            if len(move) > 0:
                action = ActionChains(driver).move_to_element(move[0]).perform()

        sleep()

        uploadVideoPic = []
        while len(uploadVideoPic) == 0 and not isTimeOut(startTime):
            sleep()
            uploadVideoPic = driver.find_elements_by_xpath('//*[@id="appEntry"]/div/div[2]/section/div[2]/div[1]/div[2]/div/section[1]/ul/li[5]/div/div[1]/div[1]/div[1]/a')
        sleep()
        if len(uploadVideoPic) > 0:
            sleep()
            action = ActionChains(driver).move_to_element(uploadVideoPic[0]).click().perform()
        print('click uploadVideoPic')

        uploadVideoPic = []
        while len(uploadVideoPic) == 0 and not isTimeOut(startTime):
            sleep()
            uploadVideoPic = driver.find_elements_by_xpath('//*[@id="appEntry"]/div/div[2]/section/div[2]/div[1]/div[2]/div/section[1]/ul/li[5]/div/div[1]/div[2]/div[2]/div/div[2]/ul/li[1]')
        sleep()
        if len(uploadVideoPic) > 0:
            sleep()
            action = ActionChains(driver).move_to_element(uploadVideoPic[0]).click().perform()
            os.system("upfile.exe " + viodePicPath)
        print('click uploadVideoPic')

        uploadVideoPic = []
        while len(uploadVideoPic) == 0 and not isTimeOut(startTime):
            sleep()
            uploadVideoPic = driver.find_elements_by_xpath('//*[@id="appEntry"]/div/div[2]/section/div[2]/div[1]/div[2]/div/section[1]/ul/li[5]/div/div[1]/div[2]/div[3]/div[3]/a[2]')
        sleep()
        if len(uploadVideoPic) > 0:
            sleep()
            action = ActionChains(driver).move_to_element(uploadVideoPic[0]).click().perform()
            os.system("upfile.exe " + viodePicPath)
        print('click uploadVideoPic save')

        sleep()
        publish = []
        while True and not isTimeOut(startTime):
            sleep()
            try:
                publish = driver.find_element_by_xpath('//*[@id="appEntry"]/div/div[2]/section/div[2]/div[2]/div/div/a[2]')
                action = ActionChains(driver).move_to_element(publish).click().perform()
                sleep()
            except:
                break;
        print('click publish video !')
#
        sleep(3)
        error = False

        if isTimeOut(startTime):
            videoNameList.append(videoName)
            driver.quit()
            continue
        driver.quit()
        #
        # os.remove(upvideoPath)
        # os.remove(viodePicPath)
#
        if error is False:
            with open('published','a') as f:
                f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\t' + usename + "\tpublished:\t" + videoName + '\n')
                total += 1
        else:
             pass

with open('finished', 'a') as f:
    f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\t' + "published:\t" + str(total) + "\tviodes" + '\n')

