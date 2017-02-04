#!/usr/bin/env python

# Python 2/3 compatibility

from __future__ import print_function

from imageprocesser import ImageProcesser

# relative module
import video

import pprint

# built-in module
import sys

points = []
if __name__ == '__main__':
    print(__doc__)

    try:
        fn = sys.argv[1]
    except:
        fn = 0
    #start video moduel
    cap = video.create_capture(fn)


    
    imgprocesser=ImageProcesser()

    def findRects()
        while True:
            #pull image from video feed
            flag, img = cap.read()
            topRect, bottomRect = imgprocesser.process_image(img)
            print("topRect and BottomRect:") 
            pprint.pprint(topRect)
            pprint.pprint(bottomRect)
            if(topRect is not None and bottomRect is not None):
                break
    counter = 0
    if(counter < 5):
        print("found rects")
        tr, br = findRects()
        points.append([tr, br])
        print("Points", len(points))
        counter += 1
