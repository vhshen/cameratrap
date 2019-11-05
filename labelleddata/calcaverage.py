import os
import re

sfile = ["deerorigmodel/conf0.5/scores.txt", "deerorigmodel/conf0.4/scores.txt", "deerorigmodel/conf0.3/scores.txt"]
ofile = "deerorigmodel/results.txt"
o = open(ofile, "w")
for s in sfile:
    o.write(s + "\n")
    print(s)
    f = open(s, "r")
    summ = 0
    numm = 0
    r = f.read()
    inftime = re.findall("(?<=inference time = )\d+.\d+", r) 
    for i in inftime:
        summ += float(i)
        numm += 1
    print("Num detections = ", numm)
    avg = summ/numm
    print("Average inference time = ", avg)
    o.write("Num detections = " + str(numm) + "\n")
    o.write("Avg inference time = " + str(avg) + "\n\n")
