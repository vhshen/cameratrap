import os

dirname = "downloads/deer"
namespassed = []
i = 0
for f in os.listdir(dirname):
    name = f.split(".")
    name[0] = ""
    fname = ".".join(name)

    if fname not in namespassed:
        namespassed.append(fname)
    else:
        i += 1
        os.remove(dirname + "/" + f)

print(i)
