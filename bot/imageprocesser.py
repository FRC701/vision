import cv2
import pprint
import numpy as np
import sys

class ImageProcesser:
    
    lastTop=None
    lastBottom=None
    
    def __init__(self):
        pass

    def process_image(self, img):
        widthmax = 800
        heightmax = 100
        widthmin = 20
        heightmin = 20
        topRatio = 4.0
        bottomRatio = 8.25
        deviation = 1.0
        rotationUThresh = 15.0
        rotationLThresh = -15.0
        #create a copy of the orginal image so we can us it for the final display
        display = img.copy()
        height, width, channels = img.shape
        #convert to 1 channel
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thrs1 = cv2.getTrackbarPos('thrs1', 'controls')
        thrs2 = cv2.getTrackbarPos('thrs2', 'controls')
        #get edge version of the bw image
        edge = cv2.Canny(gray, thrs1, thrs2, apertureSize=5)
        #find all the contours
        cimage, cnts, hierarchy = cv2.findContours(edge.copy(), cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        #print("countours found:",len(cnts))
        topRects=[]
        bottomRects=[]
        for cnt in cnts:

            print("")
            #first we get the minArea rect
            rect = cv2.minAreaRect(cnt)
            #now we find the aprox shape
            epsilon = 0.01*cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,epsilon,True)
            #we only want 4 point shapes
            if len(approx)== 4:
                rect = cv2.minAreaRect(cnt)
                print("rect")
                pprint.pprint(rect)
                #get the height and width of the rectangle
                rWidth = rect[1][0]
                rHeight = rect[1][1]
                rotation = rect[2]
                #make sure we have positive integers
                if(rWidth > 0) and (rHeight > 0):
                    lRotation = rotationLThresh
                    uRotation = rotationUThresh
                    # this is because the code above will switch the height and width when the rotation is <0
                    if(rWidth < rHeight):
                        lRotation = -90
                        uRotation = -75
                    # now we make sure the rotation is within range
                    if(rotation > lRotation) and (rotation < uRotation):
                        ratio = float(rWidth) / float(rHeight)
                        # we reverse when the rotation is negative
                        if(rotation < -7):
                            ratio = float(rHeight) / float(rWidth)


                        print("Ratio:", ratio, rWidth, rHeight)
                        #now we check ratios to find the top and bottom ratio
                        if(ratio > topRatio - deviation) and (ratio < topRatio + deviation):
                            print("found top rectangle")
                            topRects.append(rect)


                        if(ratio > bottomRatio - deviation) and (ratio < bottomRatio + deviation):
                            print("found bottom rectangle")
                            bottomRects.append(rect)




        newTop=None
        newBottom=None
        print("")
        #now we check to see if more than one of each rect was found
        if len(topRects)>1:
            print ("too many top and bottom rects")
             #loop through rects and see which one is closest to the last found rect
            if(self.lastTop is not None):
                closestTop=None
                dist=None
                for trect in topRects:
                    if dist is None:
                        closestTop=trect
                        dist=abs(trect[0][0])-abs(self.lastTop[0][0])
                    else:
                        tdist=abs(trect[0][0])-abs(self.lastTop[0][0])
                        if(tdist<dist):
                            dist=tdist
                            closestTop=rect
                newTop=closestTop
        else:
            if(len(topRects)>0):
                newTop=topRects[0]

        if len(bottomRects)>1 :
            if(self.lastBottom is not None):
                closestBott=None
                dist=None
                #loop through rects and see which one is closest to the last found rect
                for trect in bottomRects:
                    if dist is None:
                        closestBott=trect
                        dist=abs(trect[0][0])-abs(self.lastBottom[0][0])
                    else:
                        tdist=abs(trect[0][0])-abs(self.lastBottom[0][0])
                        if(tdist<dist):
                            dist=tdist
                            closestBott=rect
                newBottom=closestBott
        else:
            if(len(bottomRects)>0):
                newBottom=bottomRects[0]


        print("newTop")
        pprint.pprint(newTop)
        print("newBottom")
        pprint.pprint(newBottom)
        #if we find a bottom and top rectangle we draw it out and set the lastTop and lastBottom for next image
        if newTop is not None:
            #cv2.drawContours(display, [newTop], -1, (0, 255, 0),2)
            self.lastTop=newTop

        if newBottom is not None:
            #cv2.drawContours(display, [newBottom], -1, (0, 100, 255), 2)
            self.lastBottom=newBottom
        cv2.imshow('display',display)
