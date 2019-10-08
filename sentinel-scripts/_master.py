import sys
import subprocess
import os
import io
import pathlib as Path
import time
import mode_cnn
import crop_bb
import numpy as np
import csv

## Master Script for CXL Camera Trap Control
trigger = 'pir'     # 'pir' or 'ir'
trigger_check = 'ir'    # 'ir' or 'paired_pir'
trigger_sensitivity = '20'  #int between 1-100 (twenty being highest sensitivity)
t_background = ''   # int
t_lorawan = ''  # int
sys_mode = 'test' # 'real'
max_images = 10 # number of images to run in test scenario
save_cropped_im = 1
reset_results = 1
mcu = 'computer' # computer, rpi0
vpu = 'coral_acc' # computer, rpi0, coral_acc, coral_chip, intel, sipeed
primary_format = 'tflite' #xnor, keras, tflite
primary_type = 'image'
primary_labels = '../models/tflite/deer_binary_v0_2/dict.txt'#'models/tflite/spermwhale/spermwhale_edge_v0_1.txt'
primary_model = '../models/tflite/deer_binary_v0_2/model.tflite'#'models/tflite/spermwhale/spermwhale_edge_v0_1.tflite'
primary_data_directory = '../data/test'
primary_results_directory = '../cameratrap/data/results'
secondary_format = ''
secondary_type = ''
secondary_labels = ''
secondary_model = ''
secondary_data_directory = ''
secondary_results_directory = ''
results_directory = ''
device_identifier = ''
comms_type = ''#'lora_rfm9x' #'lora_rfm9x'
comms_backend = 'ttn'
background_subtraction = ''
current_background = ''
resolution = [300,300,4]
ai_sensitivity = 0.95
lora_counter = 0


# Set up System
#if reset_results == 1:
#    import os, shutil
#    folder = primary_results_directory
#    for the_file in os.listdir(folder):
#        file_path = os.path.join(folder, the_file)
#        try:
#            if os.path.isfile(file_path):
#                os.unlink(file_path)
        #elif os.path.isdir(file_path): shutil.rmtree(file_path)
#        except Exception as e:
#            print(e)

if sys_mode == 'test':
    print('Mode: Test')
if sys_mode == 'real':
    print('Mode: Real')
    if mcu == 'computer':
        print('Cannot run "real" mode from mcu/vpu = computer')
    try:
        import picamera
    except ImportError:
        sys.exit("Requires picamera module. "
                 "Please install it with pip:\n\n"
                 "   pip3 install picamera\n"
                 "(drop the --user if you are using a virtualenv)")
    # Initialize the camera, set the resolution and framerate
    try:
        camera = picamera.PiCamera()
    except picamera.exc.PiCameraMMALError:
        print("\nPiCamera failed to open, do you have another task using it "
              "in the background? Is your camera connected correctly?\n")
        sys.exit("Connect your camera and kill other tasks using it to run "
                 "this sample.")
    if trigger == 'pir':
        import mode_sentinel
        GPIO.setwarnings(False)
        GPIO.setup(4, GPIO.IN)
        print('Loaded: PIR')
if mcu == 'rpi0':
    import board
    import time
    from digitalio import DigitalInOut, Direction, Pull
    import RPi.GPIO as GPIO
    import busio
    import ampy
    import serial
    print('Loaded: CPU')
if vpu == 'coral_acc' :
    from edgetpu.classification.engine import ClassificationEngine
    print('Loaded: VPU')
if background_subtraction != '' :
    import mode_background
    print('Loaded: Background Subtract')
if primary_format or secondary_format == 'keras':
#    from annotation import Annotator
    import csv
    import math
    from pathlib import Path
    import numpy as np
    from PIL import Image
#    from PIL.ExifTags import TAGS
#    import cv2
    import pickle
    import requests
#    import tensorflow as tf
#    import keras
#    from keras.models import load_model
#    from tensorflow.lite.python.interpreter import Interpreter
    print('Loaded: Tensorflow / Keras')
if primary_format or secondary_format == 'tflite':
#    from tflite_runtime.interpreter import Interpreter
    print('Loaded: Tensorflow Lite')

if primary_type or secondary_type== 'image':
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
if comms_type != '':
        if comms_type == 'lora_rfm9x':
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
primary_result = []
primary_result_array = []
print("Successful Setup")


# Loop to run consistently run on RasPi
while True:
    if sys_mode == 'test': # Testing on system
        triggered = 1
    if sys_mode == 'real': # Actual camera scenario
        triggered = mode_sentinel.main(trigger, trigger_check, \
        trigger_sensitivity, image_burst, primary_model_type, secondary_model_type, data_directory)
        print("Event Detected")
    if triggered == 1 :
        # Run Primary Model, which identifies/classifies species + confidence, and saves recorded and boxed images
        print('Spinning up Primary Model', primary_model)
        #[primary_class, primary_confidence, primary_output_file] = ...
        primary_class, primary_confidence = mode_cnn.cnn(sys_mode, mcu, vpu, primary_format, resolution,\
        primary_type, primary_model, primary_labels, \
        primary_data_directory, primary_results_directory, \
        current_background, ai_sensitivity, max_images)
        print('Model Complete')
        print('Insert Code to Save Array in way that can be parsed for LoRa')
        print('NOTE: CROPPED IMAGES AND .CSV RESULTS FILE ARE SAVED IN /DATA/RESULTS FOLDER ')

        # Run Secondary Model (if it exists)
        if secondary_model :
            #[secondary_class, secondary_confidence, secondary_output_file] = ...
            secondary_class, secondary_confidence = mode_cnn.main(sys_mode, mcu, vpu, secondary_format, resolution,\
            secondary_type, secondary_model, secondary_labels,\
            primary_results_directory, secondary_results_directory,
        current_background, ai_sensitivity, max_images)
            print('Insert outcome from secondary model:')# secondary_class, secondary_confidence)
        # Run LoRa communication with outputs from primary algorithm
        if comms_type != '':
            lora_counter = mode_comms.main(primary_class, sum(primary_confidence), secondary_class, secondary_confidence,\
            device_identifier, comms_type, comms_backend, lora_counter)
        if sys_mode == 'test':
            sys.exit('Completed Scenario')
        if syst_mode == 'real':
            triggered == 0
            print('System Reset')
    if trigger_check == 0 and t_backgrond != 0 and time > t_backgrond :
        current_background = mode_background.main()
        t_background = 0
    if trigger_check == 0 and t_lorawan != 0 and time > t_lorawan :
        lorawan.main(comms_type, comms_backend)
        t_lorawan = 0
