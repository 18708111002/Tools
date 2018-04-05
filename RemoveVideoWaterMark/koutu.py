import cv2
import numpy as np

fname = 'd:/PICTURE/1.jpg'

def generateTemple(fname):
    img = cv2.imread(fname)
    rect = (350, 20, 1000, 90)
    mask = np.zeros(img.shape[:2], np.uint8)
    bgModel = np.zeros((1,65), np.float64)
    fgModel = np.zeros((1,65), np.float64)
    cv2.grabCut(img, mask, rect, bgModel, fgModel, 5, cv2.GC_INIT_WITH_RECT)
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype(np.uint8)
    out = img * mask2[:, :, np.newaxis]

    return out

