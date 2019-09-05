#Imported needed libraries 
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
import serial
import time
import RPi.GPIO as GPIO
from time import sleep 
import serial

#Define serial port for communication to Sipeed MAix BiT
ser=serial.Serial('/dev/ttyUSB0')

#Set up for LoRa Radio Transceiver Breakout
CS= DigitalInOut(board.D27)
RESET= DigitalInOut(board.D22)
spi=busio.SPI(board.SCK, MOSI= board.MOSI, MISO=board.MISO)
rfm9x=adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
rfm9x.tx_power=23
prev_packet=None

#Set up for PIR Motion Sensor
GPIO.setwarnings(False)
GPIO.setup(4, GPIO.IN)

#Run AI algorithm on Sipeed MAix BiT
os.system("ampy --port /dev/ttyUSB0 run find_face.py")

#Loop to consistently run on RasPi
while True:
	packet=None
	#Take input from PIR sensor 
	i=GPIO.input(4)
	#If no motion detected by PIR sensor
	if i==0:
		#mess= bytes("Test\r\n", "utf-8")
		#Send message to base station radio
		#rfm9x.send(mess)
		sleep(0.5)
	#If motion detected by PIR sensor
	if i==1:
		#S is variable for if face is detected or not
		s = False
		#Receive input from Sipeed MAix BiT
		with serial.Serial('/dev/ttyUSB0',1500000 , timeout=1) as ser:
			s=ser.read(10)
		#If no message is received from the LoRa Radio
		if packet is None:
			#If a face is founded by the Sipeed MAix BiT
			if s: 
				mess= bytes("Found Face\r\n", "utf-8")
				#Send message to base station radio
				rfm9x.send(mess)
				print("Detected motion, found face, sent message")
			#If a face is not found by Sipeed MAix BiT
			else:
				mess= bytes("No Face\r\n", "utf-8")
				#Send message to base station radio
				rfm9x.send(mess)
				print("Detected motion but no face")
		#If a message is received by the LoRa radio
		else:
			packet=rfm9x.receive()
			prev_packet= packet
			packet_text= str(prev_packet, "utf-8")
			print('Mess Received: ', 0, 0, 1)
			print(packet_text, 25, 0, 1)
			time.sleep(1)
		sleep(5)
		i=0
		time.sleep(0.1)
