
import glob










def main(args=None):
    parser = _make_argument_parser()
    args = parser.parse_args(args)

    sys_mode = args.sys_mode

    if model_format == keras :
        model=tf.keras.models.load_model(model_file)
        config=model.get_config()
        weights=model.get_weights()
        image_path='/home/pi/cameratrap/data/deer_train/Deer_Test0.jpg'

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

    if model_format == xnor
        # Load model
        model = xnornet.Model.load_built_in()
        print("Model: {}".format(model.name))
        print("  version {!r}".format(model.version))
        animal_detected = 0             # Initialize Animal Detector Counter (Confidence)
        detected_last_frame = False     # Initialize Detection Status
        bounding_boxes = []             #
        false_positive = 0              # Initialize False Positive Counter
        false_positive_threshold = 5    # How many frames to check before giving up
            # take images from the directory of saved images
            if primary_confidence == 0 or sys_mode == test:
                data_point = 
                model_input = xnornet.Input.rgb_image(input_res[0:2], data_point)
            # take images directly from the camera buffer
            if primary_confidence != 0 :
                # Get the frame from the CircularIO buffer.
                cam_buffer = stream.getvalue()
                # The camera has not written anything to the CircularIO yet, thus no frame is been captured
                if len(cam_buffer) != SINGLE_FRAME_SIZE_RGB:
                    continue
                # Passing corresponding RGB
                model_input = xnornet.Input.rgb_image(input_res[0:2], cam_buffer)
            # Evaluate
            results = model.evaluate(model_input)
            # Check frame model results
            for result in results:
                model_class = result.class_label.label
                local_animal_detected = False
                local_animal_detected = result.class_label.label == model_class




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
            if animal_detected >= args.detection_confidence:
                # Classification model
                if len(bounding_boxes) == 0:
                    print("Animal detected!")
                else:  # Detection model
                    print("{} animal detected!".format(len(bounding_boxes)))
                image = _convert_to_pillow_img(cam_buffer, input_res)
                if not (args.no_draw_bounding_box) and len(bounding_boxes) != 0:
                    image = _draw_bounding_box(image, bounding_boxes, input_res,
                                               args.bounding_box_color)
                _save_image_to_disk(image, args.output_filename)
            else:
                print("Checking...")
                false_positive += 1

print("Cleaning up...")
camera.stop_recording()
camera.close()
print("")
