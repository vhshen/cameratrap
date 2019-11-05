import os

for f in os.listdir("newlabels"):
    fil = open("newlabels/" + f, "r")
    lis = fil.readlines()
    newlis = []
    for l in lis:
        if l not in newlis:
            newlis.append(l)
        else:
            print("dup in: " + f)
    newf = open("newnewlabels/" + f, "w")
    for nl in newlis:
        newf.write(nl)

