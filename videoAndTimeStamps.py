#https://projects.raspberrypi.org/en/projects/parent-detector/7
#thise code will take a video when motion is sensed by PIR
filename= "Video"
while True:
  pir.wait_for_motion()
  camera.start_recording(filename)
  pir.wait_for_no_motion()
  camera.stop_recording()
  
  
  #this code will make the filename the time stamp
  from datetime import datetime
  filename="{0:%Y}-{0:%m}-{0:%d}".format(now)
