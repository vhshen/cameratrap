## Setup (Copy stable version into _master.py)
from __future__ import print_function
import argparse
import os
import shutil
import sys

def main(args=None):
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

	## Script (Copy stable version into stable_modes.py)

	#If a face is found by the Algorithm
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

if __name__ == '__main__':
    main()
