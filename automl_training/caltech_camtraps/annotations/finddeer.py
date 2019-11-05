import json

f = open("trans_test_annotations.json", "r")
newf = open("trans_test.txt", "w")
js = json.loads(f.read())
for a in js["annotations"]:
    if a["category_id"] == 34:
        imgid = a["image_id"]
        for i in js["images"]:
            if i["id"] == imgid:
                newf.write(i["file_name"] + " : ")
                newf.write(json.dumps(a))
                newf.write("\n")
