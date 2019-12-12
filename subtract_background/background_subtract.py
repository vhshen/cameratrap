'''
This program shows how to use background subtraction methods provided by OpenCV. 
You can process both videos and images
'''
from __future__ import print_function
import cv2
import argparse
parser = argparse.ArgumentParser(description='This program \
    shows how to use background subtraction methods provided by \
    OpenCV. You can process both videos and images.')
parser.add_argument('--input', type=str, help='Path to a video or a sequence of image.', default='vtest.avi')
parser.add_argument('--algo', type=str, help='Background subtraction method (KNN, MOG2).', default='MOG2')
args = parser.parse_args()
if args.algo == 'MOG2':
    backSub = cv2.createBackgroundSubtractorMOG2()
else:
    backSub = cv2.createBackgroundSubtractorKNN()
capture = cv2.VideoCapture(cv2.samples.findFileOrKeep(args.input))
if not capture.isOpened:
    print('Unable to open: ' + args.input)
    exit(0)
#frame = cv2.imread("leopard.jpg")
while True:
    ret, frame = capture.read()
    if frame is None:
        break
    
    fgMask = backSub.apply(frame)   
    
    fm = cv2.resize(frame, (960, 540)) 
    fg = cv2.resize(fgMask, (960, 540)) 
    cv2.imshow('Frame', fm)
    cv2.imshow('FG Mask', fg)
    
    keyboard = cv2.waitKey(30)
    if keyboard == 'q' or keyboard == 27:
        break
