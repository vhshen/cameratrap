## Do this inside a function such that we can call as a function from the master script
"""
from xnor.ai
This is an example to show case about xnornet surveillance use cases.
The example needs to work with a person classification/detection model.
"""


import argparse
import os
import sys

if sys.version_info[0] < 3:
    sys.exit("This sample requires Python 3. Please install Python 3!")

try:
    from PIL import Image
    from PIL import ImageDraw
except ImportError:
    sys.exit("Requires PIL module. "
             "Please install it with pip:\n\n"
             "   pip3 install pillow\n"
             "(drop the --user if you are using a virtualenv)")

try:
    import picamera
except ImportError:
    sys.exit("Requires picamera module. "
             "Please install it with pip:\n\n"
             "   pip3 install picamera\n"
             "(drop the --user if you are using a virtualenv)")

try:
    import xnornet
except ImportError:
    sys.exit("The xnornet wheel is not installed.  "
             "Please install it with pip:\n\n"
             "    python3 -m pip install --user xnornet-<...>.whl\n\n"
             "(drop the --user if you are using a virtualenv)")

## Define Functions
def _draw_pillow_rectangle_with_width(pillow_draw, xy, color=None, width=1):
    """ImageDraw does not support drawing rectangle with width, this is a
    utility function that will draw rectangle with a specific width.
    """
    (x1, y1), (x2, y2) = xy
    offset = 1
    for i in range(0, width):
        pillow_draw.rectangle(((x1, y1), (x2, y2)), outline=color)
        x1 = x1 - offset
        y1 = y1 + offset
        x2 = x2 + offset
        y2 = y2 - offset

def _make_argument_parser():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument(
        "--input_resolution", action='store', nargs=2, type=int,
        default=(1280, 720),
        help="Input Resolution of the camera, which is also the resolution of "
        "the final saved image.")
    parser.add_argument("--output_filename", action='store',
                        default="person.png",
                        help="Filename of the captured output.")
    parser.add_argument("--no_draw_bounding-box", action='store_true',
                        help="Do not draw any bounding boxes.")
    parser.add_argument(
        "--camera_frame_rate", action='store', type=int, default=15,
        help="Adjust the framerate of the camera. 0 indicates a dynamic range "
             "of framerate.")
    parser.add_argument(
        "--camera_brightness", action='store', type=int, default=65,
        help="Adjust the brightness of the camera. Range from 0 to 100.")
    parser.add_argument(
        "--camera_shutter_speed", action='store', type=int, default=1500,
        help="Adjust the shutter speed of the camera in microseconds. "
        "0 means auto shutter speed."
        "https://picamera.readthedocs.io/en/release-1.13/api_camera.html#picamera.PiCamera.shutter_speed")
    parser.add_argument(
        "--camera_video_stablization", action='store_true',
        help="Whether to turn on the video stablization, video "
        "stablization improves video during motion.")
    parser.add_argument(
        "--bounding_box_color", action='store', default="red",
        help="Bounding box color. Accepts common HTML color names.")
    parser.add_argument(
        "--camera_flash", action='store', type=int, default=0,
        help="Camera IR Flash On/Off")
    parser.add_argument(
        "--detection_confidence", action='store', type=int, default=5,
        help="If anything is detected consecutively for detection_confidence "
        "times, then we consider the object to be detected.")
    return parser

def _convert_to_pillow_img(cam_buffer, resolution):
    """Convert the @cam_buffer, which is a python camera buffer, to pillow image
    """
    print("Converting buffer to image...")
    image = Image.frombytes("RGB", resolution[0:2], cam_buffer)
    print("Finished conversion.")
    return image

def _save_image_to_disk(image, output_filename):
    """Save the image to disk with @output_filename
    """
    print("Saving image...")
    image.save(output_filename)
    print("Image saved to \'{}\'".format(os.path.abspath(output_filename)))

def _draw_bounding_box(image, bounding_boxes, resolution, color):
    """Draw the bounding boxes on top of the image
    """
    print("Drawing {} bounding boxes...".format(len(bounding_boxes)))
    for bounding_box in bounding_boxes:
        draw = ImageDraw.Draw(image)
        # Get the initial x and y coordinates times the respective dimension
        x0y0 = (int(bounding_box.x * resolution[0]),
                int(bounding_box.y * resolution[1]))
        # Get the initial x and y + bounding box width and height times the
        # respective dimension to be the other coordinate for rectangle
        x1y1 = (int((bounding_box.x + bounding_box.width) * resolution[0]),
                int((bounding_box.y + bounding_box.height) * resolution[1]))
        _draw_pillow_rectangle_with_width(draw, [x0y0, x1y1], color, 5)
    print("Finished drawing.")
    return image



def main(args=None):
    parser = _make_argument_parser()
    args = parser.parse_args(args)

    # Reconstruct the input resolution to include color channel
    input_res = (args.input_resolution[0], args.input_resolution[1], 3)
    SINGLE_FRAME_SIZE_RGB = input_res[0] * input_res[1] * input_res[2]

    # Initialize the camera, set the resolution and framerate
    try:
        camera = picamera.PiCamera()
    except picamera.exc.PiCameraMMALError:
        print("\nPiCamera failed to open, do you have another task using it "
              "in the background? Is your camera connected correctly?\n")
        sys.exit("Connect your camera and kill other tasks using it to run "
                 "this sample.")

    # Initialize the buffer for picamera to hold the frame
    # https://picamera.readthedocs.io/en/release-1.13/api_streams.html?highlight=PiCameraCircularIO
    stream = picamera.PiCameraCircularIO(camera, size=SINGLE_FRAME_SIZE_RGB)
    # All essential camera settings
    camera.resolution = input_res[0:2]
    camera.framerate = args.camera_frame_rate
    camera.brightness = args.camera_brightness
    camera.shutter_speed = args.camera_shutter_speed
    camera.video_stabilization = args.camera_video_stablization

    # Record to the internal CircularIO
    #Start Flash
    #cam_flash()
    camera.start_recording(stream, format="rgb")
    # Load model
    model = xnornet.Model.load_built_in()

    #if "person" not in model.class_labels:
    #    sys.exit(model.name + " doesn't classify 'person', exiting.")

    print("Species CNN")
    print("Model: {}".format(model.name))
    print("  version {!r}".format(model.version))
    

    animal_detected = 0             # Initialize Animal Detector Counter (Confidence) 
    detected_last_frame = False     # Initialize Detection Status
    bounding_boxes = []             # 
    false_positive = 0              # Initialize False Positive Counter
    false_positive_threshold = 5    # How many frames to check before giving up
    
    while false_positive < false_positive_threshold:
        detected_this_frame = False
        # Get the frame from the CircularIO buffer.
        cam_buffer = stream.getvalue()
        # The camera has not written anything to the CircularIO yet, thus no frame is been captured
        if len(cam_buffer) != SINGLE_FRAME_SIZE_RGB:
            continue
        # Passing corresponding RGB
        model_input = xnornet.Input.rgb_image(input_res[0:2], cam_buffer)
        # Evaluate
        results = model.evaluate(model_input)
        # Check frame model results
        for result in results:
            local_animal_detected = False
            local_animal_detected = result.class_label.label == 'bird'
            # If we already detected animal in this frame, we don't want to over count.
            if local_animal_detected and not detected_this_frame:
                if animal_detected < args.detection_confidence:
                    # If we haven't confirmed, then increase our confidence.
                    if detected_last_frame:
                        animal_detected += 1
                    # If we didn't confirm last frame but we detected in this frame, we want to reset our confidence.
                    else:
                        animal_detected = 1
            # We detected an animal in this frame
            if local_animal_detected:
                detected_this_frame = True
            # Update the history
            detected_last_frame = detected_this_frame
            # Draw Bounding Box
            bounding_boxes.append(result.rectangle)
        if animal_detected >= args.detection_confidence:
            # Classification model
            if len(bounding_boxes) == 0:
                print("Animal detected!")
            else:  # Detection model
                print("{} animal detected!".format(len(bounding_boxes)))
            image = _convert_to_pillow_img(cam_buffer, input_res)
            if not (args.no_draw_bounding_box) and len(bounding_boxes) != 0:
                image = _draw_bounding_box(image, bounding_boxes, input_res,
                                           args.bounding_box_color)
            _save_image_to_disk(image, args.output_filename)
        else:
            print("Checking...")
            false_positive += 1
            
    print("Cleaning up...")
    camera.stop_recording()
    camera.close()
    print("")


if __name__ == "__main__":
    main()
