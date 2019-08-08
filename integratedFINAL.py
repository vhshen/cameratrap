import time
import board
import busio
import sys
import subprocess
from digitalio import DigitalInOut, Direction, Pull
import adafruit_rfm9x
i2c=busio.I2C(board.SCL, board.SDA)
import RPi.GPIO as GPIO
from time import sleep
import keras
from keras.models import load_model
import os
import glob
import csv
import math
from pathlib import Path
import numpy as np
from PIL import Image
from PIL.ExifTags import TAGS
import cv2
import pickle 
import requests

#Set up for LORA
CS=DigitalInOut(board.D27)
RESET=DigitalInOut(board.D22)
spi=busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x=adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
rfm9x.tx_power=23
prev_packet=None

#Set up PIR Motion Sensor
GPIO.setwarnings(False)
GPIO.setup(4, GPIO.IN)

model_file="deer_model_please_work.h5"
model=tf.keras.models.load_model(model_file)
config=model.get_config()
weights=model.get_weights()
image_path='testers/Deer_Test1514.jpg'

def imageAdder(path_in):
  path= path_in
  image=cv2.imread(path)
  image2= cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
  img=cv2.resize(imaeg, (224,224))
  return img
  
img=imageAdder(image_path)
img=img/255

def predictor(image):
  test_image_batch=image
  test_image_batch=test_image_batch.reshape(1, 224, 224 3)
  preds= model.predict_classes(test_image_batch, batch_size=1)
  probs= model.predict(test_image_batch, batch_size=1)
  print(preds)

while True:
  packet=None
  p=0
  #Take input from PIR Motion Sensor
  i=GPIO.input(4)
  if i==0:
    sleep(1)
  if i==1:
    p=predictor(img)
    if packet is None:
      if p==1:
        mess=bytes("Found Deer\r\n", "utf-8")
        rfm9x.send(mess)
      else:
        mess=bytes("No Deer Found \r\n", "utf-8")
        rfm9x.send(mess)
    else:
      packet=rfm9x.receive()
      prev_packet=packet
      packet_text=str(prev_packet, "utf-8")
      print('Received:')
      print(packet_text)
      time.sleep(1)
    sleep(5)
    i=0
