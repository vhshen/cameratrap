#https://projects.raspberrypi.org/en/projects/parent-detector/6

#this code will take a picture from the camera and save it
from picamera import PiCamera
camera=PiCamera()
camera.capture('home/pi/pic.png')
camera.close()

##this code will run a preview from the camera lens while motion is detected by the PIR sensor
while True:
  pir.wait_for_motion()
  print("Motion detected!")
  camera.start_preview()
  pir.wait_for_no_motion()
  camera.stop_preview()
  
