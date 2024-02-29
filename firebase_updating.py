from firebase_admin import credentials, initialize_app, storage
from firebase_admin import credentials
from firebase_admin import firestore
import time


# cred = credentials.Certificate(r"credential_location.JSON")
# initialize_app(cred, {'storageBucket': 'xxxxxxxx.appspot.com'})
# Use a service account
cred = credentials.Certificate('posemein-76815-e7599e66472b.json')
initialize_app(cred, {'storageBucket': 'posemein-76815.appspot.com'})

# bucket_name = "gs://posemein-76815.appspot.com"

#The path to which the file should be downloaded
destination_file_name = r"output.mp3"
bucket = storage.bucket()


db = firestore.client()

import pygame
import time
from mutagen.mp3 import MP3

pygame.init()

def playAudio(user_id):
    try:
        user_object = db.collection('brukere').document(user_id).get()
        music_name = user_object.to_dict()['musikk']
        filename = db.collection('Musikk').document(music_name).get().to_dict()['filnavn']
        blob = bucket.blob(filename)
        blob.download_to_filename(destination_file_name)
        audio = MP3(destination_file_name)
        print(audio.info.length)
        sound = pygame.mixer.music.load(destination_file_name)  
        pygame.mixer.music.play()
        time.sleep(audio.info.length)
        pygame.mixer.music.stop()
        pygame.quit()
    except Exception as e:
        print(e)
        print('No music found for user')
        pygame.quit()
        return




with open('pose_labels.txt', 'r') as  f:
    labels = [label.strip() for label in f.readlines()]
    pasientMap = {label: f'pasient{i+1}' for i, label in enumerate(labels)}



def update_score(user_id,pose):
    pose_ref = db.collection('Poseringer').document(pose)
    pose_points = pose_ref.get().to_dict()['Poeng']


    doc_ref = db.collection('brukere').document(user_id)
    doc_ref.update({
        'score': firestore.Increment(pose_points)
    })
    print(f'Updated score for {user_id} with {pose_points} points')
    logged_in_ref = db.collection('data').document('current_user')
    logged_in_ref.update({
        'userID': '',
    })
    print('Logged out user')



def fetch_current_user() -> str:
    try:
        doc_ref = db.collection('data').document('current_user')
        doc = doc_ref.get()
        
        userID = doc.to_dict()['userID']
        if userID == '':
            print('No user logged in. Returning empty string')

        return userID
    except Exception as e:
        print(e)
        return None

def fetch_user_pose(user_id) -> str:
    if user_id == '':
        print('No user logged in')
        return None

    try:
        doc_ref = db.collection('brukere').document(user_id)
        doc = doc_ref.get()
        return doc.to_dict()['posering'].lower()
    except Exception as e:
        print(e)
        return None

if __name__ == '__main__':
    playAudio('7cselDAiVXMbkjPt2L0TuA0KsSp1')
    update_score('7cselDAiVXMbkjPt2L0TuA0KsSp1', 'bicep')