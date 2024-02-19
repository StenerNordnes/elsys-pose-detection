import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account
cred = credentials.Certificate('posemein-76815-e7599e66472b.json')
firebase_admin.initialize_app(cred)

db = firestore.client()


with open('pose_labels.txt', 'r') as  f:
    labels = [label.strip() for label in f.readlines()]
    pasientMap = {label: f'pasient{i+1}' for i, label in enumerate(labels)}



def update_score(user_id,new_score):
    doc_ref = db.collection('Pasienter').document(user_id)
    doc_ref.update({
        'Score': firestore.Increment(new_score)
    })





