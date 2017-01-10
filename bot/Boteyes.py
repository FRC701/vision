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

    cv2.namedWindow('output')
    cv2.createTrackbar('thrs1', 'output', 2000, 5000, nothing)
    cv2.createTrackbar('thrs2', 'output', 4000, 5000, nothing)
    cv2.namedWindow('mask')

    cv2.namedWindow('rgb')
    cv2.createTrackbar('lr', 'rgb', 74, 255, nothing)
    cv2.createTrackbar('lg', 'rgb', 37, 255, nothing)
    cv2.createTrackbar('lb', 'rgb', 104, 255, nothing)
    cv2.createTrackbar('hr', 'rgb', 114, 255, nothing)
    cv2.createTrackbar('hg', 'rgb', 238, 255, nothing)
    cv2.createTrackbar('hb', 'rgb', 239, 255, nothing)

    cap = video.create_capture(fn)
    def process_image(img):
        #extract green color
        #pulling color value from trackbars
        lr = cv2.getTrackbarPos('lr','rgb')
        lg = cv2.getTrackbarPos('lg','rgb')
        lb = cv2.getTrackbarPos('lb','rgb')
        hr = cv2.getTrackbarPos('hr','rgb')
        hg = cv2.getTrackbarPos('hg','rgb')
        hb = cv2.getTrackbarPos('hb','rgb')
        la=[lb, lg, lr]
        ha=[hb, hg, hr]
        print("la:",la)
        print("ha:",ha)
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
        thrs1 = cv2.getTrackbarPos('thrs1', 'output')
        thrs2 = cv2.getTrackbarPos('thrs2', 'output')
        #edge = cv2.Canny(gray, thrs1, thrs2, apertureSize=5)
        cimage, cnts, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        print("countours found:",len(cnts));

        vis = img.copy()
        vis = np.uint8(vis/2.)
        #vis[edge != 0] = (0, 255, 0)
        #for c in cnts:
            #print ("contour:")
            #pprint.pprint(c)
        #cv2.imshow('output', vis)
        cv2.imshow('mask',mask)


    while True:
        #pull image from video feed
        flag, img = cap.read()
        process_image(img)
       # cv2.imshow("images\\\", np.hstack([mask, output]))
        ch = cv2.waitKey(5) & 0xFF
        if ch == 27:
            break
    cv2.destroyAllWindows()
