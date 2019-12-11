import os
import re

fold = "deerorigmodel/neg0.5/"
bb = open(fold + "scores.txt")
for l in bb.readlines():
    if "2008_" in l or "2007_" in l or "deer" in l:
        name = l.strip().strip("jpg") + "txt"
        print(name)
    if "score" in l:
        score = re.search("(?<=score = ).*", l)
        conf = score.group(0)
    if "box" in l:
        blist = re.search("(?<=box = ).*", l)
        left, top, right, bottom = eval(blist.group(0))
        label = open(fold + "labels/" + name, "a")
        label.write("deer " + conf + " " + str(int(left)) + " " + str(int(top)) + " " + str(int(right)) + " " + str(int(bottom)) + "\n")
        label.close()


