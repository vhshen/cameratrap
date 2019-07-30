import time
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
import adafruit_rfm9x
i2c=busio.I2C(board.SCL, board.SDA)
CS= DigitalInOut(board.D27)
RESET= DigitalInOut(board.D22)
spi=busio.SPI(board.SCK, MOSI= board.MOSI, MISO=board.MISO)
rfm9x=adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
rfm9x.tx_power=23
prev_packet=None
while True:
	packet=None
	packet=rfm9x.receive()
	if packet is None:
		print('-Waiting for PKT-', 15, 20, 1)
		button_a_data= bytes("hi\r\n", "utf-8")
		rfm9x.send(button_a_data)
		print('Sent', 25,15,1)
	else:
		prev_packet= packet
		packet_text= str(prev_packet, "utf-8")
		print('RX: ', 0, 0, 1)
		print(packet_text, 25, 0, 1)
		time.sleep(1)
		
	time.sleep(0.1)
