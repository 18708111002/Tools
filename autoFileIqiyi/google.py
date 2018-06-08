
import urllib2

url = 'https://commondatastorage.googleapis.com/clusterdata-2011-1/'
f = open('C:\Users\zj\Downloads\SHA256SUM')
l = f.readlines()
f.close()

cnt = 0
start = False
for i in l:
    print(i)
    if i.count('task_constraints')>0:
        fileAddr = i.split()[1][1:]
        fileName = fileAddr.split('/')[1]
        print 'downloading', fileName
        data = urllib2.urlopen(url+fileAddr).read()
        print 'saving', fileName
        fileDown = open('D:\googleData\\task_constraints\\'+fileName, 'wb')
        fileDown.write(data)
        fileDown.close()


