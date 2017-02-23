import cv2
import pprint
import numpy as np
import sys

class ImageProcesser:

    lastTop=None
    lastBottom=None

    def __init__(self):
        pass

    def process_image(self, img,draw=False,thrs1=563,thrs2=1958,maxPoints=4,minPoints=4):
        display=None;
        if(draw==True):
            display=img.copy();
        widthmax = 100
        heightmax = 800
        widthmin = 20
        heightmin = 20
        topRatio = 0.25
        bottomRatio = 0.125
        deviation = 1.0
        rotationUThresh = 15.0
        rotationLThresh = -15.0
        upper_green = ([255,255,130])
        lower_green = ([50,50,110])
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        #create a copy of the orginal image so we can us it for the final display

        height, width, channels = img.shape

        mask = cv2.inRange(hsv, lower_green, upper_green)
        
        #convert to 1 channel
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
        blur = cv2.GaussianBlur(gray,(5,5),0)
       
        #get edge version of the bw image
        edge = cv2.Canny(blur, thrs1, thrs2, apertureSize=5)
        #find all the contours
        cimage, cnts, hierarchy = cv2.findContours(edge.copy(), mask, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        #print("countours found:",len(cnts))
        topRects=[]
        bottomRects=[]
        for cnt in cnts:
            if(draw==True):
                cv2.drawContours(display, [cnt], -1, (255,100,255), 3)
            #first we get the minArea rect
            rect = cv2.minAreaRect(cnt)
            #now we find the aprox shape
            epsilon = 0.01*cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,epsilon,True)
            #we only want 4 point shapes
            if len(approx) <= maxPoints and len(approx) >= minPoints:
                rect = cv2.minAreaRect(cnt)
                if(draw==True):
                    cv2.drawContours(display, [cnt], -1, (255,255,0), 3)
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
                            if(draw==True):
                                cv2.drawContours(display, [cnt], -1, (0,0,255), 3)
                            topRects.append([rect,cnt])


                        if(ratio > bottomRatio - deviation) and (ratio < bottomRatio + deviation):
                            print("found bottom rectangle")
                            if(draw==True):
                                cv2.drawContours(display, [cnt], -1, (0,0,255), 3)
                            bottomRects.append([rect,cnt])




        newTop=None
        newBottom=None
        #now we check to see if more than one of each rect was found
        
        if len(topRects)>1:
            print ("too many top and bottom rects")
             #loop through rects and see which one is closest to the last found rect
            if(self.lastTop is not None):
                closestTop=None
                dist=None
                for trect in topRects:
                    rct=trect[0]
                    cont=trect[1]
                    if dist is None:
                        closestTop=rct
                        print("last top",self.lastTop[0][0])
                        pprint.pprint(self.lastTop)
                        print("trect ",trect[0][0])
                        pprint.pprint(trect)
                        dist=abs(rct[0][0])-abs(self.lastTop[0][0])
                    else:
                        tdist=abs(rct[0][0])-abs(self.lastTop[0][0])
                        if(tdist<dist):
                            dist=tdist
                            closestTop=rct
                newTop=closestTop
        else:
            if(len(topRects)>0):
                newTop=topRects[0][0]
                cv2.drawContours(display, [topRects[0][1]], -1, (0,255,0), 3)

        if len(bottomRects)>1 :
            if(self.lastBottom is not None):
                closestBott=None
                dist=None
                #loop through rects and see which one is closest to the last found rect
                for trect in bottomRects:
                    rct=trect[0]
                    cont=trect[1]
                    if dist is None:
                        #first rect
                        closestBott=rect
                        print("last bottom",self.lastBottom[0][0])
                        pprint.pprint(self.lastBottom)
                        print("trect ",trect[0][0])
                        pprint.pprint(trect)
                        dist=abs(rct[0][0])-abs(self.lastBottom[0][0])
                        
                    else:
                        tdist=abs(rct[0][0])-abs(self.lastBottom[0][0])
                        if(tdist<dist):
                            dist=tdist
                            closestBott=rct
                newBottom=closestBott
        else:
            if(len(bottomRects)>0):
                newBottom=bottomRects[0][0]
                cv2.drawContours(display, [bottomRects[0][1]], -1, (0,255,0), 3)



        print("newTop")
        pprint.pprint(newTop)
        print("newBottom")
        pprint.pprint(newBottom)
        #if we find a bottom and top rectangle we draw it out and set the lastTop and lastBottom for next image
        if newTop is not None:
            self.lastTop=newTop

        if newBottom is not None:
            self.lastBottom=newBottom

        return newTop, newBottom, display
