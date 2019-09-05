import time
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
from adafruit_tinylora.adafruit_tinylora import TTN, TinyLoRa
import subprocess

# Set Pin Outs
i2c = busio.I2C(board.SCL, board.SDA)
cs  = DigitalInOut(board.D27)
rst = DigitalInOut(board.D22)
irq = DigitalInOut(board.D23) #16
spi=busio.SPI(board.SCK, MOSI= board.MOSI, MISO=board.MISO)

#cs  = DigitalInOut(board.D27)  # 13
#rst = DigitalInOut(board.D22)  # 15
#irq = DigitalInOut(board.D23)  # aka G0 #16
#en  = DigitalInOut(board.D17)  # 11

# TTN Device Address, 4 Bytes, MSB
devaddr = bytearray([0x26, 0x02, 0x1B, 0xD9])
 
# TTN Network Key, 16 Bytes, MSB
nwkey = bytearray([0xF0, 0x23, 0x39, 0x26, 0xEC, 0x19, 0x1B, 0x77, 
					0x8B, 0x23, 0xC8, 0x5D, 0x08, 0xA5, 0xDF, 0xDD])
 
# TTN Application Key, 16 Bytess, MSB
app = bytearray([0xDD, 0x91, 0x7C, 0x2B, 0x6F, 0xE7, 0xA0, 0x17, 0x32, 
					0x5F, 0x50, 0x09, 0xE2, 0xBB, 0x4E, 0xBE])
                     
ttn_config = TTN(devaddr, nwkey, app, country='US')
 
lora = TinyLoRa(spi, cs, irq, rst, ttn_config, channel=0)

# Data Packet to send to TTN

while True:
    data = bytearray(b"\x34\x55\x94\x13")
    print('Sending packet...')
    lora.send_data(data, len(data), lora.frame_counter)
    print('Packet sent!')
    lora.frame_counter += 1
    time.sleep(10)
