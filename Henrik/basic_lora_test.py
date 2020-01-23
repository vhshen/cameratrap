# Used to test ability for pi to send empty data packet over LoRa

import time
import busio
import digitalio
import board
from adafruit_tinylora.adafruit_tinylora import TTN, TinyLoRa

# Create library
i2c = busio.I2C(board.SCL, board.SDA)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = digitalio.DigitalInOut(board.D27)
irq = digitalio.DigitalInOut(board.D27)
rst = digitalio.DigitalInOut(board.D22)

# TTN device address
devaddr = bytearray([0x26, 0x02, 0x12, 0xD2])

# TTN Network key
nwkey = bytearray([0x4D, 0x79, 0x70, 0xE0, 0xED, 0xDC, 0x3C, 0xA1, 0xF7, 0x5F, 
0xE0, 0xF7, 0xD4, 0x15, 0x98, 0x8D])

# TTN Application key
app = bytearray([0x4F, 0x1B, 0xF2, 0x81, 0xCE, 0x85, 0xF1, 0xA8, 0xA6,
0x48, 0x31, 0xBF, 0xBF, 0x61, 0xDA, 0x57])

ttn_config = TTN(devaddr, nwkey, app, country='US')

lora = TinyLoRa(spi, cs, irq, rst, ttn_config)

# Data packet to send to TTN
data = bytearray(4)

while True:
	print('Sending packet...')
	lora.send_data(data, len(data), lora.frame_counter)
	print('Packet sent!')
	lora.frame_counter += 1
	time.sleep(2)
	
