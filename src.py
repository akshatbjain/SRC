# Task 1 - Detect a light source and identify its RGB value

import cv2
import numpy as np
from matplotlib import pyplot as plt

for n in range(1,6):
    string = 'test'+ str(n) + '.jpg'
    # Read image
    og = cv2.imread(string)
    height, width = og.shape[:2]
    while(height>480 or width>640):
        height = int(height/2)
        width = int(width/2)

    og = cv2.resize(og,(width,height))

    #cv2.imshow('Original', og)
    
    #Convert to grayscale
    gray = cv2.cvtColor(og,cv2.COLOR_BGR2GRAY)
    #cv2.imshow('Gray', gray)

    #Histogram
    hist, bins = np.histogram(gray.ravel(),256,[0,256])

    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)

    thresh = int(maxVal*0.9)
    binary = gray

    ret,binary = cv2.threshold(gray,thresh,255,0)
    #cv2.imshow('Binary', binary)

    im_floodfill = binary.copy()
    mask = np.zeros((height+2,width+2), np.uint8)
    cv2.floodFill(im_floodfill, mask,(0,0),255)
    im_floodfill_inv = cv2.bitwise_not(im_floodfill)
    im_floodfill = binary | im_floodfill_inv

    #cv2.imshow('floodfill', im_floodfill)

    kernel = np.ones((5,5),np.uint8)
    closing = cv2.morphologyEx(im_floodfill, cv2.MORPH_CLOSE, kernel)
    #cv2.imshow('Closing', closing)

    contours, hierarchy = cv2.findContours(closing,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    for i in range(len(contours)):
        if cv2.contourArea(contours[i]) > 200:
            M = cv2.moments(contours[i])               
            cx = int(M['m10']/(M['m00'] + 0.01))
            cy = int(M['m01']/(M['m00'] + 0.01))
            cv2.circle(og,(cx,cy),20,(0,0,255),2)
            print og[cy,cx]

    cv2.imshow('Original', og)

    cv2.waitKey(0)

cv2.destroyAllWindows()
 
