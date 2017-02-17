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
    cap = video.create_capture(fn)

    cv2.namedWindow('output', cv2.WINDOW_NORMAL)
    cv2.namedWindow('controls', cv2.WINDOW_NORMAL)
    cv2.createTrackbar('thrs1','controls',563,5000,nothing)
    cv2.createTrackbar('thrs2','controls',1958,5000,nothing)

    imgprocesser=ImageProcesser()

    def findRects():
        while True:
            #pull image from video feed
            flag, img = cap.read()
            topRect, bottomRect, img = imgprocesser.process_image(img,thrs1,thrs2,True)
            cv2.imshow('output',img)
            cv2.waitkey(0)
            print("topRect and BottomRect:")
            #pprint.pprint(topRect)
            #pprint.pprint(bottomRect)
            if(topRect is not None):
                pprint.pprint(topRect)
    #counter = 0
    #if(counter < 5):
        #print("found rects")
        #tr, br = findRects()
        #points.append([tr, br])
        #print("Points", len(points))
        #counter += 1
