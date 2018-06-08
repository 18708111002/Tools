#-*- coding:utf-8 -*-


import json
import requests
import os
import pandas as pd
import datetime
import json
import sys
# reload(sys)
# sys.setdefaultencoding('utf8')
account = []
data = []
with open('./account','r') as f:
   for  line in f:
      userName = line.split()[0]
      pwd= line.split()[1]
      account.append((userName,pwd))

#定义请求头

if os.path.exists('./profit.xlsx'):
   df = pd.read_excel('./profit.xlsx')
else:
   df = pd.DataFrame(columns=['Username','NickName','Credit','Before Yesterday Profit','History Profit','Time','trail','Infomation'])


for userName,pwd in account:
   session = requests.session()
   login_url = "http://creator.miaopai.com/auth/login"

   loginheaders = {'Accept': 'application/json, text/plain, */*',
      'Accept-Encoding': 'gzip, deflate',
      'Accept-Language': 'zh-CN',
      'Cache-Control': 'no-cache',
      'Connection': 'Keep-Alive',
      'Content-Type': 'application/x-www-form-urlencoded',
      'Cookie': 'PHPSESSID=ugd10h5mnpc4qmhnsbbivm9bu4; Hm_lpvt_e6af01253df49e1d8df23316e3dee264=1525868064',
      'Host': 'creator.miaopai.com',
      'Origin': 'http://creator.miaopai.com',
      'Referer': 'http://creator.miaopai.com/login',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299',
      'X-Requested-With': 'XMLHttpRequest'}

   reqdata={  'bblogintype': '1',
      'phone': userName,
      'pwd': pwd,
      'remember': 'false',
      'type': '0'
   }

   token  = eval(session.post(login_url, data=reqdata, headers=loginheaders).content)['data']
   nickName= token['nick'].decode('unicode_escape')
   trial_status = token['platform']['trial_status']
   token = token['token']
   reqHeaders = {'Accept': 'application/json, text/plain, */*',
      'Accept-Encoding': 'gzip, deflate',
      'Accept-Language': 'zh-CN',
      'Connection': 'Keep-Alive',
      'Cookie': 'Hm_lvt_e6af01253df49e1d8df23316e3dee264=1525868030,1525877684; PHPSESSID=m36ten1eneek1cs22f49h470o7; Hm_lpvt_e6af01253df49e1d8df23316e3dee264=1525877684; SRV_CREATOR_COOKIE_LOGIN_TOKEN='+token ,
      'Content-Type': 'application/x-www-form-urlencoded',
      'Host': 'creator.miaopai.com',
      'Referer': 'http://creator.miaopai.com/profits/divideInto',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299',
      'X-Requested-With': 'XMLHttpRequest'}

   info  = eval(session.post('http://creator.miaopai.com/commission/mympc',  headers=reqHeaders).content)
   # print(info)
   info = info['data']
   credit = info['credit']
   qiantianMpc = info['qiantianMpc']
   historyMpc = info['historyMpc']


   msg = eval(session.post('http://creator.miaopai.com/message/getList?page=1&pageSize=20', headers=reqHeaders).content)
   # print(msg)
   information = ''
   for dic in msg['data']['list']:
        title = dic['title']
        ctime = dic['ctime']
        if r'\u88ab\u5904\u4ee5' in title and r'\u5904\u7f5a' in title or r'\u88ab\u7981\u6b62' in title:
            information += title.decode('unicode_escape') + " " + ctime + "\n"
#
   if trial_status == '0':
      trial_status = 'yes'
   else:
      trial_status = 'no'

   userInfo = {}
   userInfo['Username'] = str(userName)
   userInfo['NickName'] = nickName
   userInfo['Credit'] = credit
   userInfo['Before Yesterday Profit'] = qiantianMpc
   userInfo['History Profit'] = historyMpc
   userInfo['Time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
   userInfo['trail'] = trial_status
   userInfo['Infomation'] = information

   df = df.append(userInfo,ignore_index=True)
   # data.append([str(userName),nickName,credit,qiantianMpc,historyMpc,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),trial_status,information])

df.to_excel('./profit.xlsx',index=False)

