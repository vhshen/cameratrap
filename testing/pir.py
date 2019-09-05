import RPi.GPIO as GPIO
import time
from time import sleep 
import busio
import board 
i2c=busio.I2C(board.SCL, board.SDA)
from picamera import PiCamera
camera=PiCamera()

GPIO.setwarnings(False)
GPIO.setup(4, GPIO.IN)
while True:
	i=GPIO.input(4)
	if i==0:
		print("No Motion")
		sleep(1)
	if i==1:
		print("Motion Detected")
		camera.capture('/home/pi/Desktop/img.jpg')
		sleep(5)
		i=0
