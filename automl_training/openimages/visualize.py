import os
import cv2

for iname in os.listdir("recheck"):
    tname = iname.strip("jpg") + "txt"
    img = cv2.imread("recheck/" + iname)
    f = open("labels/" + tname, "r")
    for line in f.readlines():
        n, xmin, ymin, xmax, ymax = line.split()
        xmin, ymin, xmax, ymax = int(float(xmin)), int(float(ymin)), int(float(xmax)), int(float(ymax))
        cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0,0,255))
        cv2.imshow("hello", img)
        cv2.waitKey(0)
    cv2.imwrite("vises/" + iname, img)
    f.close()
