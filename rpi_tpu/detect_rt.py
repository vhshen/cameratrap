'''
This program runs detection in EVERY FRAME in realtime
Obviously this means it lags behind real time severely
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
ap.add_argument("-l", "--labels", required=True,
            help="path to labels file")
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
                  
# initialize the pi camera video stream
vs = VideoStream(src=0).start()
time.sleep(2.0)

# loop over the frames from the video stream
while True:
    frame = vs.read()
    # resize frame to half width
    # seems like imutils currently isn't working
    frame = cv2.resize(frame, (int(frame.shape[1]*0.5), int(frame.shape[0]*0.5)))
    orig = frame.copy()
                         
    # prepare the frame for object detection by converting (1) it
    # from BGR to RGB channel ordering and then (2) from a NumPy
    # array to PIL image format
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = Image.fromarray(frame)

    # make predictions on the input frame
    start = time.time()
    results = model.DetectWithImage(frame, threshold=args["confidence"],
            keep_aspect_ratio=True, relative_coord=False)
    end = time.time()
    print("Inference time: " + str(end-start))

    # loop over the results
    for r in results:
        # extract the bounding box and box and predicted class label
        box = r.bounding_box.flatten().astype("int")
        (startX, startY, endX, endY) = box
        label = labels[r.label_id]
        
        # draw the bounding box and label on the image
        cv2.rectangle(orig, (startX, startY), (endX, endY),
                (0, 255, 0), 2)
        y = startY - 15 if startY - 15 > 15 else startY + 15
        text = "{}: {:.2f}%".format(label, r.score * 100)
        cv2.putText(orig, text, (startX, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                                                                    
        # show the output frame and wait for a key press
        cv2.imshow("Frame", orig)
        key = cv2.waitKey(1) & 0xFF                               
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break                                                                        
cv2.destroyAllWindows()
vs.stop()

