<<<<<<< HEAD
## Master Script for CXL Camera Trap Control

=======
>>>>>>> 87de2fef14b5a094491edb2d40336150ddfb85d4
#Imported needed libraries
import time
import sys
import subprocess
import os

# Simulation with Onboard Files??
test = 0

# Import External Scripts
# import stable_modes
import mode_background
import mode_comm_lora
import mode_primary_im_cnn
<<<<<<< HEAD
import mode_primary_im_cnn_simulation
=======
>>>>>>> 87de2fef14b5a094491edb2d40336150ddfb85d4
import mode_sentinel
import sort_images_into_directories
import rpi_setup
import time

rpi_setup.main()


#Loop to run consistently run on RasPi

while True:
	input_image = "data/deer_train/Deer_Test1502.jpg"
	# Run Sentinel
	mode_sentinel.main()
	if test == 0:
		mode_primary_im_cnn.main()
	if test == 1:
		mode_primary_im_cnn_simulation.main(
		input_image
		)
	else :
		break
