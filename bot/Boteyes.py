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
    #this will hold the final boundaries for the color filter
    boundaries = [
    ([17, 15, 100], [50, 56, 200]),
    ([1, 1, 0], [120, 120, 0]),
    ([25, 146, 190], [62, 174, 250]),
    ([103, 86, 65], [145, 133, 128])
]
    #min and max width of potential contours

    sd = ShapeDetector()
    #we will have a window for the controls and a window for the final display
    cv2.namedWindow('output')
    cv2.namedWindow('controls')
    #controls to adjust various things
    cv2.createTrackbar('thrs1', 'controls', 563, 5000, nothing)
    cv2.createTrackbar('thrs2', 'controls', 1958, 5000, nothing)

    cv2.createTrackbar('lr', 'controls', 29, 255, nothing)
    cv2.createTrackbar('hr', 'controls', 127, 255, nothing)

    cv2.createTrackbar('lg', 'controls', 33, 255, nothing)
    cv2.createTrackbar('hg', 'controls', 250, 255, nothing)

    cv2.createTrackbar('lb', 'controls', 82, 255, nothing)
    cv2.createTrackbar('hb', 'controls', 218, 255, nothing)

    cap = video.create_capture(fn)
    def process_image(img):
        #create a copy of the orginal image so we can us it for the final display
        display = img.copy()
        height, width, channels = img.shape
        #print(height,width)
        #get color values from controls
        lr = cv2.getTrackbarPos('lr','controls')
        lg = cv2.getTrackbarPos('lg','controls')
        lb = cv2.getTrackbarPos('lb','controls')
        hr = cv2.getTrackbarPos('hr','controls')
        hg = cv2.getTrackbarPos('hg','controls')
        hb = cv2.getTrackbarPos('hb','controls')
         #our two color boundaries
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
        #we convert it to a 1 channel matrix
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        #gray = cv2.GaussianBlur(gray, (7, 7), 0)
         #we add a threshold
        ret,thresh = cv2.threshold(gray,127,255,0)
        thrs1 = cv2.getTrackbarPos('thrs1', 'controls')
        thrs2 = cv2.getTrackbarPos('thrs2', 'controls')
        edge = cv2.Canny(gray, thrs1, thrs2, apertureSize=5)
        cimage, cnts, hierarchy = cv2.findContours(edge.copy(), cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        print("countours found:",len(cnts))
        filter = []
        #we draw all the found contours
        cv2.drawContours(display, cnts, -1, (255, 255, 100), 2)
        for cnt in cnts:
            #first we filter out the contours that are the wrong size
            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(display,[box],0,(255,0,255),2)
            width = rect[1][1]
            height = rect[1][0]
            widthmax = 800
            heightmax = 100
            widthmin = 20
            heightmin = 20
            print ("checking ",height,width)
            if (width<widthmax) and (height <heightmax) and (width >= widthmin) and (height > heightmin):
                print ("detected ",height,width)
                #now we make sure it is a rectangle
                #shape = sd.detect(cnt)
                #if shape == "rectangle":
                 #   filter.append(cnt)
                cv2.drawContours(display, [cnt], -1, (0, 255, 0), 2)

        print("filter length:", len(filter))
        print("")

        vis = img.copy()
        vis = np.uint8(vis/2.)
        vis[edge != 0] = (0, 255, 0)
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
