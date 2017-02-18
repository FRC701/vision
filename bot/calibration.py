#!/usr/bin/env python

# Python 2/3 compatibility

from __future__ import print_function

from imageprocesser import ImageProcesser

# relative module
import video

import cv2

import pprint

# built-in module
import sys

def nothing(*arg):
    pass

points = []
if __name__ == '__main__':
    print(__doc__)

    try:
        fn = sys.argv[1]
    except:
        fn = 0
    #start video moduel
    cap = video.create_capture(str(fn)+":size=1024x768")

    cv2.namedWindow('output', cv2.WINDOW_NORMAL)
    cv2.namedWindow('controls', cv2.WINDOW_NORMAL)
    cv2.createTrackbar('thrs1','controls',563,5000,nothing)
    cv2.createTrackbar('thrs2','controls',1958,5000,nothing)
    cv2.createTrackbar('maxPoints','controls',4,15,nothing)
    cv2.createTrackbar('minPoints','controls',4,15,nothing)

    imgprocesser=ImageProcesser()

    def findRects():
        while True:
            #pull image from video feed
            flag, img = cap.read()
            thrs1 = cv2.getTrackbarPos('thrs1', 'controls')
            thrs2 = cv2.getTrackbarPos('thrs2', 'controls')
            maxPoints = cv2.getTrackbarPos('maxPoints','controls')
            minPoints = cv2.getTrackbarPos('minPoints','controls')
            topRect, bottomRect, img = imgprocesser.process_image(img,True,thrs1,thrs2,maxPoints,minPoints)
            print("is none",img is None)
            if img is not None:
                cv2.imshow('output',img)
                ch = cv2.waitKey(5) & 0xFF
            print("topRect and BottomRect:")
            #pprint.pprint(topRect)
            #pprint.pprint(bottomRect)
            if(topRect is not None):
                pprint.pprint(topRect)
    findRects()
    #counter = 0
    #if(counter < 5):
        #print("found rects")
        #tr, br = findRects()
        #points.append([tr, br])
        #print("Points", len(points))
        #counter += 1
