import os

# Check to make sure all the labels have files
#f = open("deerlabels.txt", "r")
#for line in f.readlines():
#    fname = line.split()[0].split("/")[2]
#    if not os.path.exists("labelled/" + fname):
#        print(fname)

i = 0
lab = open("templabels.txt", "r")
l = lab.read()
#print(l)
# Check to make sure all the files have labels
for f in os.listdir("labelled"):
    af = f + "\n"
    if af not in l:
        os.rename("labelled/" + f, "otherdeer/" + f)
        i += 1
print(i)

