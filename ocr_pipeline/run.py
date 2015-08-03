__author__ = 'jr'

import toolbox
import cv2
import sys

if __name__ == '__main__':
    #img = cv2.imread("test/receipt_2_1500x846.jpg")
    img = cv2.imread(sys.argv[1])
    if img == None:
        print "Could not open file."
    else:
        cv2.imshow("img", img)
        stage1 = toolbox.cropReceiptBorder(img)
        cv2.imshow('stage1',stage1)
        stage2 = toolbox.applyImageFilters(stage1)
        cv2.imshow('stage2',stage2)
        #stage3 = toolbox.deskew(sta
        stage3 = stage2
        toolbox.applyOCR(stage3)
        cv2.imshow('stage3',stage3)
        cv2.waitKey(0)