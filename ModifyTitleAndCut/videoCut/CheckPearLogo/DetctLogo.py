#coding=utf-8
import cv2
import scipy as sp
import sys
import os


inputFileDir = sys.argv[1]


print("inputFileDir  : " + inputFileDir)

picList = []
for picName in os.listdir(inputFileDir):
    picList.append(picName)

img2 = cv2.imread('temple.jpg',0) # trainImage
for picName in picList:
    img1 = cv2.imread(inputFileDir + "\\" + picName,0) # queryImage
    img1 = img1[0:200, 0:200]

    # Initiate SIFT detector
    sift = cv2.SIFT()

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1,None)
    kp2, des2 = sift.detectAndCompute(img2,None)

    # FLANN parameters
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks=50)   # or pass empty dictionary
    flann = cv2.FlannBasedMatcher(index_params,search_params)
    matches = flann.knnMatch(des1,des2,k=2)

    # print 'matches...',len(matches)
    # Apply ratio test
    good = []
    for m,n in matches:
        if m.distance < 0.75*n.distance:
            good.append(m)
    print picName,'good',len(good)

    if len(good) > 1:
        print(picName + "is left logo")


def isPearLogo(templeImg,img):

    img1 = img[0:200, 0:200]

    # Initiate SIFT detector
    sift = cv2.SIFT()

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(templeImg, None)

    # FLANN parameters
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)  # or pass empty dictionary
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)

    good = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good.append(m)
    print picName, 'good', len(good)

    if len(good) > 1:
        return True

# #####################################
# visualization
h1, w1 = img1.shape[:2]
h2, w2 = img2.shape[:2]
view = sp.zeros((max(h1, h2), w1 + w2, 3), sp.uint8)
view[:h1, :w1, 0] = img1
view[:h2, w1:, 0] = img2
view[:, :, 1] = view[:, :, 0]
view[:, :, 2] = view[:, :, 0]

# for m in good:
#     # draw the keypoints
#     # print m.queryIdx, m.trainIdx, m.distance
#     color = tuple([sp.random.randint(0, 255) for _ in xrange(3)])
#     #print 'kp1,kp2',kp1,kp2
#     cv2.line(view, (int(kp1[m.queryIdx].pt[0]), int(kp1[m.queryIdx].pt[1])) , (int(kp2[m.trainIdx].pt[0] + w1), int(kp2[m.trainIdx].pt[1])), color)
#
# cv2.imshow("view", view)
# cv2.waitKey()