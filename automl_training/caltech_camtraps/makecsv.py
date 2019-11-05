import os
import cv2
import csv
import json

f = open("labels.txt", "r")
cs = open("labels_calcamtraps.csv", "w")
urlf = open("caltech.txt", "r")
allurls = urlf.read().split("\n")
labc = csv.writer(cs, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

for line in f.readlines():
    fname, d = line.split(" : ")
    dic = json.loads(d)
    wline = []
    wline.append("UNASSIGNED")
    for u in allurls:
        if (u.strip("gs://cxl-deer/").split("-2019")[0] + ".jpg") == fname:
            wline.append(u)
    wline.append("Deer")
    img = cv2.imread("deerimages/" + fname)
    h, w, c = img.shape
    bbox = dic["bbox"]
    xmin, ymin, wid, hei = float(bbox[0]), float(bbox[1]), float(bbox[2]), float(bbox[3])
    x1, y1, x2, y2 = xmin/w, ymin/h, (xmin+wid)/w, (ymin+hei)/h
    wline.extend([x1, y1,'','',x2,y2,'',''])
    labc.writerow(wline)

cs.close()
f.close()
