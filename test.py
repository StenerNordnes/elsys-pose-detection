from picamera2 import Picamera2
import time
import cv2
from firebase_updating import playAudio

picam2 = Picamera2()

config = picam2.create_still_configuration()
picam2.configure(config)
picam2.start()


img = picam2.capture_array()


cv2.imwrite('frame.jpg', img)

playAudio('SIqui9NaXKfDspXwnfvZVWb5Nz32')


# import libcamera

