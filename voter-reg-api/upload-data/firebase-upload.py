import csv
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate("../secrets/firebase_config.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

csv_file = "../../data-processing/wake_upload.csv"

# Create a batch object
batch = db.batch()

with open(csv_file, newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        voter_reg_num = row["voter_reg_num"]
        doc_ref = db.collection("registeredvoters").document(voter_reg_num)
        doc = doc_ref.get()

        if not doc.exists:
            voter_data = {
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "street_address": row["res_street_address"],
                "city": row["res_city_desc"],
                "birth_year": int(row["birth_year"]),
                "gender": row["gender_code"],
                "race": row["race_code"],
                "ethnicity": row["ethnic_code"],
                "party": row["party_cd"],
            }
            # Add the set operation to the batch
            batch.set(doc_ref, voter_data)

# Commit the batch write
batch.commit()

print("Data uploaded successfully!")