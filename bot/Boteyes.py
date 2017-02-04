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
from imageprocesser import ImageProcesser
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
    #holds the last rects found to compare
    lastTop=None
    lastBottom=None


    #min and max width of potential contours
    screenCenter = 320
    widthmax = 800
    heightmax = 100
    widthmin = 20
    heightmin = 20
    topRatio = 4.0
    bottomRatio = 8.25
    deviation = 1.0
    rotationUThresh = 15.0
    rotationLThresh = -15.0
    sd = ShapeDetector()
    #we will have a window for the controls and a window for the final display
    cv2.namedWindow('output')
    cv2.namedWindow('controls')
    #controls to adjust various things
    cv2.createTrackbar('thrs1', 'controls', 563, 5000, nothing)
    cv2.createTrackbar('thrs2', 'controls', 1958, 5000, nothing)


    cap = video.create_capture(fn)



    imgprocesser=ImageProcesser()


    while True:
        #pull image from video feed
        flag, img = cap.read()
        screenCenter = len(img.cols) / 2
        topRect, bottomRect = imgprocesser.process_image(img)
        tRectCenter = topRect[0][0]
        tRectWidth = topRect[1][0]
        topOffset = screenCenter - tRectCenter
        if(tRectCenter - (tRectWidth / 2) < 0):
            print("Rectangle is off screen to the left!")
        if(tRectCenter + (tRectWidth / 2) > len(img.cols):
           print("Rectangle is off screen to the right!")
       # cv2.imshow("images\\\", np.hstack([mask, output]))
        ch = cv2.waitKey(5) & 0xFF
        if ch == 27:
            break
    cv2.destroyAllWindows()
