from fastapi import HTTPException
import firebase_admin
from firebase_admin import credentials
from google.cloud import firestore as gcloud_firestore

# Initialize Firebase
cred = credentials.Certificate(
    "./secrets/firebase_config.json"
)  # Path to your Firebase JSON
firebase_admin.initialize_app(cred)
db = gcloud_firestore.Client()  # Firestore database reference


def get_voter_num(
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
