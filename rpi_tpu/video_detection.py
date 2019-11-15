'''
This program runs detection on a video file.
Again, runs very slowly because processes every frame.
'''
from edgetpu.detection.engine import DetectionEngine
from imutils.video import VideoStream
from PIL import Image
import argparse
import imutils
import time
import cv2
 
# default confidence threshold is 0.4
ap = argparse.ArgumentParser()
ap.add_argument("-m", "--model", required=True,
            help="path to TensorFlow Lite object detection model")
ap.add_argument("-l", "--labels", required=False,
            help="path to labels file")
ap.add_argument("-v", "--video", required=True, help="path to video file")
ap.add_argument("-c", "--confidence", type=float, default=0.4,
            help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

# parse labels file, load into directory.
print("[INFO] parsing class labels...")
labels = {}
for row in open(args["labels"]):
    (classID, label) = row.strip().split(maxsplit=1)
    labels[int(classID)] = label.strip()
                 
# load the Google Coral object detection model
print("[INFO] loading Coral model...")
model = DetectionEngine(args["model"])
                  
# initialize the video stream from file
print("[INFO] opening video stream...")
vs = cv2.VideoCapture(args["video"])
time.sleep(2.0)

# initialize the video writer
capfps = int(vs.get(cv2.CAP_PROP_FPS))
out = cv2.VideoWriter("../deervideos/labelvids/output.avi", cv2.VideoWriter_fourcc('M','J','P','G'), capfps, (int(vs.get(cv2.CAP_PROP_FRAME_WIDTH)),int(vs.get(cv2.CAP_PROP_FRAME_HEIGHT))))
print("[INFO] cap fps = " + str(capfps))

print("[INFO] entering loop...")
# loop over the frames from the video stream
while True:
    # grab the frame from the threaded video stream and resize it
    # to have a maximum width of 500 pixels
    ret, frame = vs.read()
    if not ret:
        print("no more frames!")
        break
    frame = imutils.resize(frame, width=500)
    orig = frame.copy()
                         
    # prepare the frame for object detection by converting (1) it
    # from BGR to RGB channel ordering and then (2) from a NumPy
    # array to PIL image format
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = Image.fromarray(frame)
                                             
    # make predictions on the input frame
    start = time.time()
    results = model.DetectWithImage(frame, threshold=args["confidence"], keep_aspect_ratio=True, relative_coord=False)
    end = time.time()

    # write to file even when no results found
    if not results:
        print("[INFO] nothing detected, writing...")
        out.write(orig)

    # loop over the results
    for r in results:
        # extract the bounding box and box and predicted class label
        box = r.bounding_box.flatten().astype("int")
        (startX, startY, endX, endY) = box
        label = labels[r.label_id]
                                                 
        # draw the bounding box and label on the image
        cv2.rectangle(orig, (startX, startY), (endX, endY),(0, 255, 0), 2)
        y = startY - 15 if startY - 15 > 15 else startY + 15
        text = "{}: {:.2f}%".format(label, r.score * 100)
        cv2.putText(orig, text, (startX, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        print("[INFO] writing frame...")
        print("Detection: " + str(r.score*100) + "%")
        print("Bounding box: " + str(r.bounding_box.flatten()))
        out.write(orig)
    
    # show the output frame
    cv2.imshow("Frame", orig)
    cv2.waitKey(1)

cv2.destroyAllWindows()
vs.release()
