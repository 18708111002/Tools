# # -*- coding:utf-8 -*-
import json
import requests
import os
import pandas as pd
import datetime
import json
import sys
import chardet

account = []
data = []

with open('./account','r') as f:
   for  line in f:
      userName = line.split()[0]
      pwd= line.split()[1]
      yourname = line.split()[2]
      account.append((userName,pwd,yourname))


import re
def isMail(str):
   p = re.compile(r'[^\._][\w\._-]+@(?:[A-Za-z0-9]+\.)+[A-Za-z]+$')
   res = p.match(str)
   if res:
      return True
   else:
      return False


if os.path.exists('./profit.xlsx'):
   df = pd.read_excel('./profit.xlsx')
else:
   df = pd.DataFrame(columns=['total_videos', 'total_balance', 'yesterday_income', 'fail_videos', 'nickname', 'account', 'level', 'credibility', 'successful_videos', 'time', 'balance', 'employeeName'])

for userName,pwd,yourname in account:

   statisData = []
   info = {'employeeName':yourname,
           'account': None,
           'nickname': None,
           'level': None,
           'balance': None,
           'total_balance': None,
           'yesterday_income': None,
           'credibility': None}

   session = requests.session()
   if isMail(userName):
      login_url = "https://mpapi.qutoutiao.net/member/login?email=" + userName + "&telephone=&password=" + pwd + "&keep=&captcha=&source=0&k=&dtu=200"
   else:
      login_url = "https://mpapi.qutoutiao.net/member/login?email=&telephone=" + userName + "&password=" + pwd + "&keep=&captcha=&source=1&k=&dtu=200"
   # print login_url
   token  = eval(session.post(login_url).content)['data']
   token = token['token']
   data = eval(session.post('https://mpapi.qutoutiao.net/member/getMemberInfo?token='+ token +'&dtu=200').content)['data']
   print userName
   info['time'] = datetime.datetime.now().strftime('%Y-%m-%d')
   info['account'] = userName
   info['nickname'] = data['nickname']
   info['level'] = data['level']
   info['balance'] = data['balance']
   info['total_balance'] = data['total_balance']
   info['yesterday_income'] = data['yesterday_income']
   info['credibility'] = data['credibility']

   data = eval(session.post('https://mpapi.qutoutiao.net/video/getList?status=&page=1&title=&submemberid=&nickname=&start_date=&end_date=&isMotherMember=false&token=' + token + '&dtu=200').content)['data']

   videos = data['videos']
   info['total_videos'] = 0
   info['fail_videos']  = 0
   info['successful_videos'] = 0

   now = datetime.datetime.now()

   for v  in videos:
      publish = datetime.datetime.strptime(v['submit_time'].split()[0],"%Y-%m-%d")
      if now - publish <= datetime.timedelta(days=1):
         info['total_videos'] += 1
         if int(v['quality']) < 2:
            info['fail_videos'] += 1
         else:
            info['successful_videos'] += 1

   df = df.append(info,ignore_index=True)

   # data = []
   # for k in info.keys():
   #    data.append(info[k])
   # statisData.append(data)



   # if os.path.exists('./profit.csv'):
   #    df = pd.read_csv('./profit.csv')
   #    profit = pd.DataFrame(statisData,columns=info.keys())
   #    profit = df.append(profit)
   #    profit.to_csv('./profit.csv',index=False)
   # else:
   #    profit = pd.DataFrame(statisData,columns=info.keys())
   #    profit.to_csv('./profit.csv',index=False,mode='a')

df.to_excel('./profit.xlsx',index=False)

#
#
#
