Folder for the CXL "demo" deployment

If you want to do realtime detection:
    - use "gstreamer/detect.py", which is modified google code.
    has the fastest inference times and works pretty smoothly
    	- note that our model don't detect much with this program
	but the preset models do, meaning that it is a problem with 
	our models and not the program

    - video_detection.py works on video file detection

    - q_rt.py is realtime detection using a LIFO queue class
    so it works in "real time" as well but the inference time is longer

    - detect_rt.py is realtime detection without multithreading,
    so it runs detection on every frame and is therefore very slow.

    - folder_objdet.py runs object detection on an entire folder of
    images.

object_detection.py is just for static detection of a single image

googlewebscrape contains a script for being able to scrape images
off of google images

classification contains google's scripts for image classification
(non-realtime)
