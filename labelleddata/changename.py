import os

i = 5
for f in os.listdir("."):
    if "py" in f:
        continue
    os.rename(f, "deer" + str(i) + ".jpg")
    i += 1
