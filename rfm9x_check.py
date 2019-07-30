import time
import busio
from digitalio import DigitalInOut, Direction, Pull
import board

import adafruit_rfm9x
i2c=busio.I2C(board.SCL, board.SDA)
CS=DigitalInOut(board.CE1)
RESET=DigitalInOut(board.D25)
spi=busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
while True:
	try:
		rfm9x=adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
		print('RFM9x: Detected', 0,0,1)
	except RuntimeError:
		print('RFM9x: ERROR', 0, 0,1) 
	time.sleep(0.1)
