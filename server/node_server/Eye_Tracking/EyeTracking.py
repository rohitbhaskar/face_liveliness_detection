# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 08:16:54 2018

@author: Tanay_Shah
"""

import cv2
import numpy as np


#haar classifiers they will come with opencv installation
# face_cascade = cv2.CascadeClassifier('C:/Users/Tanay Shah/Anaconda2/pkgs/opencv-2.4.11-py27_1/Library/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml')
# eye_cascade = cv2.CascadeClassifier('C:/Users/Tanay Shah/Anaconda2/pkgs/opencv-2.4.11-py27_1/Library/share/OpenCV/haarcascades/haarcascade_eye.xml')
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')


# thresholds to be set after observing values
leftEyeMovementXThreshold = 10
rightEyeMovementXThreshold = 10

leftEyeMovementYThreshold = 10
rightEyeMovementYThreshold = 10

liveliness = False



def leftTopEye(x , y, eyes):
    leftTop1 = 10000
    leftTop2 = 10000
    print x , y , eyes
    for i in range(0 , len(eyes)):
        (ex,ey,ew,eh) = eyes[i]
        if (x+int(ex+0.5*ew)) < leftTop1 and y+int(ey+0.5*eh) < leftTop2:
            correctEye = (ex,ey,ew,eh)
    return correctEye

def rightTopEye(x , y, eyes):
    rightTop1 = 0
    rightTop2 = 0
    for i in range(0 , len(eyes)):
        (ex,ey,ew,eh) = eyes[i]
        if (x+int(ex+0.5*ew)) > rightTop1 and y+int(ey+0.5*eh) > rightTop2:
            correctEye = (ex,ey,ew,eh)
    return correctEye

#face angle for registration step
def calculateFaceAngle(x , y , correct_eyes):
    (ex1,ey1,ew1,eh1) = correct_eyes[0]
    (ex2,ey2,ew2,eh2) = correct_eyes[1]
    y2 = y+int(ey2+0.5*eh2)
    y1 = y+int(ey1+0.5*eh1)
    x2 = x+int(ex2+0.5*ew2)
    x1 = x+int(ex2+0.5*ew2)
    try:
        return (y2-y1)/(x2-x1)
    except:
        return 0
    
# register frames
def registerImage(image, angle):
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
  return result        
    
#read video file
cap = cv2.VideoCapture("1.mp4")
while not cap.isOpened():
    cap = cv2.VideoCapture(0)
    cv2.waitKey(1000)
    # print "Wait for the header"

leftEyeMotionX = []
rightEyeMotionX = []

leftEyeMotionY = []
rightEyeMotionY = []

i =0

faceAngle = 0


#dummy condition actual till end of video
# while i <int(cap.get(cv2.CAP_PROP_FRAME_COUNT)):
while i <0:
    flag, image = cap.read()
    i = i +1
    if flag:
        # The frame is ready and already captured
        gray  = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
 
        centers=[]
        faces = face_cascade.detectMultiScale(gray,1.3,5)
        
        for (x,y,w,h) in faces:
 
            #create two Regions of Interest.
            roi_gray = gray[y:y+h/2, x:x+w]
            roi_color = image[y:y+h/2, x:x+w]
            # print "face detected"
            eyes = eye_cascade.detectMultiScale(roi_gray)
            
            correct_eyes = []
            if len(correct_eyes) !=0:
                correct_eyes.append(leftTopEye(x , y , eyes))
                correct_eyes.append(rightTopEye(x , y , eyes))
            
            # Store the cordinates of eyes in the frame to the 'center' array
            eyeCentroidX = 0
            eyeCentroidY = 0
            for (ex,ey,ew,eh) in eyes:
                eyeCentroidX = eyeCentroidX + x+int(ex+0.5*ew)
                eyeCentroidY = eyeCentroidY + x+int(ey+0.5*eh)
                centers.append((x+int(ex+0.5*ew), y+int(ey+0.5*eh)))
                # print "eye dete ted"
                cv2.circle(image,(x+int(ex+0.5*ew), y+int(ey+0.5*eh)), 5, (0,255,0), -1)
            try:
                eyeCentroidX = eyeCentroidX / len(eyes)
                eyeCentroidY = eyeCentroidY / len(eyes)
                
                #image registration
                faceAngle = calculateFaceAngle(x , y , correct_eyes)
                image = registerImage(image , faceAngle)
                
                eyes = eye_cascade.detectMultiScale(roi_gray)
                
                
                for (ex,ey,ew,eh) in eyes:
                    doneLeft = False
                    doneRight = False
                    if x+int(ex+0.5*ew) < eyeCentroidX and (not doneLeft):
                        leftEyeMotionX.append(x+int(ex+0.5*ew))
                        leftEyeMotionY.append(y+int(ey+0.5*eh))
                        doneLeft = True
                        if x+int(ex+0.5*ew) > eyeCentroidX and (not doneRight):
                            rightEyeMotionX.append(x+int(ex+0.5*ew))
                            rightEyeMotionX.append(y+int(ey+0.5*eh))
                            doneRight = True
                
            except ZeroDivisionError:
                pass    
        # cv2.imshow('video', image)
    else:
        pass
        # cv2.waitKey(1000)
        
    # if cv2.waitKey(10) == 27:
    #     break
    
if len(leftEyeMotionX) ==0 or len(rightEyeMotionX) ==0:
    pass
else:
    leftEyeXMovement = leftEyeMotionX[0] - leftEyeMotionX[-1]
    leftEyeYMovement = leftEyeMotionY[0] - leftEyeMotionY[-1]
    
    rightEyeXMovement = rightEyeMotionX[0] - rightEyeMotionX[-1]
    rightEyeYMovement = rightEyeMotionY[0] - rightEyeMotionY[-1]  
    
    if leftEyeXMovement > leftEyeMovementXThreshold and leftEyeYMovement > leftEyeMovementYThreshold and rightEyeXMovement > rightEyeMovementXThreshold and rightEyeYMovement > rightEyeMovementYThreshold :
        liveliness = True

print 1

#cv2.destroyAllWindows()
  
