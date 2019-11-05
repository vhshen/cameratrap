import os
import cv2
import csv
import json

cs = open("labels_openimages.csv", "w")
labc = csv.writer(cs, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

url = "gs://cxl-deer/"

for f in os.listdir("deerimages"):
    txtname = f.strip("jpg") + "txt"
    txt = open("labels/" + txtname, "r")
    img = cv2.imread("deerimages/" + f)
    h, w, c = img.shape
    for line in txt.readlines():
        wline = []
        wline.append("UNASSIGNED")
        wline.append(url + f)
        wline.append("Deer")
        name, midx, midy, wid, hei = line.split()
        midx, midy, wid, hei = float(midx), float(midy), float(wid), float(hei)
        x1 = midx - wid/2
        x2 = midx + wid/2
        y1 = midy - hei/2
        y2 = midy + hei/2
        wline.extend([x1, y1,'','',x2,y2,'',''])
        labc.writerow(wline)
    txt.close()

cs.close()
