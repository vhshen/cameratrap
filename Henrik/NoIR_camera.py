# first script to test the NoIR picam's capture() method

from time import sleep
from picamera import PiCamera
camera = PiCamera()
camera.resolution = (1024, 768)
camera.start_preview()

# iso
# Higher for lower light. 800 and above and it starts to get noisy
# 0 for auto
camera.iso = 400 

# shutter_speed 
# 0 for auto            
# shutter speed range is any multiple of 18.9 microseconds
#camera.shutter_speed = 33333 # microseconds
print (camera.shutter_speed)

# trigger speed (? can you affect that here?)

# Flash timing
# Options: off, auto, on, redeyem fillin, torch
#camera.FLASH_MODES = off # no LEDs hooked up yet, uncomment when ready

# Exposure; range betwen -25 -> 25. Larger values = brighter images
camera.exposure_compensation = 0 # default is 0

# Exposure mode
# Options: off, auto, night, nightpreview, backlight, spotlight, sports, snow, beach,
#          verylong, fixedfps, antishake, fireworks
camera.exposure_mode = 'auto' # default is auto

# led (through GPIO, could this be how you sync it?)

# Automatic white balance mode
# Options: off, auto, sunlight, cloudy, shade, tungsten, flourescent, incandescent, flash, horizon
camera.awb_mode = 'auto' # default is auto

 
# Other settings include brightness (0 -> 100), contrast (-100 -> 100), image_effect, 
# saturation (-100 -> 100) 

camera.brightness = 50 #normal

# camera warm-up time and image capture
sleep(4) #shows preview window for X seconds before taking a picture
camera.capture( 'image.jpg' )

# need to close camera at end? camera.close()

# _get_camera_settings()  -> will this give accurate camera settings?
