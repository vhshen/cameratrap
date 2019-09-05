## Setup (Copy stable version into _master.py)

## Script (Copy stable version into a function in stable_modes.py)

packet=None
	#Take input from PIR sensor
	i=GPIO.input(4)
	#If no motion detected by PIR sensor
	if i==0:
		data = bytearray(b"\x00\x00\x00\x00")
		print('No Motion')
	#If motion detected by PIR sensor
	if i==1:
		#S is variable for if face is detected or not
		s = False
		#Run Primary CNN Mode

		#Receive input image
		image =
		#If no message is received from the LoRa Radio
		if packet is None:
