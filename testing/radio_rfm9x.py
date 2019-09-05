import time
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
import adafruit_rfm9x
from adafruit_tinylora.adafruit_tinylora import TTN, TinyLoRa

# Set Pin Outs
i2c = busio.I2C(board.SCL, board.SDA)
cs  = DigitalInOut(board.D27)
rst = DigitalInOut(board.D22)
irq = DigitalInOut(board.D16)
spi=busio.SPI(board.SCK, MOSI= board.MOSI, MISO=board.MISO)

# Set LoRa Set
#rfm9x=adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
#rfm9x.tx_power=23
#rfm9x.spreading_factor=10
#prev_packet=None
#count =0 

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

temp_val  = 0xff
humid_val = 0xff

while True:
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


#while True:
#	packet=None
#	packet=rfm9x.receive()
#	if packet is None:
#		print('-Waiting for PKT-', 15, 20, 1)
#		button_a_data= bytes("hi\r\n", "utf-8")
#		rfm9x.send(button_a_data)
	#	print('Sent', 25,15,1)
	#	time.sleep(0.5)
#	else:
#		prev_packet= packet
#		packet_text= str(prev_packet, "utf-8")
#		print('RX: ', 0, 0, 1)
#		print(packet_text, 25, 0, 1)
#		time.sleep(0.5)
#	time.sleep(0.1)
