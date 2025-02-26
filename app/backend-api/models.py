from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv
import os

load_dotenv()
google_credentials = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
voters_csv = os.getenv("VOTERS_CSV_FILE")


class ValidVoter(BaseModel):
    voter_reg_num: int
    last_name: str
    first_name: str
    res_street_address: str
    race_code: str
    ethnic_code: str
    party_cd: str
    gender_code: str
    birth_year: int
    res_city_desc: str


class UserAccount(BaseModel):
    voter_reg_num: int
    email: str
    password_hash: str


class VoteData(BaseModel):
    voter_reg_num: int
    issue_1: str
    issue_2: str
    issue_other: Optional[str] = None
    write_in: Optional[str] = None
