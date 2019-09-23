## Setup (Copy stable version into _master.py)

## Script (Copy stable version into a function in stable_modes.py)
from __future__ import print_function
import argparse
import os
import shutil
import sys
import RPi.GPIO as GPIO
import time

def main(args=None):

    if trigger
	j = 0
	while True:
		#Take input from PIR sensor
		i=GPIO.input(4)
		#If no motion detected by PIR sensor
		if i==0:
			print('No Motion')
			j = 0
		#If motion detected by PIR sensor
		if i==1:
			if j <= 15:
				print('Motion Detected')
				time.sleep(0.5)
				j = j + 1
				print(j)
			if j == 6:

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
				break


if __name__ == "__main__":
    main()
