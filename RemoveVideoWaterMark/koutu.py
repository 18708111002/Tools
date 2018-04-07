import cv2
import numpy as np

fname = 'd:/PICTURE/1/3.jpg'

# def generateTemple(fname):
#     img = cv2.imread(fname)
#     rect = (10, 20, 1000, 100)
#     mask = np.zeros(img.shape[:2], np.uint8)
#     bgModel = np.zeros((1,65), np.float64)
#     fgModel = np.zeros((1,65), np.float64)
#     cv2.grabCut(img, mask, rect, bgModel, fgModel, 5, cv2.GC_INIT_WITH_RECT)
#     mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype(np.uint8)
#     out = img * mask2[:, :, np.newaxis]
#
#     return out

img = cv2.imread(fname)
img = img[-300:-1, -300:-1]
cv2.imshow('test win', img)
cv2.imwrite(fname + 'logo.jpg', img)
cv2.waitKey(0)