** This is the repository that contains all the scripts for realtime detection on an RPI4 with a Coral TPU and a RPi Cam, using TF Lite models.

The files are as follows:
    * classify_capture.py: Script from Google TF, classify objects in real time.
    * detect.py: Script from Google, runs object detection using openCV
    * noimg_detect.py: Same as detect.py but without displaying the image.
    * q_detect.py: Multithreaded realtime detection using the VideoStream class
        * inference time is slower than gstreamer
    * noimg_q_detect.py: Same as above, but doesn't display image.
    * In the folder gstreamer:
        * gstreamer.py: helper functions
        * detect.py: Adapted streaming code from Google, uses the gstreamer api.
