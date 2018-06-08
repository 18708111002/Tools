import re
from PIL import Image
pattern = re.compile(r'([-0-9]+)px')

x1 = []
y1 = []
x2 = []
y2 = []
with open('jigsaw.txt','r') as f:
    for line in f:
        x1.append(abs(int(pattern.findall(line)[0])))
        y1.append(abs(int(pattern.findall(line)[1])))
        width = int(pattern.findall(line)[2])
        height = int(pattern.findall(line)[3])

x2 = x1[len(x1)/2:]
y2 = y1[len(y1)/2:]
x1 = x1[:len(x1)/2]
y1 = y1[:len(y1)/2]

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
    nim.show()
    return nim
realign('bg.jpg',x1,x2,height,width,360,214).save('train.jpg')

# coding=utf-8
import cv2
import scipy as sp

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

    print 'matches...', len(matches)
    # Apply ratio test
    good = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good.append(m)
    print 'good', len(good)
#
#
# # #####################################
# # visualization
# h1, w1 = img1.shape[:2]
# h2, w2 = img2.shape[:2]
#
# view = sp.zeros((max(h1, h2), w1 + w2, 3), sp.uint8)
# view[:h1, :w1, 0] = img1
# view[:h2, w1:, 0] = img2
# view[:, :, 1] = view[:, :, 0]
# view[:, :, 2] = view[:, :, 0]
#
# for m in good:
#     # draw the keypoints
#     print m.queryIdx, m.trainIdx, m.distance
#     color = tuple([sp.random.randint(0, 255) for _ in xrange(3)])
#     print 'kp1,kp2',kp1,kp2
#     print(kp2)
#     print(int(kp2[m.trainIdx].pt[0]), int(kp2[m.trainIdx].pt[1]))
#     print((int(kp1[m.queryIdx].pt[0]), int(kp1[m.queryIdx].pt[1])))
#     cv2.line(view, (int(kp1[m.queryIdx].pt[0]), int(kp1[m.queryIdx].pt[1])),
#              (int(kp2[m.trainIdx].pt[0] + w1), int(kp2[m.trainIdx].pt[1])), color)
#
# cv2.imshow("view", view)
# cv2.waitKey()