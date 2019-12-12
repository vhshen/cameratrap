'''
processes a video and does background subtraction based on movement
'''
# Python code for Background subtraction using OpenCV 
import numpy as np 
import cv2 
  
cap = cv2.VideoCapture('cheetahrun.mp4') 
fgbg = cv2.createBackgroundSubtractorMOG2() 
  
while(1): 
    ret, frame = cap.read() 
  
    fgmask = fgbg.apply(frame) 
   
    cv2.imshow('fgmask', frame) 
    cv2.imshow('frame', fgmask) 
  
      
    k = cv2.waitKey(30) & 0xff
    if k == 27: 
        break
      
  
cap.release() 
cv2.destroyAllWindows()