import os

for f in os.listdir("negs"):
    if "jpg" in f:
        txtname = f.strip("jpg") + "txt"
        o = open("negs/labels/" + txtname, "w")
        o.close()
