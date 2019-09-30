import argparse
import time
import numpy as np
import os
from annotation import Annotator
from tflite_runtime.interpreter import Interpreter
from PIL import Image
import re
## Master Script for CXL Camera Trap Control
trigger = 'pir'     # 'pir' or 'ir'
trigger_check = 'ir'    # 'ir' or 'paired_pir'
trigger_sensitivity = '20'  #int between 1-100 (twenty being highest sensitivity)
t_background = ''   # int
t_lorawan = ''  # int
sys_mode = 'test' # 'real'
mcu = 'computer' # computer, rpi0
vpu = '' # computer, rpi0, coral_acc, coral_chip, intel, sipeed
primary_format = 'tflite' #xnor, keras, tflite
primary_type = 'image'
labels = 'models/tflite/spermwhale/spermwhale_edge_v0_1.txt'
pmodel = 'models/tflite/spermwhale/spermwhale_edge_v0_1.tflite'
data_directory = 'data/deer_train'
primary_results_directory = 'data/results'
secondary_format = ''
secondary_type = ''
secondary_labels = ''
secondary_model = ''
secondary_data_directory = ''
secondary_results_directory = ''
results_directory = ''
device_identifier = ''
comms_type = '' #'lora_rfm9x'
comms_backend = 'ttn'
background_subtraction = ''
current_background = ''
resolution = [300,300,4]
ai_sensitivity = 0.9


#Saves camera frame and model inference results to user-defined storage directory
def save_data(image,results,path,ext='png'):
    tag = '%010d' % int(time.monotonic()*1000)
    name = '%simg-%s.%s' %(path,tag,ext)
    image.save(name)
    print('Frame saved as: %s' %name)
    logging.info('Image: %s Results: %s', tag,results)
# For
def print_results(start_time, last_time, end_time, results):
    """Print results to terminal for debugging."""
    inference_rate = ((end_time - start_time) * 1000)
    fps = (1.0/(end_time - last_time))
    print('\nInference: %.2f ms, FPS: %.2f fps' % (inference_rate, fps))
    for label, score in results:
      print(' %s, score=%.2f' %(label, score))
# Allows for localized training
def do_training(results,last_results,top_k):
    """Compares current model results to previous results and returns
    true if at least one label difference is detected. Used to collect
    images for training a custom model."""
    new_labels = [label[0] for label in results]
    old_labels = [label[0] for label in last_results]
    shared_labels  = set(new_labels).intersection(old_labels)
    if len(shared_labels) < top_k:
      print('Difference detected')
      return True
# Function to pull the labels from a path string
def load_labels(path):
  """Loads the labels file. Supports files with or without index numbers."""
  with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    labels = {}
    for row_number, content in enumerate(lines):
      pair = re.split(r'[:\s]+', content.strip(), maxsplit=1)
      if len(pair) == 2 and pair[0].strip().isdigit():
        labels[int(pair[0])] = pair[1].strip()
      else:
        labels[row_number] = pair[0].strip()
  return labels

def set_input_tensor(interpreter, image):
  """Sets the input tensor."""
  print('Interpreter:', interpreter)
  tensor_index = interpreter.get_input_details()[0]['index']
  input_tensor = interpreter.tensor(tensor_index)()[0]
  input_tensor[:, :] = image

def get_output_tensor(interpreter, index):
  """Returns the output tensor at the given index."""
  output_details = interpreter.get_output_details()[index]
  tensor = np.squeeze(interpreter.get_tensor(output_details['index']))
  return tensor
# Will's Initial keras Model function
def tf_image_detector():
    print('Add more code for kera implemenation')
    model             = tf.keras.models.load_model(model_file)
    config            = model.get_config()
    weights           = model.get_weights()
    test_image_batch  = data_point
    test_image_batch  = test_image_batch.reshape(1, 224, 224, 3)
    result_class      = model.predict_classes(test_image_batch, batch_size=1)
    result_confidence = model.predict(test_image_batch, batch_size=1)
    return (result_class, result_confidence)

def tflite_image_detector(interpreter, image, threshold):
  """Returns a list of detection results, each a dictionary of object info."""
  set_input_tensor(interpreter, image)
  interpreter.invoke()

  # Get all output details
  boxes = get_output_tensor(interpreter, 0)
  classes = get_output_tensor(interpreter, 1)
  scores = get_output_tensor(interpreter, 2)
  count = int(get_output_tensor(interpreter, 3))

  results = []
  for i in range(count):
    if scores[i] >= threshold:
      result = {
          'bounding_box': boxes[i],
          'class_id': classes[i],
          'score': scores[i]
      }
      results.append(result)
  return results


directory = os.fsencode(data_directory)
animal_detected = 0             # Initialize Animal Detector Counter (Confidence)
detected_last_frame = False     # Initialize Detection Status
bounding_boxes = []             #
false_positive = 0              # Initialize False Positive Counter
false_positive_threshold = 5    # How many frames to check before giving up
labels = 'models/tflite/spermwhale/spermwhale_edge_v0_1.txt'
model = 'models/tflite/spermwhale/spermwhale_edge_v0_1.tflite'
single =1
print("Labels File:",labels)
labels = load_labels(labels)
print("Model File:",model)
interpreter = Interpreter(model)
print("interpreter variable:",interpreter)
interpreter.allocate_tensors()
_, input_height, input_width, _ = interpreter.get_input_details()[0]['shape']
print('Image Input Size... Height', input_height,'Width:',input_width)
print('Loaded CNN Parameters')


image_path = 'data/deer_train/Deer_Train1309.jpg'
image = Image.open(image_path).convert('RGB').resize(
    (input_height, input_width), Image.ANTIALIAS)
results = tflite_image_detector(interpreter, image, 0.6)
