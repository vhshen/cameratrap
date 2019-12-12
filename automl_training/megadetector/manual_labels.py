'''
This file helps manually go through the output of the megadetector
and only saves the labels that are not wrong.
'''
import json
import os
import cv2
import keyboard

parser = argparse.ArgumentParser()
# Name of the class you are detecting
parser.add_argument("classname", metavar="classname", type=str, help="class name")
# Directory containing all the images that were megadetected
parser.add_argument("imagedir", metavar="imageDIR", type=str, help="directory with original images")
# Directory to save the label files to
parser.add_argument("labeldir", metavar="labelDIR", type=str, help="directory with generated labels")
# The json output of the megadetector
parser.add_argument("output_json", metavar="outputJSON", help="json file output by megadetector")
args = parser.parse_args()
jsonf = args.output_json
classname = args.classname
imagedir = args.imagedir + "/"
if "//" in imagedir:
    imagedir = args.imagedir
labeldir = args.labeldir + "/"
if "//" in labeldir:
    labeldir = args.labeldir

# Open the json output file
f = open(jsonf, "r")
full = f.read()
js = json.loads(full)

for name in os.listdir(imagedir):
    pth = imagedir + name
    oimg = cv2.imread(pth)
    img = cv2.resize(oimg, None, fx=0.3, fy=0.3)
    h, w, c = img.shape
    for i in js["images"]:
        # TODO: you might have to change this to whatever prefix
        # is in the "file" line of the output json
        if i["file"] == ("../" + pth):
            label = open(labeldir + name.strip("jpg") + "txt", "w")
            for d in i["detections"]:
                x1 = int(d["bbox"][0]*w)
                y1 = int(d["bbox"][1]*h)
                x2 = x1 + int(d["bbox"][2]*w)
                y2 = y1 + int(d["bbox"][3]*h)
                cv2.rectangle(img, (x1,y1), (x2,y2), (0,0,255))
                cv2.imshow("image", img)
                cv2.waitKey(200)
                # if the bounding box is wrong, type "y" and enter
                # else, just press enter
                if input("Is this wrong? ") != "y":
                    midx = str(d["bbox"][0] + d["bbox"][2]/2)
                    midy = str(d["bbox"][1] + d["bbox"][3]/2)
                    label.write(classname + " " + midx + " " + midy + " " + str(d["bbox"][2]) + " " + str(d["bbox"][3]) + "\n")
            label.close()
f.close()
