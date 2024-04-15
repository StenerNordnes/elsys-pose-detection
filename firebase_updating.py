from firebase_admin import credentials, initialize_app, storage
from firebase_admin import credentials
from firebase_admin import firestore
import time

# Initialiserer Firebase med nødvendige legitimasjonsopplysninger og lagringsbøtte
cred = credentials.Certificate('posemein-76815-e7599e66472b.json')
initialize_app(cred, {'storageBucket': 'posemein-76815.appspot.com'})

# Definerer navnet på filen som skal lastes ned fra lagringsbøtten
destination_file_name = r"output.mp3"

# Initialiserer en referanse til lagringsbøtten
bucket = storage.bucket()

# Initialiserer en Firestore klient
db = firestore.client()

import pygame
import time
from mutagen.mp3 import MP3

def playAudio(user_id):
    # Initialiserer Pygame mixer for lydavspilling
    pygame.mixer.init()

    try:
        # Henter brukerobjektet fra Firestore
        user_object = db.collection('brukere').document(user_id).get()

        # Sjekker om brukeren har en tilpasset melodi, hvis ja, bruker den, ellers bruker den standardmusikken
        if user_object.to_dict()['melodi'] != '':
            filename = user_object.to_dict()['melodi']
            filename = 'Mussa/' + filename 
        else:
            music_name = user_object.to_dict()['musikk']
            filename = db.collection('Musikk').document(music_name).get().to_dict()['filnavn']
            filename = 'Mussa/' + filename
                        
        # Henter filen fra lagringsbøtten
        blob = bucket.blob(filename)
        blob.download_to_filename(destination_file_name)

        # Henter lengden på lydfilen for å kunne vente til den er ferdig med å spille
        audio = MP3(destination_file_name)
        print(audio.info.length)

        # Laster lydfilen inn i Pygame mixer og spiller den av
        sound = pygame.mixer.music.load(destination_file_name)  
        pygame.mixer.music.play()

        # Venter til lydfilen er ferdig med å spille
        time.sleep(audio.info.length)
        # Stopper musikken etter at den er ferdig med å spille
        pygame.mixer.music.stop()

        # Avslutter Pygame
        pygame.quit()

    # Håndterer eventuelle unntak som kan oppstå under avspilling av lyd
    except Exception as e:
        print(e)
        print('No music found for user')

        # Avslutter Pygame selv om det oppstår en feil
        pygame.quit()
        # Avslutter funksjonen tidlig hvis det oppstår en feil
        return


# Åpner 'pose_labels.txt' filen og leser etikettene inn i en liste, lager også en ordbok som kartlegger etikettene til pasient-IDer
with open('pose_labels.txt', 'r') as  f:
    labels = [label.strip() for label in f.readlines()]
    pasientMap = {label: f'pasient{i+1}' for i, label in enumerate(labels)}

# Funksjon for å oppdatere poengsummen til en bruker basert på posen de laget
def update_score(user_id, pose):
    try:
        # Henter dokumentet for den gitte posen fra 'Poseringer' samlingen i Firestore
        pose_ref = db.collection('Poseringer').document(pose)
        pose_points = pose_ref.get().to_dict()['Poeng']

        # Henter brukerdokumentet og oppdaterer poengsummen og innsjekkstidspunktet
        doc_ref = db.collection('brukere').document(user_id)
        doc_ref.update({
            'score': firestore.Increment(pose_points),
            'innsjekkTidspunkt': firestore.SERVER_TIMESTAMP,
        })
        print(f'Oppdatert poengsum for {user_id} med {pose_points} poeng')

        # Logger ut brukeren ved å sette 'userID' feltet i 'current_user' dokumentet til en tom streng
        logged_in_ref = db.collection('data').document('current_user')
        logged_in_ref.update({
            'userID': '',
        })
        print('Logget ut bruker')
    except Exception as e:
        print(e)
        return

# Funksjon for å hente ID-en til den nåværende brukeren
def fetch_current_user() -> str:
    try:
        # Henter 'current_user' dokumentet fra 'data' samlingen i Firestore
        doc_ref = db.collection('data').document('current_user')
        doc = doc_ref.get()
        
        userID = doc.to_dict()['userID']
        if userID == '':
            print('Ingen bruker er logget inn. Returnerer tom streng')

        return userID
    except Exception as e:
        print(e)
        return None

def fetch_user_pose(user_id) -> str:
    '''Funksjon for å hente posen til den nåværende brukeren'''
    if user_id == '':
        print('Ingen bruker er logget inn')
        return None

    try:
        # Henter brukerdokumentet og returnerer posen
        doc_ref = db.collection('brukere').document(user_id)
        doc = doc_ref.get()
        return doc.to_dict()['posering'].lower()
    except Exception as e:
        print(e)
        return None

# Hovedprogrammet starter her hvis denne filen kjøres som et skript
if __name__ == '__main__':
    pygame.init()
    audio = MP3('output.mp3')
    print(audio.info.length)
    sound = pygame.mixer.music.load('output.mp3')  
    pygame.mixer.music.play()
    time.sleep(audio.info.length)
    pygame.mixer.music.stop()
    pygame.quit()