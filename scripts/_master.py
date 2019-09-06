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

#lora setup
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

# Import External Scripts
import stable_modes
import mode_background
import mode_comm_lora
import mode_primary_im_cnn
import mode_sentinel
import sort_images_into_directories
import static_image_bounding_box


print('Successful Setup')

#Loop to run consistently run on RasPi
while True:
	 # Run Sentinel
	 mode_sentinel
	 if :
		mode_primary_im_cnn



	 else
	 sleep
