import os
import json
import cv2

f = open("trimmedlabels.txt", "r")

for line in f.readlines():
    fname = line.split()[0]
    d = line.strip(fname).strip(" : ")
    dic = json.loads(d)
    li = dic["bbox"]
    xmin, ymin, xmax, ymax = int(li[0]), int(li[1]), int(li[2]+li[0]), int(li[3]+li[1])
    img = cv2.imread("fullimages/" + fname)
    cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0,0,255))
    cv2.imshow("hello", img)
    cv2.waitKey(0)
