import time
import tensorflow as tf
import cv2
from firebase_updating import update_score, pasientMap, fetch_current_user, playAudio, fetch_user_pose  # Importerer funksjoner fra firebase_updating-modulen
from predict_label import predictImage  # Importerer funksjonen predictImage fra predict_label-modulen
from picamera2 import Picamera2  # Importerer Picamera2-klassen fra picamera2-modulen
import RPi.GPIO as GPIO

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)  # Setter GPIO-modus til BCM

BUTTON_PIN = 15  
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Setter opp pin 15 som en inngangspinne og setter initialverdien til å være trukket opp (på)

picam2 = Picamera2()  # Oppretter et nytt Picamera2-objekt
config = picam2.create_still_configuration()  # Oppretter en stillbildekonfigurasjon
picam2.configure(config)  # Konfigurerer kameraet med den opprettede konfigurasjonen
picam2.start()  # Starter kameraet

def cameraMain():  # Definerer hovedfunksjonen for kameraet
    successful_exit = False  # Initialiserer variabelen successful_exit
    poseConsecutive = 0
    failSafeConsecutive = 0
    current_userID = fetch_current_user()  # Henter ID-en til innlogget bruker
    pose = fetch_user_pose(current_userID)  # Henter poseringen
    if current_userID == '' or pose is None: 
        print('No user logged in')
        return
    while True: 
        img = picam2.capture_array()  # Tar et bilde med kameraet og lagrer det som en array
        tensor: tf.Tensor = tf.convert_to_tensor(img)  # Konverterer bildet til en tensor
        (newName, confidence, frame) = predictImage(tensor)  # Bruker predictImage-funksjonen til å forutsi posen i bildet
        if newName == pose and confidence >= 0.90: 
            poseConsecutive += 1
            failSafeConsecutive = 0
        else:  
            poseConsecutive = 0
            failSafeConsecutive += 1
        if poseConsecutive == 10:  # Etter 10 korrekte gjenkjenninger bilder, oppdater scoren til brukeren og spill av lyd
            print(f'Pose {newName} detected for 10 consecutive frames')
            print(f'Updating score for {current_userID}')
            update_score(current_userID, pose)
            playAudio(current_userID)
            successful_exit = True
            break
        if failSafeConsecutive == 30:  # Etter 30 mislykkede gjenkjenninger, avslutt programmet
            print('Pose not detected for 30 consecutive frames')
            break
    return successful_exit  # Returnerer verdien av successful_exit

if __name__ == '__main__':
    cameraMain()  # Kjører hovedfunksjonen for kameraet hvis dette skriptet kjøres som hovedprogrammet