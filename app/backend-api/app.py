from fastapi import FastAPI, HTTPException
import firebase_admin
from firebase_admin import credentials
from google.cloud import firestore as gcloud_firestore
from models import google_credentials

# Initialize Firebase
cred = credentials.Certificate(google_credentials)
firebase_admin.initialize_app(cred)
db = gcloud_firestore.Client()  # Firestore database reference

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


# endpoint to get voter_reg_num
@app.get("/get-voter-reg-num")
async def get_voter_reg_num(
    first_name: str = None, last_name: str = None, birth_year: int = None
):
    # retrieve firestore data
    voters_ref = db.collection("registeredVoters")
    query = voters_ref

    if first_name:
        query = query.where("first_name", "==", first_name)
    if last_name:
        query = query.where("last_name", "==", last_name)
    if birth_year:
        query = query.where("birth_year", "==", birth_year)

    results = query.stream()

    # make a list of voter data from query results
    voter_list = [{"voter_reg_num": doc.id, **doc.to_dict()} for doc in results]

    # raise 404 if no voters match the query
    if not voter_list:
        raise HTTPException(status_code=404, detail="Voter not found")

    # extract voter_reg_num from voter data
    voter_reg_nums = [voter["voter_reg_num"] for voter in voter_list]

    return {"voter_reg_nums": voter_reg_nums}
