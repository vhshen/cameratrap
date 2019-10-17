import json

f = open("caltech_images_20190919.json", "r")
newf = open("imgnames.txt", "w")
js = json.loads(f.read())
for a in js["annotations"]:
    if a["category_id"] == 34:
        imgid = a["image_id"]
        for i in js["images"]:
            if i["id"] == imgid:
                newf.write(i["file_name"])
                #newf.write(json.dumps(a))
                newf.write("\n")
