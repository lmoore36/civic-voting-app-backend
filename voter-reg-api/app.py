from fastapi import FastAPI, HTTPException, Depends
import firebase_admin
from firebase_admin import credentials, firestore, auth

# Initialize Firebase
cred = credentials.Certificate("./secrets/firebase_config.json")  # Path to your Firebase JSON
firebase_admin.initialize_app(cred)
db = firestore.client()  # Firestore database reference

app = FastAPI()


@app.get("/")
def root():
    return {"message": "FastAPI with Firebase is working!"}
