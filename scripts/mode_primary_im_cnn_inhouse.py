import keras
from keras.models import load_model
import tensorflow as tf
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
import sys

model_file="deer_model_please_work.h5"
model=tf.keras.models.load_model(model_file)
config=model.get_config()
weights=model.get_weights()
image_path='testers/Deer_Test1514.jpg'

def imageAdder(path_in):
  path= path_in
  image=cv2.imread(path)
  image2= cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
  img=cv2.resize(image, (224,224))
  return img
  
img=imageAdder(image_path)
img=img/255


def predictor(image):
  test_image_batch=image
  test_image_batch=test_image_batch.reshape(1, 224, 224, 3)
  preds= model.predict_classes(test_image_batch, batch_size=1)
  probs= model.predict(test_image_batch, batch_size=1)
  print(preds)


predictor(img)
