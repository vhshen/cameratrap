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
camera = 'PiCamera'
t_background = ''   # int
t_lorawan = ''  # int
sys_mode = 'test' # 'real'
max_images = 100 # number of images to run in test scenario
save_cropped_im = 1
reset_results = 1
mcu = 'computer' # computer, rpi0
primary_format = 'tflite' #coral, tf_lite,tensorflow, tflite
primary_type = 'image'
secondary_format = ''
secondary_type = ''
device_identifier = ''
comms_type = ''#'lora_rfm9x' #'lora_rfm9x'
comms_backend = 'ttn'
background_subtraction = ''
current_background = ''
resolution = [300,300,4]
ai_sensitivity = 0.6
lora_counter = 0

if mcu == 'computer':
    import mode_cnn_computer as mode_cnn
if mcu == 'rpi0':
    import mode_cnn

def import_peripherals():

    if camera == 'PiCamera':
        import picamera
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

# Defines the inputs to the script
def user_selections():
    parser = argparse.ArgumentParser()
    parser.add_argument('--sys_mode', required=True,
                        help='Test or Real')
    parser.add_argument('--mcu', required=False, default='rpi0',
                        help='Type of Microcontroller')
    parser.add_argument('--primary_format', required=False, default='coral',
                        help='What format is the model in?')
    parser.add_argument('--secondary_format', required=False, default='coral',
                        help='What format is the model in?')
    parser.add_argument('--primary_type', required=False, default='image',
                        help='Image, Video, Acoustics, Motion')
    parser.add_argument('--secondary_type', required=False, default='image',
                        help='Image, Video, Acoustics, Motion')
    args = parser.parse_args()
    return args

## Initialization


primary_labels = 'models/tflite/deer_binary_v0_2/dict.txt'#'models/tflite/spermwhale/spermwhale_edge_v0_1.txt'
primary_model = 'models/tflite/deer_binary_v0_2/model.tflite'#'models/tflite/spermwhale/spermwhale_edge_v0_1.tflite'
primary_data_directory = '/home/sam/AI_Training/deer_train'
primary_results_directory = 'data/results'
secondary_labels = ''
secondary_model = ''
secondary_data_directory = ''
secondary_results_directory = ''

if sys_mode == 'test':
    print('Mode: Test')
if sys_mode == 'real':
    print('Mode: Real')
    if mcu == 'computer':
        print('Cannot run "real" mode from mcu/vpu = computer')
    if mcu == rpi0:
        primary_format = args.primary_format
        secondary_format = args.secondary_format
        primary_type = args.primary_type
        secondary_type = args.secondary_type



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
        primary_class, primary_confidence = mode_cnn.cnn(sys_mode, mcu, primary_format, resolution,\
        primary_type, primary_model, primary_labels, \
        primary_data_directory, primary_results_directory, \
        current_background, ai_sensitivity, max_images)
        print('Model Complete')
        print('Insert Code to Save Array in way that can be parsed for LoRa')
        print('NOTE: CROPPED IMAGES AND .CSV RESULTS FILE ARE SAVED IN /DATA/RESULTS FOLDER ')

        # Run Secondary Model (if it exists)
        if secondary_model :
            #[secondary_class, secondary_confidence, secondary_output_file] = ...
            secondary_class, secondary_confidence = mode_cnn.main(sys_mode, mcu, secondary_format, resolution,\
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
