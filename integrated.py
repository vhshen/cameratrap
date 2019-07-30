import time
import busio
import sys
import subprocess 
import ampy
import os
from digitalio import DigitalInOut, Direction, Pull
import board
import adafruit_rfm9x
i2c=busio.I2C(board.SCL, board.SDA)
print(devices)
import serial
import time
ser=serial.Serial('/dev/ttyUSB0', 19200, timeout=5)
import RPi.GPIO as GPIO
from time import sleep 
from picamera import PiCamera
camera=PiCamera()
CS= DigitalInOut(board.D27)
RESET= DigitalInOut(board.D22)
spi=busio.SPI(board.SCK, MOSI= board.MOSI, MISO=board.MISO)
rfm9x=adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
rfm9x.tx_power=23
prev_packet=None
GPIO.setwarnings(False)
GPIO.setup(4, GPIO.IN)
while True:
	packet=None
	packet=rfm9x.receive()
	i=GPIO.input(4)
	if i==0:
		print("No Motion")
		sleep(1)
	if i==1:
		print("Motion Detected")
		camera.capture('/home/pi/Desktop/img.jpg')
		os.system('ampy --port /dev/ttyUSB0 run find_face.py')
		picture= ser.readline()
		if packet is None and picture==True:
			mess= bytes("Took picture\r\n", "utf-8")
			rfm9x.send(mess)
			print('Sent Mess')
		else:
			prev_packet= packet
			packet_text= str(prev_packet, "utf-8")
			print('Mess Received: ', 0, 0, 1)
			print(packet_text, 25, 0, 1)
			time.sleep(1)
		sleep(5)
		i=0
		time.sleep(0.1)
