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
from canlistener import Canlistener

# relative module
import video

import pprint

# built-in module
import sys


class Eyes():




    #holds the last rects found to compare
    lastTop=None
    lastBottom=None
    #measurments in inches
    knownDist1 = 24
    knownWidth = 4
    knownHeigth = 16
    knownPixelW1 = 0
    knownPixelH1 = 0

    #min and max width of potential contours
    screenCenter = 320
    widthmax = 100
    heightmax = 800
    widthmin = 20
    heightmin = 20
    topRatio = 4.0
    bottomRatio = 8.00
    deviation = 1.0
    rotationUThresh = 15.0
    rotationLThresh = -15.0
    sd = ShapeDetector()
    distance=0
    #we will have a window for the controls and a window for the final display
    #cv2.namedWindow('output')
    #cv2.namedWindow('controls')
    #controls to adjust various things
    #cv2.createTrackbar('thrs1', 'controls', 563, 5000, nothing)
    #cv2.createTrackbar('thrs2', 'controls', 1958, 5000, nothing)

    cam=0



    draw = False
    imgprocesser=ImageProcesser()
    def __init__(self,cam,draw=False):
        self.draw=draw
        if(self.draw==True):
            print("showing display")
            cv2.namedWindow('display',cv2.WINDOW_NORMAL)
        self.cam=cam
        clistener=Canlistener(parent=self)
    def send_data(self):
        bus2=can.interface.Bus(can_interface, bustype='socketcan_native')
        msg = can.Message(arbitration_id=33821708, data=[self.distance, self.topOffset, 0, 1, 3, 1, 4, 1], extended_id=False)
        bus2.send(msg)
    def calcDistByWidth(self):
        focalLength = (self.knownPixelW1 * self.knownDist1) / self.knownWidth
        self.distance = (self.knownWidth * focalLength) / self.tRectWidth
    def calcDistByHeigth(self):
        focalLength = (self.knownPixelH1 * self.knownDist1) / self.knownHeigth
        self.distance = (self.knownHeigth * focalLength) / self.tRectHeigth
    def start_process(self):
        cap = video.create_capture(self.cam)
        while True:
            #pull image from video feed
            flag, img = cap.read()
            self.screenCenter = len(img) / 2
            print(self.screenCenter)
            self.topRect, self.bottomRect, dis = self.imgprocesser.process_image(img,draw=self.draw)
            if self.draw == True:
                print("Showing image")
                cv2.imshow('display',dis)
                ch = cv2.waitKey(5) & 0xFF
            if self.topRect is not None:
                print("self.topRect ")
                pprint.pprint(self.topRect)
                self.tRectCenter = self.topRect[0][0]
                self.tRectWidth = self.topRect[0][0] * 2
                self.tRectHeigth = self.topRect[0][1] * 2
                self.topOffset = self.screenCenter - self.tRectCenter
                if(self.tRectCenter - (self.tRectWidth / 2) < 0):
                    self.calcDistByHeigth()
                    print("Rectangle is off screen to the left!")
                elif(self.tRectCenter + (self.tRectWidth / 2) > len(img)):
                    self.calcDistByHeigth()
                    print("Rectangle is off screen to the right!")
                else:
                     self.calcDistByWidth()
           # cv2.imshow("images\\\", np.hstack([mask, output]))



if __name__ == '__main__':
    print(__doc__)
    try:
        fn = sys.argv[1]
    except:
        fn = 0
    eyes=Eyes(fn,True)
    eyes.start_process()
