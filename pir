import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(4, GPIO.IN)
while True:
	i=GPIO.input(4)
	if i==0:
		print("No Motion")
		time.sleep(0.1)
	if i==1:
		print("Motion Detected")
		time.sleep(0.1)
