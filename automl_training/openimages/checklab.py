import os

iaaa = 0
for i in os.listdir("labels"):
    fname = i.strip("txt") + "jpg"
    if not os.path.exists("deerimages/" + fname):
        iaaa += 1
        print(i)
        os.rename("labels/" + i, "unused/" + i)

print(iaaa)

ibbb = 0
for i in os.listdir("deerimages"):
    fname = i.strip("jpg") + "txt"
    if not os.path.exists("labels/" + fname):
        ibbb += 1
        print(i)
        #os.rename("test/Label/" + i, "unused/" + i)

print(ibbb)
