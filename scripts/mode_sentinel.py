## Setup (Copy stable version into _master.py)

## Script (Copy stable version into a function in stable_modes.py)
from __future__ import print_function
import argparse
import os
import shutil
import sys


if sys.version_info[0] < 3:
    sys.exit("This sample requires Python 3. Please install Python 3!")

def main(args=None):
	#Take input from PIR sensor
	i=GPIO.input(4)
	#If no motion detected by PIR sensor
	if i==0:
		print('No Motion')
	#If motion detected by PIR sensor
	if i==1:
		#S is variable for if face is detected or not
		s = False

if __name__ == "__main__":
    main()
