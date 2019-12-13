This is a folder with all the labelled data that came out of our "deployed" models.

Files:
    - deerfind.py: download deer from google
    - calcaverage.py: calculate average inference times per directory
    - makebb.py: makes bounding box label files based on evaluations from the TPU and our models

Folders:
    - deerimages = 89 original deer images from google.
    - negs = 100 random negative images from the VOC dataset
    - deervideos = 5 original deer video clips from youtube, each <5 seconds long
    - ground_truth = the original images run through the megadetector
    - mAP = tool to calculate the mAP for the various models. The original repository can be found [here](https://github.com/Cartucho/mAP)

For all the models, there are the images with drawn detections, 
for three different confidence thresholds: 0.3, 0.4, 0.5
There are also negative images that were passed through.
nodetect.txt are the images that didn't have detections
scores.txt have the confidence levels, bounding boxes, and inference times.
    - deerorigmodel = results from the original deer model (~250 pics)
    - deer2500model = results from 2500 deer image model
    - deer4000model = results from 4000 deer image model
