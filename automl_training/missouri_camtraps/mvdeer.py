import os
import shutil

f = open("deerlabels.txt", "r")
i = 0
for line in f.readlines():
    filename = line.split()[0].split("/")[2]
    newp = "labelled/" + filename
    #old = line.split()[0]
    old = "otherdeer/" + filename
    if line.split()[1] == "1" and os.path.exists(old):
        os.rename(old, newp)
        i += 1
    else:
        print(old)
print(i)


