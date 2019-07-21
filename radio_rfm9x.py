"""
Example for using the RFM9x Radio with Raspberry Pi.
https://learn.adafruit.com/lora-and-lorawan-radio-for-raspberry-pi/sending-data-using-a-lora-radio

 
Learn Guide: https://learn.adafruit.com/lora-and-lorawan-for-raspberry-pi
Author: Brent Rubell for Adafruit Industries
"""
# Import Python System Libraries
import time
# Import Blinka Libraries
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
# Import the SSD1306 module.
#import adafruit_ssd1306
# Import RFM9x
import adafruit_rfm9x
 
 
# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

# Configure LoRa Radio
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
rfm9x.tx_power = 23
prev_packet = None
 
while True:
    packet = None
 
    # check for packet rx
    packet = rfm9x.receive()
    if packet is None:
        print('- Waiting for PKT -', 15, 20, 1)
    else:
        # Display the packet text and rssi
        prev_packet = packet
        packet_text = str(prev_packet, "utf-8")
        print('RX: ', 0, 0, 1)
        print(packet_text, 25, 0, 1)
        time.sleep(1)
 
        # Send Message
        button_a_data = bytes("Button A!\r\n","utf-8")
        rfm9x.send(button_a_data)
        print('Sent Button A!', 25, 15, 1)
   
    time.sleep(0.1)
