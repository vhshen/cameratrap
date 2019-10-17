import csv

nfile = open("deerclass.csv", "w")
writer = csv.writer(nfile, delimiter=",")
cfile = open("classifications.csv")
csv_reader = csv.reader(cfile, delimiter=",")
line_count = 0
for row in csv_reader:
    if line_count == 0:
        line_count = 1
        fieldnames = row
        writer.writerow(row)
    elif "Roe Deer" in row or "Fallow Deer" in row:
        writer.writerow(row)

nfile.close()
cfile.close()
