## This is a script of functions that are stable, please do not push until your code is stable

def sentinel()
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

def cwd()
	pass

def background()
	pass

def comm_lora(data)
	lora.send_data(data, len(data), lora.frame_counter)
	print('Packet sent!')
	lora.frame_counter += 1

def primary_im_cnn(photo)
	if :
		print("Class Found")
		data = bytearray(b"\x01\x01\x00\x00")
		if class==deer:
			stable_modes.cwd()
		elif class==dog:
			pass
		else
			pass
		stable_modes.comm_lora()
	else :
		print("False Positive")
