__author__ = 'jr'

import cv2
import numpy as np
import tesseract

def deskew(image):
    """
    Computes the skew angle of the text and applies any necessary rotations.
    Then crops the image.
    Assumes the image is loaded and in grayscale.
    """
    img = image.copy()
    size = img.shape
    #TODO - do i need to flip the background color?
    cv2.bitwise_not(img, img) # flip the background from white to black and forground to white
    lines = cv2.HoughLinesP(img, rho=1, theta=np.pi/180, threshold=75, minLineLength = size[1]/2.0, maxLineGap = 20)
    disp_lines = np.empty(size)
    angle = 0.0
    nb_lines = lines.shape[1]
    for i in range(0, nb_lines):
        line_i = lines[0, i]
        #cv2.line(disp_lines, (line_i[0], line_i[1]), (line_i[2], line_i[3]), 255)
        angle += np.arctan2(line_i[3]-line_i[1], line_i[2]-line_i[0])

    angle /= nb_lines
    angle = angle*180.0/np.pi # convert to degrees

    # Now rotate the image
    #compute the box
    #TODO - Optimize the loop here.
    points = []
    for i in range(0, size[0]):
        for j in range(0, size[1]):
            if img[i, j]:
                points.append([j, i])
    points = np.array(points)
    rect = cv2.minAreaRect(points)
    # Draw a box around the area of interest for debuging purposes
    #box = cv2.cv.BoxPoints(rect)
    #box = np.int0(box)
    #cv2.drawContours(img, [box], 0, 255, 1)
    mat = cv2.getRotationMatrix2D(rect[0], angle, 1)
    result = cv2.warpAffine(img, mat, (size[1], size[0]), flags=cv2.INTER_CUBIC)
    cv2.bitwise_not(result, result)
    return result


def cropReceiptBorder(image):
    """
    Pulls the receipt out of the image
    Assumes the
    """
    medBlur = cv2.medianBlur(src=image, ksize=13)
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    gray_blur = cv2.cvtColor(medBlur,cv2.COLOR_BGR2GRAY)
    mask = np.zeros((gray_blur.shape),np.uint8)

    edges = cv2.Canny(image=gray_blur, threshold1= 130.0, threshold2=250.0, L2gradient=True)
    contour,hier = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    # The biggest area should be the receipt
    max_area = 0
    best_cnt = None
    for cnt in contour:
        area = cv2.contourArea(cnt)
        if area > 1000:
            if area > max_area:
                max_area = area
                best_cnt = cnt

    cv2.drawContours(mask,[best_cnt],0,255,-1)
    cv2.drawContours(mask,[best_cnt],0,0,2)

    #corners = cv2.cornerHarris(src=mask,blockSize=2,ksize=3, k=0.04)
    #corners = cv2.dilate(corners,None)
    #image[corners>0.01*corners.max()] = [0,0,255]

    #TODO - clean up the looping.  Possible optimizations here.
    size = mask.shape
    x_pts = []
    y_pts = []
    for i in range(0, size[0]):
        for j in range(0, size[1]):
            if mask[i, j]:
                x_pts.append(i)
                y_pts.append(j)
    x_pts = np.array(x_pts)
    y_pts = np.array(y_pts)
    x1, x2 = x_pts.min(), x_pts.max()
    y1, y2 = y_pts.min(), y_pts.max()

    w = x2 - x1
    h = y2 - y1

    marginX = int(w * 0.05)
    marginY = int(h * 0.05)

    x1 += marginX
    x2 -= marginX
    y1 += marginY
    y2 -= marginY

    return gray[x1:x2, y1:y2]

def applyImageFilters(image):
    """
    Applies the filters to make the letters/digits stand out more
    and get rid of any dis-colorization and shadows
    assumes the image is in grayscale
    """
    #blur = cv2.GaussianBlur(image, (3, 3), 0)
    #blur = cv2.medianBlur(src=image, ksize=3)

    #res = cv2.adaptiveThreshold(src=blur, maxValue=255,
    #                            adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    #                            thresholdType=cv2.THRESH_BINARY, blockSize=13, C=7)

    #retVal, res = cv2.threshold(src=blur, thresh=0, maxval=255, type=cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    #cv2.fastNlMeansDenoising(src=res, dst=res, h=40, templateWindowSize=9, searchWindowSize=21)

    #element = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2,2))
    #res = cv2.morphologyEx(src=res, op=cv2.MORPH_OPEN, kernel=element)
    #res = cv2.morphologyEx(src=res, op=cv2.MORPH_CLOSE, kernel=element)

    gray = cv2.GaussianBlur(image,(3,3),0)
    gray = cv2.adaptiveThreshold(src=gray, maxValue=255,
                                adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                thresholdType=cv2.THRESH_BINARY, blockSize=13, C=7)
    kernel1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(20,20))
    close = cv2.morphologyEx(gray,cv2.MORPH_CLOSE,kernel1)
    div = np.float32(gray)/(close)
    res = np.uint8(cv2.normalize(div,div,0,255,cv2.NORM_MINMAX))
    return res

def applyImageFiltersIM(image):
    """
    Cleans the image using image magick
    assumes the image is in grayscale
    """


def applyOCR(image):
    """
    Applies the ocr to the image
    assumes the image is in grayscale
    """
    api = tesseract.TessBaseAPI()
    api.Init(".","eng",tesseract.OEM_DEFAULT)
    api.SetPageSegMode(tesseract.PSM_AUTO)

    cvmat_image= cv2.cv.fromarray(image)
    iplimage = cv2.cv.GetImage(cvmat_image)
    tesseract.SetCvImage(iplimage, api)
    result = api.GetUTF8Text()
    conf = api.MeanTextConf()
    print "result=", result
    print "conf=", conf
