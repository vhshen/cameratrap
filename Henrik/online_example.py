"""Using TinyLoRa with a Si7021 Sensor.
"""
import time
import busio
import digitalio
import board
import adafruit_si7021
from adafruit_tinylora.adafruit_tinylora import TTN, TinyLoRa
 
# Create library object using our bus i2c port for si7021
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_si7021.SI7021(i2c)
 
# Create library object using our bus SPI port for radio
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
 
# RFM9x Breakout Pinouts
cs = digitalio.DigitalInOut(board.D27)
irq = digitalio.DigitalInOut(board.D27)
rst = digitalio.DigitalInOut(board.D22)
 
# Feather M0 RFM9x Pinouts
# cs = digitalio.DigitalInOut(board.RFM9X_CS)
# irq = digitalio.DigitalInOut(board.RFM9X_D0)
# rst = digitalio.DigitalInOut(board.RFM9x_RST)
 
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
 
# Data Packet to send to TTN
data = bytearray(4)
 
while True:
    temp_val = sensor.temperature
    humid_val = sensor.relative_humidity
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
    lora.frame_counter += 1
    time.sleep(2)

