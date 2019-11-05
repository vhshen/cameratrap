import os
import cv2
import csv
import json

f = open("deerlabels.txt", "r")
cs = open("labels_misscamtraps.csv", "w")
urlf = open("miss.txt", "r")
allurls = urlf.read().split("\n")
labc = csv.writer(cs, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

for line in f.readlines():
    fname = line.split()[0].split("/")[2]
    li = line.split()
    wline = []
    wline.append("UNASSIGNED")
    for u in allurls:
        url = u.strip("gs://cxl-deer/").split("-2019")[0]+".JPG"
        if url == fname:
            wline.append(u)
    wline.append("Deer")
    img = cv2.imread("deerimages/" + fname)
    h, w, c = img.shape
    xmin, ymin, xmax, ymax = int(li[2]), int(li[3]), int(li[4]), int(li[5])
    x1, y1, x2, y2 = xmin/w, ymin/h, xmax/w, ymax/h
    wline.extend([x1, y1,'','',x2,y2,'',''])
    labc.writerow(wline)

cs.close()
f.close()
