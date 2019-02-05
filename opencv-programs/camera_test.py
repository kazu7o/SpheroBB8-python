from picamera import PiCamera
from time import sleep

camera = PiCamera()
camera.start_preview()

sleep(5)

camera.capture('/home/pi/codes/SpheroBB8-python/opencv-programs/test1.jpg')
camera.stop_preview()
