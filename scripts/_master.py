## Master Script for CXL Camera Trap Control

trigger = 'pir'     # 'pir' or 'ir'
trigger_check = 'ir'    # 'ir' or 'paired_pir'
trigger_sensitivity = '20'  #int between 1-100 (twenty being highest sensitivity)
t_background = ''   # int
t_lorawan = ''  # int
sys_mode = 'test' # 'real'
mcu = 'rpi0'
vpu = 'rpi0' # rpi0, coral_acc, coral_chip, intel, sipeed
primary_model_format = 'xnor' #xnor, keras
primary_model_type = 'image'
primary_model_file = "deer_model_please_work.h5" # 'species_detector_xnor' #'in-house'#'mobile_net'
primary_data_directory = ''
secondary_model_format = ''
secondary_model_type = ''
secondary_model_file = ''
secondary_data_directory = ''
device_identifier =
comms_type = '' #'lora_rfm9x'
comms_backend = 'ttn'

import sys
import subprocess
import os
import ampy
import serial
import io
import pathlib as Path
import time
import mode_cnn
# Set up System
if system_mode == 'test':
        repo = '/home/pi/cameratrap/data/deer_train'
        print('Mode = Test')
if system_mode == 'real':
    try:
        import picamera
    except ImportError:
        sys.exit("Requires picamera module. "
                 "Please install it with pip:\n\n"
                 "   pip3 install picamera\n"
                 "(drop the --user if you are using a virtualenv)")
    print('Mode = Real')
if mcu == 'rpi0':
        import board
        import time
        from digitalio import DigitalInOut, Direction, Pull
        import RPi.GPIO as GPIO
        import busio
        print('Loaded: CPU')
if vpu == 'rpi0':
        print('Loaded: VPU')
if trigger == 'pir':
        import mode_sentinel
        GPIO.setwarnings(False)
        GPIO.setup(4, GPIO.IN)
        print('Loaded: PIR')
if background_subtraction != '' :
        import mode_background
        print('Loaded: Background Subtract')
if primary_model_format or secondary_model_format == 'keras':
        import keras
        from keras.models import load_model
        import csv
        import math
        from pathlib import Path
        import numpy as np
        from PIL import Image
        from PIL.ExifTags import TAGS
        import cv2
        import pickle
        import requests
        import tensorflow as tf
        print('Loaded: Keras')
if primary_model_format or secondary_model_format == 'xnor':
        import sort_images_into_directories
        try:
        import xnornet
    except ImportError:
        sys.exit("The xnornet wheel is not installed.  "
                 "Please install it with pip:\n\n"
                 "    python3 -m pip install --user xnornet-<...>.whl\n\n"
                 "(drop the --user if you are using a virtualenv)")
        try:
        from PIL import Image
        from PIL import ImageDraw
    except ImportError:
        sys.exit("Requires PIL module. "
                 "Please install it with pip:\n\n"
                 "   pip3 install pillow\n"
                 "(drop the --user if you are using a virtualenv)")
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
        print('Loaded: xnor.ai')
if primary_model_type or secondary_model_type== 'image':
        from PIL import Image
        def imageAdder(path_in):
                path = path_in
                image=cv2.imread(path)
                image2 = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                img = cv2.resize(image, (224,224))
                return img
        def predictor(image):
                test_image_batch=image
                test_image_batch=test_image_batch.reshape(1, 224, 224, 3)
                preds = model.predict_classes(test_image_batch, batch_size=1)
                probs = model.predict(test_image_batch, batch_size=1)
                print(preds)
        print('Loaded: Image Analysis Infrastructure')
if comms != 'none':
        if comms == 'lora_rfm9x':
                import adafruit_rfm9x
                i2c=busio.I2C(board.SCL, board.SDA)
                from adafruit_tinylora.adafruit_tinylora import TTN, TinyLoRa
                import mode_comm_lora
                cs  = DigitalInOut(board.D27)
                rst = DigitalInOut(board.D22)
                irq = DigitalInOut(board.D23) #16
                en  = DigitalInOut(board.D17) #16
                spi=busio.SPI(board.SCK, MOSI= board.MOSI, MISO=board.MISO)
                rfm9x=adafruit_rfm9x.RFM9x(spi, cs, rst, 915.0)
                rfm9x.tx_power=23
                prev_packet=None
                print('Loaded: RF9x LoRa')
        if comms_backend == 'ttn':
                # ttn setup
                devaddr = bytearray([0x26, 0x02, 0x1B, 0xD9])
                nwkey = bytearray([0xF0, 0x23, 0x39, 0x26, 0xEC, 0x19, 0x1B, 0x77,
                                                        0x8B, 0x23, 0xC8, 0x5D, 0x08, 0xA5, 0xDF, 0xDD])
                app = bytearray([0xDD, 0x91, 0x7C, 0x2B, 0x6F, 0xE7, 0xA0, 0x17, 0x32,
                                                        0x5F, 0x50, 0x09, 0xE2, 0xBB, 0x4E, 0xBE])
                ttn_config = TTN(devaddr, nwkey, app, country='US')
                lora = TinyLoRa(spi, cs, irq, rst, ttn_config, channel=0)
                print('Loaded: The Things Network')
if sys.version_info[0] < 3:
    sys.exit("This sample requires Python 3. Please install Python 3!")
time = 0
print("Successful Setup")


# Loop to run consistently run on RasPi
while True:
    tic = time.clock()
    if system_mode == 'test': # Testing on system
        trigger_check = 1
    if system_mode == 'real': # Actual camera scenario
        trigger_check = mode_sentinel.main(trigger, trigger_check, trigger_sensitivity, primary_model_type, secondary_model_type, data_directory)
        print("Event Detected")
    if trigger_check == 1 :
        # Run Primary Model, which identifies/classifies species + confidence, and saves recorded and boxed images
        print('Spinning up Primary Model')
        [primary_class, primary_confidence, primary_output_file] = ...
            ... mode_cnn.main(sys_mode, mcu, vpu, primary_model_format, primary_model_type, primary_model_file, data_directory, current_background)
        print('Insert outcome from primary model, queing xxxx model')
        # Run Secondary Model (if it exists)
        if secondary_model_file :
            [secondary_class, secondary_confidence, secondary_output_file] = ...
                ... mode_cnn.main(system_mode, secondary_model_type, secondary_model_format, secondary_model_file, secondary_data_directory)
            print('Insert outcome from secondary model')
        # Run LoRa communication with outputs from primary algorithm
        if comms_type != '':
            mode_comms.main(primary_class, primary_confidence, secondary_class, secondary_confidence, device_identifier, comms_type, comms_backend)
    if trigger_check == 0 t_backgrond != 0 and time > t_backgrond :
        current_background = mode_background.main()
        t_background = 0
    if trigger_check == 0 and t_lorawan != 0 and time > t_lorawan :
        lorawan.main(comms_type, comms_backend)
        t_lorawan = 0
    toc = time.clock()
    time = toc - tic
