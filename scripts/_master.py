## Master Script for CXL Camera Trap Control
system_mode = 'test' # 'real'
mcu = 'rpi0'
vpu = 'rpi0' # rpi0, coral_acc, coral_chip, intel, sipeed
trigger = 'pir'
trigger_check = 'ir'
background_subtraction = '' # y/n
primary_model_format = 'xnor' #xnor, keras
primary_model_type = 'image' 
primary_model_file = "deer_model_please_work.h5" # 'species_detector_xnor' #'in-house'#'mobile_net'
secondary_model_format = ''
secondary_model_type = ''
secondary_model_file = ''
lora_mesh = ''
comms = 'none'#'lora_rfm9x'
comms_backend = 'ttn'

import sys
import subprocess
import os
import ampy
import serial
import io
import pathlib
# Set up System
if system_mode == 'test':
        repo = '/home/pi/cameratrap/data/deer_train'
        print('Mode = Test')
if system_mode == 'real':
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
        import tensorflow as tf
        print('Loaded: Keras')
if primary_model_format or secondary_model_format == 'xnor':
        import mode_primary_im_cnn
        import mode_primary_im_cnn_simulation
        import sort_images_into_directories
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

print("Successful Setup")

#Loop to run consistently run on RasPi
while True:
        if system_mode == 'real': # Actual camera scenario
                mode_sentinel.main(trigger, trigger_check, background_subtraction, lora_mesh)
                print("Event Detected")
        # Run Primary Model, which identifies/classifies species + confidence, and saves recorded and boxed images
        print('Spinning up Primary Model')
        mode_cnn.main(system_mode, primary_model_type, primary_model_format, primary_model_file)
        print('Insert outcome from primary model, queing xxxx model')
        if secondary_model_file :
                mode_cnn.main(system_mode, secondary_model_type, secondary_model_format, secondary_model_file)
                print('Insert outcome from secondary model')
        # Run LoRa communication with outputs from primary algorithm
        if comms != 'none':
                mode_comms.main(message, comms, comms_backend)
                print('LoRa Message Sent!')
