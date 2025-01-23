import os
import psycopg2
from dotenv import load_dotenv
from flask_cors import CORS
from flask import Flask, jsonify, request

# SQL queries
CREATE_VOTERS_TABLE = ("CREATE TABLE IF NOT EXISTS registered_users (id SERIAL PRIMARY KEY, name TEXT NOT NULL, address TEXT NOT NULL, county TEXT NOT NULL);")
INSERT_VOTER_RETURN_ID = "INSERT INTO registered_users (name, address, county) VALUES (%s, %s, %s) RETURNING id;"

# loads variables from .env file into environment
load_dotenv() 

# creates a new Flask app
app = Flask(__name__)

# enables CORS
CORS(app)

# gets variables from .env file
url = os.getenv('DATABASE_URL')

# creates a connection to the database
connection = psycopg2.connect(url)

# ensure voters table exists
with connection:
    with connection.cursor() as cursor:
        cursor.execute(CREATE_VOTERS_TABLE)
        connection.commit()

## ENDPOINTS ##

# GET all voters
@app.get("/api/voters")
def get_voters():
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, name, address, county FROM registered_users")
        voters = cursor.fetchall()
        return jsonify(voters), 200

# CREATE a new voter
@app.post("/api/new_voter")
def create_voter():
    # get data from request
    data = request.get_json()
    name = data["name"]
    address = data["address"]
    county = data["county"]

    # insert data into database
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_VOTER_RETURN_ID, (name, address, county))
            voter_id = cursor.fetchone()[0]
    
    # return voter id on success
    return {"id": voter_id, "message": f"Voter {name} from {county} created."}, 201

if __name__ == "__main__":
    app.run(debug=True)