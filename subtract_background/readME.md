Different possible algorithms:

    - PIL\_imagediff.py
        - uses Pillow branch of PIL library
        - compares two images and creates a greyscale third image of the difference
        - the "difference" is highlighted on a scale to black and white
        - seems to take too long

    - opencv\_picdiff.py
        - outputs a grayscale image of thresholding
        - detects way too many differences (i.e. pixel by pixel comparison, unclean)

    - opencv\_imgsubtraction.py
        - outputs a "subtracted" image
        - still detects ALL the differences (because literal pixel subtraction)

    - bg\_subtract\_video.py
        - processes a video and does background subtraction
        - based on movement
        - may not work on little movement? depends on thresholding

    - background_subtraction.py
        - this program uses background subtraction methods from OpenCV. 
        - you can process both videos and images
