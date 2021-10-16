import logging
from firebase_admin import credentials, db
import firebase_admin
import os

def store(db_ref, img_hash, description):    
    db_ref.child("hash_table").child(img_hash).set({"hash": img_hash, "description": description})

def get_db_reference():
    key = os.path.isfile('databaseKey.json') 
    if not key:
        logging.warning('No database key found, not attempting to connect')
        return None

    cred = credentials.Certificate('databaseKey.json')
    #this is my db, we should get a shared one in the future
    firebase_admin.initialize_app(cred, {'databaseURL':'https://meme-hash-default-rtdb.europe-west1.firebasedatabase.app/'})

    ref = db.reference('/')

    return ref