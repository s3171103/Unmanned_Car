import time
from io import BytesIO
from picamera import PiCamera
camera = PiCamera()
my_stream = BytesIO()
camera.resolution=(2592,1944)
camera.start_preview()
time.sleep(2)
camera.capture(my_stream,'jpeg')
time.sleep(5)
camera.stop_preview()
