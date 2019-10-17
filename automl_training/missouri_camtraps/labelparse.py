

f = open("labels.txt", "r")
newf = open("realdeerlabels.txt", "w")
for line in f.readlines():
    animal = line.split()[0].split("/")[0].split("-")[1]
    if "Deer" in animal and line.split()[1] != "0": 
        newf.write(line)

