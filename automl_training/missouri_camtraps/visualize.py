import os
import cv2

f = open("deerlabels.txt", "r")

for line in f.readlines():
    fname = line.split()[0].split("/")[2]
    li = line.split()
    xmin, ymin, xmax, ymax = int(li[2]), int(li[3]), int(li[4]), int(li[5])
    img = cv2.imread("deerimages/" + fname)
    cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0,0,255))
    cv2.imshow("hello", img)
    cv2.waitKey(0)
