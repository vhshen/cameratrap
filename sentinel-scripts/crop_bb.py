def crop(image, x1, x2, y1, y2) :
    # Improting Image class from PIL module
    from PIL import Image

    # Opens a image in RGB mode
    im = Image.open(image)

    # Cropped image of above dimension
    # (It will not change orginal image)
    im_crop = im.crop((x1, y1, x2, y2))

    # Shows the image in image viewer
    #im_crop.show()

    return im_crop
