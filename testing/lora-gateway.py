"""Using TinyLoRa with a Si7021 Sensor.
"""
import time
import busio
import digitalio
import board
#import adafruit_si7021
from adafruit_tinylora.adafruit_tinylora import TTN, TinyLoRa
 
# Board LED
#led = digitalio.DigitalInOut(board.D13)
#led.direction = digitalio.Direction.OUTPUT
 
# Create library object using our bus i2c port for si7021
#i2c = busio.I2C(board.SCL, board.SDA)
#sensor = adafruit_si7021.SI7021(i2c)
 
# Create library object using our bus SPI port for radio
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
 
# RFM9x Breakout Pinouts
cs = digitalio.DigitalInOut(board.D5)
irq = digitalio.DigitalInOut(board.D6)
rst = digitalio.DigitalInOut(board.D4)
 
# Feather M0 RFM9x Pinouts
# cs = digitalio.DigitalInOut(board.RFM9X_CS)
# irq = digitalio.DigitalInOut(board.RFM9X_D0)
# rst = digitalio.DigitalInOut(board.RFM9x_RST)
 
# TTN Device Address, 4 Bytes, MSB
devaddr = bytearray([0x26, 0x02, 0x1B, 0xD9])
 
# TTN Network Key, 16 Bytes, MSB
nwkey = bytearray([0xF0, 0x23, 0x39, 0x26, 0xEC, 0x19, 0x1B, 0x77, 
					0x8B, 0x23, 0xC8, 0x5D, 0x08, 0xA5, 0xDF, 0xDD])
 
# TTN Application Key, 16 Bytess, MSB
app = bytearray([0xDD, 0x91, 0x7C, 0x2B, 0x6F, 0xE7, 0xA0, 0x17, 0x32, 
					0x5F, 0x50, 0x09, 0xE2, 0xBB, 0x4E, 0xBE])
 
ttn_config = TTN(devaddr, nwkey, app, country='US')
 
lora = TinyLoRa(spi, cs, irq, rst, ttn_config)
 
# Data Packet to send to TTN
data = bytearray(4)
 
while True:
    temp_val = test2
    humid_val = test3
    print('Temperature: %0.2f C' % temp_val)
    print('relative humidity: %0.1f %%' % humid_val)
 
    # Encode float as int
    temp_val = int(temp_val * 100)
    humid_val = int(humid_val * 100)
 
    # Encode payload as bytes
    data[0] = (temp_val >> 8) & 0xff
    data[1] = temp_val & 0xff
    data[2] = (humid_val >> 8) & 0xff
    data[3] = humid_val & 0xff
 
    # Send data packet
    print('Sending packet...')
    lora.send_data(data, len(data), lora.frame_counter)
    print('Packet Sent!')
    led.value = True
    lora.frame_counter += 1
    time.sleep(2)
    led.value = False
