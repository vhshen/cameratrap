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
import time
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
from adafruit_tinylora.adafruit_tinylora import TTN, TinyLoRa
import subprocess

#Define serial port for communication to Sipeed MAix BiT
ser=serial.Serial('/dev/ttyUSB0')

#l ora setup
# Set Pin Outs
i2c = busio.I2C(board.SCL, board.SDA)
cs  = DigitalInOut(board.D27)
rst = DigitalInOut(board.D22)
irq = DigitalInOut(board.D23) #16
en  = DigitalInOut(board.D17) #16
spi=busio.SPI(board.SCK, MOSI= board.MOSI, MISO=board.MISO)
rfm9x=adafruit_rfm9x.RFM9x(spi, cs, rst, 915.0)
rfm9x.tx_power=23
prev_packet=None
# ttn setup
devaddr = bytearray([0x26, 0x02, 0x1B, 0xD9])
nwkey = bytearray([0xF0, 0x23, 0x39, 0x26, 0xEC, 0x19, 0x1B, 0x77, 
					0x8B, 0x23, 0xC8, 0x5D, 0x08, 0xA5, 0xDF, 0xDD])
app = bytearray([0xDD, 0x91, 0x7C, 0x2B, 0x6F, 0xE7, 0xA0, 0x17, 0x32, 
					0x5F, 0x50, 0x09, 0xE2, 0xBB, 0x4E, 0xBE])                     
ttn_config = TTN(devaddr, nwkey, app, country='US')
lora = TinyLoRa(spi, cs, irq, rst, ttn_config, channel=0)

#Set up for PIR Motion Sensor
GPIO.setwarnings(False)
GPIO.setup(4, GPIO.IN)
print('Successful Setup')

#Run AI algorithm on Sipeed MAix BiT
os.system("ampy --port /dev/ttyUSB0 run find_face.py")
print('MAix Setup Successful')


#Loop to consistently run on RasPi
while True:
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
		#Receive input from Sipeed MAix BiT
		with serial.Serial('/dev/ttyUSB0',1500000 , timeout=1) as ser:
			s=ser.read(10)
		#If no message is received from the LoRa Radio
		if packet is None:
			#If a face is founded by the Sipeed MAix BiT
			if s: 
				data = bytearray(b"\x01\x01\x00\x00")
			#If a face is not found by Sipeed MAix BiT
			else:
				data = bytearray(b"\x01\x00\x00\x00")
				print("Detected motion but no face")
	lora.send_data(data, len(data), lora.frame_counter)
	print('Packet sent!')
	lora.frame_counter += 1
	sleep(10)
