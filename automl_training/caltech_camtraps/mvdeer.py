import os
import shutil

f = open("trimmedlabels.txt", "r")

i = 0
for line in f.readlines():
    name = line.split(" : ")[0]
    if os.path.exists("fullimages/" + name) and not os.path.exists("bigdeerimages/" + name):
        shutil.copy("fullimages/" + name, "bigdeerimages/" + name)
        i += 1

print(i)


    
