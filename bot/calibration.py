#!/usr/bin/env python

# Python 2/3 compatibility

from __future__ import print_function

from imageprocesser import ImageProcesser

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
    #start video moduel
    cap = video.create_capture(fn)


    
    imgprocesser=ImageProcesser()


    while True:
        #pull image from video feed
        flag, img = cap.read()
        topRect, bottomRect = imgprocesser.process_image(img)
        print("topRect and BottomRect:") 
        pprint.pprint(topRect)
        pprint.pprint(bottomRect)
        if(topRect is not None and bottomRect is not None):
            break
    print("found rects")
