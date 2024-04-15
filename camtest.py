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

    name = ''
    poseConsecutive = 0
    failSafeConsecutive = 0

    current_userID = fetch_current_user()  # Henter ID-en til den nåværende brukeren
    pose = fetch_user_pose(current_userID)  # Henter posen til den nåværende brukeren

    print(f'Current user: {current_userID}\nPose: {pose}')  # Skriver ut ID-en og posen til den nåværende brukeren

    if current_userID == '' or pose is None:  # Hvis det ikke er noen nåværende bruker eller posen er None, avslutt funksjonen
        print('No user logged in')
        return

    while True:  # Starter en uendelig løkke

        img = picam2.capture_array()  # Tar et bilde med kameraet og lagrer det som en array
        tensor: tf.Tensor = tf.convert_to_tensor(img)  # Konverterer bildet til en tensor
        (newName, conf, frame) = predictImage(tensor)  # Bruker predictImage-funksjonen til å forutsi posen i bildet
        
        if newName == pose and conf >= 0.90:  # Hvis den forutsagte posen er lik den ønskede posen og konfidensen er større enn eller lik 0.99, øk poseConsecutive og nullstill failSafeConsecutive
            poseConsecutive += 1
            failSafeConsecutive = 0
            
        else:  # Hvis den forutsagte posen ikke er lik den ønskede posen, nullstill poseConsecutive og øk failSafeConsecutive
            poseConsecutive = 0
            failSafeConsecutive += 1

        if poseConsecutive == 10:  # Hvis den ønskede posen har blitt forutsagt i 10 påfølgende bilder, oppdater scoren til brukeren og spill av lyd
            print(f'Pose {newName} detected for 15 consecutive frames')
            print(f'Updating score for {current_userID}')
            update_score(current_userID, pose)
            # playAudio(current_userID)
            successful_exit = True
            break

        if failSafeConsecutive == 30:  # Hvis den ønskede posen ikke har blitt forutsagt i 30 påfølgende bilder, avslutt løkken
            print('Pose not detected for 30 consecutive frames')
            break

        name = newName
        print(newName, conf)
        print('Consecutive count: ', poseConsecutive)

    return successful_exit  # Returnerer verdien av successful_exit

if __name__ == '__main__':
    cameraMain()  # Kjører hovedfunksjonen for kameraet hvis dette skriptet kjøres som hovedprogrammet