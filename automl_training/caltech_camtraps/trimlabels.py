import os
import json
import cv2

f = open("labels.txt", "r")
w = open("trimmedlabels.txt", "w")

fint = 0
wint = 0
for line in f.readlines():
    fint += 1
    fname, d = line.split(" : ")
    dic = json.loads(d)
    if "bbox" in dic:
        wint += 1
        w.write(line)

print("num labels: " + str(fint))
print("num labels after trim: " + str(wint))
