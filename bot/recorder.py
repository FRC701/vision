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
import time
import os


# relative module
import video

import pprint

# built-in module
import sys


class Recorder():
    cap=None

    cam=0
    path="videos/"

    def __init__(self,cam):
        self.cap = video.create_capture()

    def start_process(self):
        cntr=0
        nm = str(time.time())
        self.path=self.path+nm
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        while True:
            #pull image from video feed
            flag, img = self.cap.read()
            cv2.imwrite(self.path+"/"+str(cntr)+".jpg",img)
            cntr+=1




if __name__ == '__main__':
    print(__doc__)
    try:
        fn = sys.argv[1]
    except:
        fn = 0
    recorder=Recorder(fn)
    recorder.start_process()
