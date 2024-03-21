import time
import tensorflow as tf
import cv2
from firebase_updating import update_score, pasientMap, fetch_current_user, playAudio, fetch_user_pose
from predict_label import predictImage
from picamera2 import Picamera2
import RPi.GPIO as GPIO

BUTTON_PIN = 15  # replace with your button's GPIO pin number
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set up the button pin as an input


picam2 = Picamera2()
config = picam2.create_still_configuration()
picam2.configure(config)
picam2.start()


def cameraMain():
    successful_exit = False

    name = ''
    poseConsecutive = 0

    current_userID = fetch_current_user()
    pose = fetch_user_pose(current_userID)

    print(f'Current user: {current_userID}\nPose: {pose}')

    if current_userID == '' or pose is None:
        print('No user logged in')
        return


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
            successful_exit = True
            break

        # cv2.imwrite('frame.jpg', frame)
        name = newName
        print(newName, conf)
        print('Consecutive count: ', poseConsecutive)
        # time.sleep(5)
        if GPIO.input(BUTTON_PIN) == GPIO.HIGH:
            print('Button pressed, pose detection exited')
            break

    return successful_exit


if __name__ == '__main__':
    cameraMain()
