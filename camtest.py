from picamera2 import Picamera2
import time
import tensorflow as tf
from predict_label import predictImage
import cv2
from firebase_updating import update_score, pasientMap, fetch_current_user, playAudio, fetch_user_pose

picam2 = Picamera2()

config = picam2.create_still_configuration()
picam2.configure(config)
picam2.start()

name = ''
poseConsecutive = 0

current_userID = fetch_current_user()
pose = fetch_user_pose(current_userID)

print(f'Current user: {current_userID}\nPose: {pose}')

if current_userID == '' or pose is None:
    print('No user logged in')
    exit(0)


while True:
    img = picam2.capture_array()
    tensor = tf.convert_to_tensor(img)
    (newName, 
     conf 
     ,frame
     ) = predictImage(tensor)
    
    if newName == pose and conf >= 0.99:
        poseConsecutive += 1
    else:
        poseConsecutive = 0

    if poseConsecutive == 10:
        print(f'Pose {newName} detected for 15 consecutive frames')
        print(f'Updating score for {current_userID}')
        update_score(current_userID, pose)
        playAudio(current_userID)
        break

    cv2.imwrite('frame.jpg', frame)
    name = newName
    print(newName, conf)
    print('Consecutive count: ', poseConsecutive)
    # time.sleep(5)

