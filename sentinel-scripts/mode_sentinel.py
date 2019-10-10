
## Setup (Copy stable version into _master.py)

## Script (Copy stable version into a function in stable_modes.py)
from __future__ import print_function
import argparse
import os
import shutil
import sys
import RPi.GPIO as GPIO
import time

def save_data(image,results,path,ext='jpeg'):
    tag = '%010d' % int(time.monotonic()*1000)
    name = '%simg-%s.%s' %(path,tag,ext)
    image.save(name)
    print('Frame saved as: %s' %name)
    logging.info('Image: %s Results: %s', tag,results)

def user_selections():
    parser = argparse.ArgumentParser()
    parser.add_argument('--trigger', required=True,
                        help='Type of trigger')
    parser.add_argument('--trigger_check', required=False, default='',
                        help='Any additional trigger check methods')
    parser.add_argument('--trigger_sensitivity', required=True,
                        help='how sensitive is the trigger')
    parser.add_argument('--image_burst', required=False, default = 0,
                        help='How many images are taken immediately')
    parser.add_argument('--model_type', required=False, default = 'image',
                        help='Image, Video, Acoustics, Motion')
    parser.add_argument('--data_directory', required=True,
                        help='Where are the burst images being saved?')
    args = parser.parse_args()
    return args

def main(trigger, trigger_check, trigger_sensitivity, image_burst, \
    model_type, data_directory):
    trigger_count = 0
    # check if trigger exists, if it doesn't break this script and return to _master.py
    if trigger :
           print('No trigger is specified, moving forward with script')
           return 0
    if trigger == pir :
        while True :
    		#Take input from PIR sensor
                pir_status = GPIO.input(4)
    		#If no motion detected by PIR sensor
                if pir_status == 0:
    		        print('No Motion')
    		        trigger_count = 0
    		#If motion detected by PIR sensor
                if pir_status == 1:
    			if trigger_count <= args.trigger_sensitivity:
    				print('Motion Detected, awaiting confirmation')
    				time.sleep(0.5)
    				j = j + 1
    				print(j)
                else:
                    print('Insert Flash Stuff')
                    burst = 0
                    if burst < 6:
                        camera.start_recording(stream, format="rgb")
                        image = stream.getvalue()
                        save_data(image,results,args.data_directory,ext='jpeg')
                        print('Taking photo burst')
                        burst += 1
                    else :
                        return 1
                        break

if __name__ == "__main__":
    main()
