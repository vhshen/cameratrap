import os

for f in os.listdir("deerimages/"):
    if "oi_" in f:
        continue
    os.rename("deerimages/" + f, "deerimages/oi_" + f)

for t in os.listdir("labels/"):
    if "oi_" in t:
        continue
    os.rename("labels/" + t, "labels/oi_" + t)
