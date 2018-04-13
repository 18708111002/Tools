#encoding:utf-8
import re
import os

List =[]

for videoName in os.listdir('d:\inputvideo'):
    List.append(re.split(u'@|!|\.|,|，|-|\?|_|？|！|。', videoName))
    print(List)

# rule = rule[:-1]
# List =[]
# with open('LIST.TXT','r') as f:
#     for line in f:
#         List.append(re.split(u'@|!|\.|,|，|-|\?|_|？|！|。',line))
#
# with open('modify.txt','w') as f:
#     for line in List:
#         for word in line:
#             # f.write(line[0])
#             f.write(word + "          ")
#         f.write('\n')