Folder for the CXL "demo" deployment


If you want to do realtime detection:
    
    - detect\_rt.py is realtime detection using imutils VideoStream class
        - Realtime inference time for:
            - COCO Mobilenet model: ~ 1.27 seconds
            - Deer4000: ~ 5.55 seconds
            - Deer2500: ~ 15.6 seconds
            - DeerOrig: ~ 39.4 seconds

    - q\_rt.py is realtime detection using a custom LIFO queue class
        - Realtime inference time for:
            - COCO Mobilenet model: ~ 1.21 seconds
            - Deer4000: ~ 5.95 seconds
            - Deer2500: ~ 18.1 seconds
            - DeerOrig: ~ 47.8 seconds

    - use "gstreamer/detect.py", which is modified google code.
        - Realtime inference time for:
            - COCO Mobilenet model: ~ 1.8 seconds
            - Deer4000: ~ 10.4 seconds
            - Deer2500: ~ 21.1 seconds
            - DeerOrig: ~ 67.9
    	- note that our model don't detect much with this program
	but the preset models do
        - also note that this program displays every frame even when it hasn’t run inference on it, which is why it seems faster. However, in reality, it is actually doing the inferences slower than the other methods (probably because it is expending time to display every frame)

    - video\_detection.py works on video file detection

    - folder\_objdet.py runs object detection on an entire folder of
    images.

The "COCO Mobilenet model" referenced above is: mobilenet_ssd_v1_coco_quant_postprocess_edgetpu.tflite

object\_detection.py is just for static detection of a single image

googlewebscrape contains a script for being able to scrape images
off of google images

classification contains google's scripts for image classification
(non-realtime)


