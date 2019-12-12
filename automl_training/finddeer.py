'''
This script finds deer files in the missouri camera traps dataset
by parsing the JSon
'''
import json

deerints = [4, 12, 14, 15]
f = open("missouri_camtraps/missouri_camera_traps_set1.json", "r")
newf = open("missouri_camtraps/miss_camtraps.txt", "w")
js = json.loads(f.read())
for a in js["annotations"]:
    if a["category_id"] in deerints:
        imgid = a["image_id"]
        for i in js["images"]:
            if i["id"] == imgid:
                newf.write(i["file_name"] + ":" )
                newf.write(json.dumps(a))
                newf.write("\n")
