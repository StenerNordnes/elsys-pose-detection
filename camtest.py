from picamera2 import Picamera2
import time
import tensorflow as tf
from predict_label import predictImage
import cv2
from firebase_updating import update_score, pasientMap

picam2 = Picamera2()

config = picam2.create_still_configuration()
picam2.configure(config)
picam2.start()

name = ''
poseConsecutive = 0

while True:
    img = picam2.capture_array()
    tensor = tf.convert_to_tensor(img)
    newName, conf, frame = predictImage(tensor)

    if conf > 0.999:
        name = newName
        poseConsecutive += 1
    else:
        name = ''
        poseConsecutive = 0

    if poseConsecutive > 10:
        update_score(pasientMap[name], 10)
        poseConsecutive = 0
        


    cv2.imwrite("frame.jpg", frame)
    print(newName, conf)
    time.sleep(5)

