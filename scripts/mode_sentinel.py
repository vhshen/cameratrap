## Setup (Copy stable version into _master.py)

## Script (Copy stable version into a function in stable_modes.py)
from __future__ import print_function
import argparse
import os
import shutil
import sys
import RPi.GPIO as GPIO
import time


if sys.version_info[0] < 3:
    sys.exit("This sample requires Python 3. Please install Python 3!")

def main(args=None):
	j = 0 
	while True:
		#Take input from PIR sensor
		i=GPIO.input(4)
		#If no motion detected by PIR sensor
		if i==0:
			print('No Motion')
			time.sleep(1)
			j = 0
		#If motion detected by PIR sensor
		if i==1:
			if j <= 15:
				print('Motion Detected')
				time.sleep(0.5)
				j = j + 1
				print(j)
			if j == 6:
				break
		

if __name__ == "__main__":
    main()
