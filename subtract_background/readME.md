Different possible algorithms:

    - PIL\_imagediff.py
        - uses Pillow branch of PIL library
        - compares two images and creates a greyscale third image of the difference
        - the "difference" is highlighted on a scale to black and white
        - seems to take too long

    - opencv\_picdiff.py
        - outputs a grayscale image of thresholding
        - detects way too many differences (i.e. pixel by pixel comparison, unclean)

    - opencv\_picdiff.py
        - outputs a "subtracted" image
        - still detects ALL the differences (because literal pixel subtraction)

