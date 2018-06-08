#!coding:utf-8    相信这句大家都懂的，不解释

#导入需要的python模块httplib，用来模拟提交http请求，详细的用法可见python帮助手册

import requests
import os
import pandas as pd
import datetime
import json
account = []
data = []
with open('./account','r') as f:
   for  line in f:
      userName = line.split()[0]
      pwd= line.split()[1]
      account.append((userName,pwd))



#定义请求头

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
   info = info['data']
   credit = info['credit']
   qiantianMpc = info['qiantianMpc']
   historyMpc = info['historyMpc']

   if trial_status == '0':
      trial_status = 'yes'
   else:
      trial_status = 'no'

   data.append([str(userName),credit,qiantianMpc,historyMpc,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),trial_status])

if os.path.exists('./profit.csv'):
   df = pd.read_csv('./profit.csv')
   profit = pd.DataFrame(data,columns=['Username','Credit','Before Yesterday Profit','History Profit','Time','trail'])
   profit = df.append(profit)
   profit.to_csv('./profit.csv',index=False)

else:
   profit = pd.DataFrame(data,columns=['Username','Credit','Before Yesterday Profit','History Profit','Time','trail'])
   profit.to_csv('./profit.csv',index=False)
