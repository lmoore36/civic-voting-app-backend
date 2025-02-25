from fastapi import FastAPI, HTTPException, Depends
import firebase_admin
from firebase_admin import credentials, firestore, auth

# Initialize Firebase
cred = credentials.Certificate("./secrets/firebase_config.json")  # Path to your Firebase JSON
firebase_admin.initialize_app(cred)
db = firestore.client()  # Firestore database reference

app = FastAPI(
    title="Civic Voting App API",
    contact={
        "name": "Civic Voting Project",
        "url": "https://github.com/appteamcarolina/civic-voting-backend.git",
    },
        description="""
## Introduction

API for App Team Carolina's Civic Voting Project. This API is used to validate registered voters, sign up new users, record votes, and get voting results.
""",
    openapi_tags=[
        {"name": "Validate", "description": "Check if a user is a registered voter"},
        {"name": "Sign Up", "description": "Create a new user account"},
        {"name": "Vote", "description": "Record a user's vote"},
        {"name": "Results", "description": "Get civic voting results"},
    ],
)



@app.get("/")
def root():
    return {"message": "FastAPI with Firebase is working!"}
