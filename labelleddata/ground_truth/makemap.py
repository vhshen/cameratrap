import os
import cv2

for f in os.listdir("labels"):
    print(f)
    l = open("labels/" + f, "r")
    o = open("maplabels/" + f, "w")

    iname = f.strip("txt") + "jpg"
    img = cv2.imread("../deerimages/" + iname)
    h, w, c = img.shape

    for line in l.readlines():
        name, midx, midy, wid, hei = line.split()
        midx, midy, wid, hei = float(midx), float(midy), float(wid), float(hei)
        left = int(midx*w - wid*w/2)
        right = int(midx*w + wid*w/2)
        top = int(midy*h - hei*h/2)
        bottom = int(midy*h + hei*h/2)

        o.write(name + " " + str(left) + " " + str(top) + " " + str(right) + " " + str(bottom) + "\n")

    l.close()
    o.close()
