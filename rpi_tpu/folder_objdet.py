'''
This program uns detection on an entire folder of images
Outputting the resulting images w/ detections into an output directory
Also outputs a file with all the scores/inference times, and a file
that details on the images with nothing detected.
'''
import argparse
import platform
import subprocess
import time
from edgetpu.detection.engine import DetectionEngine
from PIL import Image
from PIL import ImageDraw
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', help='Path of the detection model.', required=True)
    parser.add_argument('--conf', help='confidence threshold', required=True)
    parser.add_argument('--indir', help='input directory', required=True)
    parser.add_argument('--outdir', help='output directory', required=True)
    args = parser.parse_args()
    conf = float(args.conf)
    nod = open(args.outdir + "nodetect.txt", "w")
    detf = open(args.outdir + "scores.txt", "w")
    
    # loop through all images in directory
    for f in os.listdir(args.indir):
        if os.path.exists(args.outdir + f):
            continue
        if "py" in f:   
            continue
        print("Processing " + f + "...")
        output_name = args.outdir + f

    	# initialize engine.
        engine = DetectionEngine(args.model)

        # open image
        img = Image.open(args.indir + f)
        draw = ImageDraw.Draw(img)

        # run detection and calculate inference time
        startt = time.time()
        ans = engine.DetectWithImage(img, threshold=conf, keep_aspect_ratio=True,relative_coord=False, top_k=10)
        inftime = time.time() - startt

        # display result
        if ans:
            for obj in ans:
                # write the result to the scores text file
                print ('-----------------------------------------')
                detf.write('-----------------------------------------\n')
                detf.write(f + "\n")
                print ('score = ', obj.score)
                detf.write('score = ' + str(obj.score) + "\n")
                box = obj.bounding_box.flatten().tolist()
                print ('box = ', box)
                detf.write('box = ' + str(box) + "\n")
                detf.write('inference time = ' + str(inftime) + ' seconds\n\n')
                # draw the bounding box.
                draw.rectangle(box, outline='red')
                # save to output folder
                img.save(output_name)
        else:
            print ('No object detected!')
            # write result to the no detect text file
            nod.write(f + "\n")
    nod.close()
    detf.close()

if __name__ == '__main__':
    main()
