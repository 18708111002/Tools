# # -*- coding:utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import os
import time
import sys
reload(sys)
sys.setdefaultencoding("utf-8" )
import re
#做一个等待的通用方法
def sleep(sec=1):
    time.sleep(sec)
rootdir = r'd:\test'
type = u'娱乐'
videoNameList = []
for file in os.listdir(rootdir):
    if file.split('.')[-1] == u'mp4':
        videoNameList.append(file.split('.')[0])

usename = '17198016614'
pwd = 'miludeer115'
videoName = videoNameList[0]
upvideoPath = os.path.join(rootdir ,videoName+ '.mp4')
viodePicPath = os.path.join(rootdir ,videoName+ '.jpg')
#
driver = webdriver.Chrome()
driver.maximize_window()
driver.get("http://creator.miaopai.com/login")
sleep()

account=[]
while len(account) == 0:
    sleep()
    account = driver.find_elements_by_xpath('/html/body/div/div/span/main/main/div/section/div/div[2]/div[4]/form/div[1]/input')
account[0].send_keys(usename)

passwd = []
while len(passwd) == 0:
    sleep()
    passwd = driver.find_elements_by_xpath('/html/body/div/div/span/main/main/div/section/div/div[2]/div[4]/form/div[2]/input')
passwd[0].send_keys(pwd)


login = []
while len(login) == 0:
    sleep()
    login = driver.find_elements_by_xpath('/html/body/div/div/span/main/main/div/section/div/div[2]/div[4]/form/button')
login[0].send_keys(Keys.ENTER)

upvideoBtn = []
while len(upvideoBtn) == 0:
    sleep()
    upvideoBtn = driver.find_elements_by_xpath('/html/body/div/div/span/main/div/div[1]/div[2]/ul/li[2]')
upvideoBtn[0].click()  #upvideo

chooseVideoBtn=[]
while len(chooseVideoBtn) == 0 :
    sleep()
    chooseVideoBtn = driver.find_elements_by_xpath('//*[@id="uploadVideo"]')
chooseVideoBtn[0].click()
os.system("upfile.exe " + upvideoPath)


typeInput = []
while len(typeInput) == 0:
    sleep()
    typeInput = driver.find_elements_by_xpath('/html/body/div[1]/div/span/main/div/div[3]/div/div/div[2]/div/div[3]/div[2]/div[2]/form/div[3]/div/div/div[1]/div[1]/input')
typeInput[0].click()


//*[@id="cutMark"]/div/div[3]/span/button
upVideoPic = []
while len(upVideoPic) == 0:
    upVideoPic = driver.find_elements_by_xpath('//*[@id="uploadMyMark"]')
sleep()
action = ActionChains(driver).move_to_element(upVideoPic[0]).click().perform()
os.system("upfile.exe " + viodePicPath)
sleep()





typeSelect = []
while len(typeSelect) == 0:
    typeSelect = driver.find_elements_by_xpath('//ul[@class="el-select-group"]/li')

for t in typeSelect:
    if t.text == type:
        print(t.text)
        sleep()
        t.click()
        break

# progress_bar = []
# while len(progress_bar) == 0:
#     progress_bar = driver.find_elements_by_xpath('/html/body/div[1]/div/span/main/div/div[3]/div/div/div[2]/div/div[3]/div[2]/div[2]/div/div[2]')
# while True:
#     if u'上传成功' in progress_bar[0].text:
#         break
# sleep(10)
# # #
# videoManage = []
# while len(videoManage) == 0:
#     videoManage = driver.find_elements_by_xpath('/html/body/div[1]/div/span/main/div/div[1]/div[2]/ul/li[3]')
# videoManage[0].click()
# # #
# draftbox = []
# while len(draftbox) == 0:
#     draftbox =driver.find_elements_by_xpath('/html/body/div[2]/div/span/main/div/div[3]/div/div[1]/div[2]/div[1]/div/div[1]/div/div[3]')
# draftbox[0].click()
# # #
# editButton = []
# while len(editButton) == 0:
#     editButton = driver.find_elements_by_xpath('/html/body/div[2]/div/span/main/div/div[3]/div/div[2]/div[1]/ul/li/div[2]/div[3]/div/span/button[2]')
# action = ActionChains(driver).move_to_element(editButton[0]).click().perform()

# upVideoPic = []
# while len(upVideoPic) == 0:
#     upVideoPic = driver.find_elements_by_xpath('//*[@id="uploadMyMark"]')
# action = ActionChains(driver).move_to_element(upVideoPic[0]).click().perform()
# os.system("upfile.exe " + viodePicPath)






