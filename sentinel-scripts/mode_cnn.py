import argparse
import time
import numpy as np
import os
from annotation import Annotator
from tflite_runtime.interpreter import Interpreter
from PIL import Image
import re


#Saves camera frame and model inference results to user-defined storage directory
def save_data(image,results,path,ext='jpg'):
    name = '%simg-%s.%s' %(path,tag,ext)
    image.save(name)
    print('Frame saved as: %s' %name)
    logging.info('Image: %s Results: %s', results)
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
# Annotate the identified objects
def live_annotate_objects(annotator, results, labels):
  """Draws the bounding box and label for each object in the results."""
  for obj in results:
    # Convert the bounding box figures from relative coordinates
    # to absolute coordinates based on the original resolution
    ymin, xmin, ymax, xmax = obj['bounding_box']
    xmin = int(xmin * CAMERA_WIDTH)
    xmax = int(xmax * CAMERA_WIDTH)
    ymin = int(ymin * CAMERA_HEIGHT)
    ymax = int(ymax * CAMERA_HEIGHT)

    # Overlay the box, label, and score on the camera preview
    annotator.bounding_box([xmin, ymin, xmax, ymax])
    annotator.text([xmin, ymin],
                   '%s\n%.2f' % (labels[obj['class_id']], obj['score']))
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
  #print('Interpreter:', interpreter)
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
    print('Add more code for keras implemenation')
    model             = tf.keras.models.load_model(model_file)
    config            = model.get_config()
    weights           = model.get_weights()
    test_image_batch  = data_point
    test_image_batch  = test_image_batch.reshape(1, 224, 224, 3)
    result_class      = model.predict_classes(test_image_batch, batch_size=1)
    result_confidence = model.predict(test_image_batch, batch_size=1)
    return (result_class, result_confidence)
# Adds image file to allow it to be run (Will's Code, may be depreciated)
def imageAdder(path_in):
  path      = path_in
  image     = cv2.imread(path)
  image2    = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
  img       = cv2.resize(image, (224,224))
  return img

def tflite_im(interpreter, input_width, input_height, file_path, threshold):
    """Returns a list of detection results, each a dictionary of object info."""
    file = Image.open(file_path).convert('RGB').resize(
      (input_height, input_width), Image.ANTIALIAS)
    tic = time.process_time()
    set_input_tensor(interpreter, file)
    interpreter.invoke()

    # Get all output details
    boxes = get_output_tensor(interpreter, 0)
    classes = get_output_tensor(interpreter, 1)
    scores = get_output_tensor(interpreter, 2)
    count = int(get_output_tensor(interpreter, 3))

    results = []
    toc = time.process_time()
    clock = toc - tic
    for i in range(count):
        if scores[i] >= threshold:
          result = {
              'file': file_path,
              'bounding_box': boxes[i],
              'class_id': classes[i],
              'score': scores[i],
              'time': clock
          }
          results.append(result)
    return results

# Defines the inputs to the script
def user_selections():
    parser = argparse.ArgumentParser()
    parser.add_argument('--sys_mode', required=True,
                        help='Test or Real')
    parser.add_argument('--mcu', required=False, default='rpi0',
                        help='Type of Microcontroller')
    parser.add_argument('--vpu', required=False, default='rpi0',
                        help='Type of AI Processor')
    parser.add_argument('--model_format', required=True,
                        help='What format is the model in?')
    parser.add_argument('--model_type', required=True,
                        help='Image, Video, Acoustics, Motion')
    parser.add_argument('--model_file', required=True,
                        help='Specify the model file')
    parser.add_argument('--data_directory', required=True,
                        help='Where are the files being accessed')
    parser.add_argument('--results_directory', required=True,
                        help='Where are the files being saved')
    #parser.add_argument('--do_training', required=False, default = False,
    #                    help='Save relevant files for training custom model')
    parser.add_argument('--current_background', required=False, default='',
                        help='Last Recorded Background ')
    args = parser.parse_args()
    return args

# The main function script
def cnn(sys_mode, mcu, vpu, model_format, type, resolution, \
    model, labels, data_directory, results_directory, \
    current_background, ai_sensitivity):
    directory = os.fsencode(data_directory)
    animal_detected = 0             # Initialize Animal Detector Counter (Confidence)
    detected_last_frame = False     # Initialize Detection Status
    bounding_boxes = []             #
    false_positive = 0              # Initialize False Positive Counter
    false_positive_threshold = 5    # How many frames to check before giving up
    image_burst = 10
    result_array = []
    files_checked = 0
    max_files = 15
    print('Files being checked:', max_files)
    #print("Labels File:",labels)
    labels = load_labels(labels)
    #print("Model File:",model)
    interpreter = Interpreter(model)
    #print("interpreter variable:",interpreter)
    interpreter.allocate_tensors()
    _, input_height, input_width, _ = interpreter.get_input_details()[0]['shape']
    #print('Image Input Size... Height', input_height,'Width:',input_width)
    #print('Loaded CNN Parameters')

    if vpu == 'coral_acc' :
        print('Add more code for the coral accelerator')

    if type == 'image' or 'acoustic':
        if sys_mode == 'real' :
            if mcu != rpi0 :
                sys.exit('Not ready for this part yet!')
            # take images directly from the camera buffer
            if confidence != 0 :
                # Reconstruct the input resolution to include color channel
                input_res = (resolution[0], resolution[1], 3)
                SINGLE_FRAME_SIZE_RGB = input_res[0] * input_res[1] * input_res[2]

                # Initialize the camera, set the resolution and framerate
                try:
                    camera = picamera.PiCamera()
                except picamera.exc.PiCameraMMALError:
                    print("\nPiCamera failed to open, do you have another task using it "
                          "in the background? Is your camera connected correctly?\n")
                    sys.exit("Connect your camera and kill other tasks using it to run "
                             "this sample.")

                # Initialize the buffer for picamera to hold the frame
                # https://picamera.readthedocs.io/en/release-1.13/api_streams.html?highlight=PiCameraCircularIO
                stream = picamera.PiCameraCircularIO(camera, size=SINGLE_FRAME_SIZE_RGB)
                # All essential camera settings
                camera.resolution = input_res[0:2]
                camera.framerate = args.camera_frame_rate
                camera.brightness = args.camera_brightness
                camera.shutter_speed = args.camera_shutter_speed
                camera.video_stabilization = args.camera_video_stablization

                # Get the frame from the CircularIO buffer.
                image = stream.getvalue()
                # The camera has not written anything to the CircularIO yet, thus no frame is been captured
                #if len(cam_buffer) != SINGLE_FRAME_SIZE_RGB:
                #    continue
                # Passing corresponding RGB
                results = tflite_im(interpreter, image, ai_sensitivity)
                print(results)
                # If we already detected animal in this frame, we don't want to over count.
                if local_animal_detected and not detected_this_frame:
                    if animal_detected < args.detection_confidence:
                        # If we haven't confirmed, then increase our confidence.
                        if detected_last_frame:
                            animal_detected += 1
                        # If we didn't confirm last frame but we detected in this frame, we want to reset our confidence.
                        else:
                            animal_detected = 1
                # We detected an animal in this frame
                if local_animal_detected:
                    detected_this_frame = True
                    # Update the history
                    detected_last_frame = detected_this_frame
                    # Draw Bounding Box
                    bounding_boxes.append(result.rectangle)
                else:
                    print("Checking...")
                    false_positive += 1
                    save_data()
                if false_positive_threshold >= false_positive :
                    print("Cleaning up...")
                    camera.stop_recording()
                    camera.close()
            # take images from the initial burst triggered in mode_sentinel.py
            if confidence == 0 :
                for file in os.listdir(data_directory):
                    filename = os.fsdecode(file)
                    if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".jpeg"):
                        current_image = os.path.join(data_directory,file)
                        print('Current Image:', current_image)
                        results = tflite_im(interpreter, input_width, input_height, current_image, ai_sensitivity)
                    else:
                        print("All Burst Files Checked")
                        break
        # Test Scenario (running algorithm on files presaved to data_directory)
        if sys_mode == 'test' :
            print('Test Script Initialized...')
            for file in os.listdir(data_directory):
                if max_files < files_checked :
                    print('Checked all files')
                    break
                filename = os.fsdecode(file)
                if filename.endswith(".jpg") :
                    result = filename
                    current_image = os.path.join(data_directory,file)
                    #print('Current Image:', current_image)
                    result = tflite_im(interpreter, input_width, input_height, current_image, ai_sensitivity)

                    #print(result)
                    #result_row = result.append(result)
                    #print('Input to CNN:',image)
                else:
                    print("All files Checked")
                    break
                result_array = np.append(result_array, result)
                #print(result_array)
                files_checked += 1
        # take images from the directory of saved images
    if type == 'video' :
        print('Code for Video Recognition not Completed')
    return result_array


if __name__ == "__main__":
    main()
