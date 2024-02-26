from picamera2 import Picamera2
import time
import tensorflow as tf
from predict_label import predictImage
import cv2
from firebase_updating import update_score, pasientMap, fetch_current_user

picam2 = Picamera2()

config = picam2.create_still_configuration()
picam2.configure(config)
picam2.start()

name = ''
poseConsecutive = 0

current_userID = fetch_current_user()

while True:
    img = picam2.capture_array()
    tensor = tf.convert_to_tensor(img)
    (newName, 
     conf 
     ,frame
     ) = predictImage(tensor)
    
    if newName == name and conf >= 0.99:
        poseConsecutive += 1
    else:
        poseConsecutive = 0

    if poseConsecutive == 10:
        print(f'Pose {newName} detected for 15 consecutive frames')
        print(f'Updating score for {pasientMap[newName]}')
        update_score(pasientMap[newName], 1)

    cv2.imwrite('frame.jpg', frame)
    name = newName
    print(newName, conf)
    print('Consecutive count: ', poseConsecutive)
    # time.sleep(5)

