#!/usr/bin/env python

'''
Vistion target detection for robot

Usage:
  Boteyes.py [<video source>]

  Trackbars control edge thresholds.

'''

# Python 2/3 compatibility
from __future__ import print_function

import cv2
import numpy as np
from pyimagesearch.shapedetector import ShapeDetector

# relative module
import video

import pprint

# built-in module
import sys


if __name__ == '__main__':
    print(__doc__)

    try:
        fn = sys.argv[1]
    except:
        fn = 0

    def nothing(*arg):
        pass

    boundaries = [
    ([17, 15, 100], [50, 56, 200]),
    ([1, 1, 0], [120, 120, 0]),
    ([25, 146, 190], [62, 174, 250]),
    ([103, 86, 65], [145, 133, 128])
]
    widthmax = 300
    heightmax = 300
    widthmin = 100
    heightmin = 30
    sd = ShapeDetector()

    cv2.namedWindow('output')
    cv2.namedWindow('controls')

    cv2.createTrackbar('thrs1', 'controls', 2000, 5000, nothing)
    cv2.createTrackbar('thrs2', 'controls', 4000, 5000, nothing)
    #cv2.namedWindow('mask')

    cv2.createTrackbar('lr', 'controls', 74, 255, nothing)
    cv2.createTrackbar('lg', 'controls', 37, 255, nothing)
    cv2.createTrackbar('lb', 'controls', 104, 255, nothing)
    cv2.createTrackbar('hr', 'controls', 114, 255, nothing)
    cv2.createTrackbar('hg', 'controls', 238, 255, nothing)
    cv2.createTrackbar('hb', 'controls', 239, 255, nothing)

    cap = video.create_capture(fn)
    def process_image(img):
        display = img.copy()
        
        #extract green color
        #pulling color value from trackbars
        lr = cv2.getTrackbarPos('lr','controls')
        lg = cv2.getTrackbarPos('lg','controls')
        lb = cv2.getTrackbarPos('lb','controls')
        hr = cv2.getTrackbarPos('hr','controls')
        hg = cv2.getTrackbarPos('hg','controls')
        hb = cv2.getTrackbarPos('hb','controls')
        la=[lb, lg, lr]
        ha=[hb, hg, hr]
        #print("la:",la)
        #print("ha:",ha)
        lower= np.array(la, dtype = "uint8")
        upper=np.array(ha, dtype = "uint8")
        # find the colors within the specified boundaries and apply
        # the mask
        mask = cv2.inRange(img, lower, upper)
        output = cv2.bitwise_and(img, img, mask = mask)
       # print("mask")
        #pprint.pprint(mask)
        #print ("output")
        #pprint.pprint(output)

        gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
        gray2=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        ret,thresh = cv2.threshold(gray,127,255,0)
        thrs1 = cv2.getTrackbarPos('thrs1', 'controls')
        thrs2 = cv2.getTrackbarPos('thrs2', 'controls')
        #edge = cv2.Canny(gray, thrs1, thrs2, apertureSize=5)
        cimage, cnts, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        print("countours found:",len(cnts))
        filter = []
        cv2.drawContours(display, cnts, -1, (255, 255, 0), 2)
        for cnt in cnts:
            rect = cv2.minAreaRect(cnt)       #I have used min Area rect for better result
            width = rect[1][0]
            height = rect[1][1]
            if (width<widthmax) and (height <heightmax) and (width >= widthmin) and (height > heightmin):
                shape = sd.detect(cnt)
                if shape == "rectangle":
                    filter.append(cnt)
                    cv2.drawContours(display, [cnt], -1, (255, 0, 0), 2)
                    
        print("filter length:", len(filter))
        print("")

        #vis = img.copy()
        #vis = np.uint8(vis/2.)
        #vis[edge != 0] = (0, 255, 0)
        #for c in cnts:
            #print ("contour:")
            #pprint.pprint(c)
        #cv2.imshow('output', vis)
        cv2.imshow('display',display)


    while True:
        #pull image from video feed
        flag, img = cap.read()
        process_image(img)
       # cv2.imshow("images\\\", np.hstack([mask, output]))
        ch = cv2.waitKey(5) & 0xFF
        if ch == 27:
            break
    cv2.destroyAllWindows()
