import firebase_admin
from firebase_admin import credentials, firestore
import csv
from models import google_credentials, voters_csv

if not firebase_admin._apps:
    cred = credentials.Certificate(google_credentials)
    firebase_admin.initialize_app(cred)

db = firestore.client()


def upload_csv_to_firestore():
    print(f"Processing CSV file: {voters_csv}")

    try:
        with open(voters_csv, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            processed_rows = 0

            for row in reader:
                voter_reg_num = row.get("voter_reg_num")

                if not voter_reg_num:
                    print("Skipping row without voter_reg_num.")
                    continue

                voter_data = {
                    "first_name": row.get("first_name"),
                    "last_name": row.get("last_name"),
                    "street_address": row.get("res_street_address"),
                    "city": row.get("res_city_desc"),
                    "birth_year": (
                        int(row.get("birth_year")) if row.get("birth_year") else None
                    ),
                    "gender": row.get("gender_code"),
                    "race": row.get("race_code"),
                    "ethnicity": row.get("ethnic_code"),
                    "party": row.get("party_cd"),
                }

                doc_ref = db.collection(COLLECTION_NAME).document(str(voter_reg_num))
                doc_ref.set(voter_data)

                processed_rows += 1

            print(f"Successfully uploaded {processed_rows} rows to Firestore.")

    except Exception as e:
        print(f"Error processing file {CSV_FILE}: {e}")


if __name__ == "__main__":
    upload_csv_to_firestore()
