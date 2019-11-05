import json

deerints = [4, 12, 14, 15]
f = open("missouri_camera_traps_set1.json", "r")
js = json.loads(f.read())
newf = open("deers.json", "w")

for a in js["annotations"]:
    if a["category_id"] in deerints and "bbox" in a:
        imgid = a["image_id"]
        for i in js["images"]:
            if i["id"] == imgid:
                newf.write(i["file_name"] + " ")
                newf.write(json.dumps(a))
                newf.write("\n")

f.close()
newf.close()
