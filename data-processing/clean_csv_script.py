import pandas as pd

input_file = './wake_county/wake_voters.csv'
output_file = 'wake_upload.csv'

columns_to_keep = [
    "voter_reg_num", 
    "last_name", 
    "first_name", 
    "res_street_address",
    "race_code",
    "ethnic_code",
    "party_cd",
    "gender_code",
    "birth_year",
    "res_city_desc"
]

# read the csv
df = pd.read_csv(input_file, low_memory=False)

# filter rows where city is APEX
filtered_df = df[df['res_city_desc'].str.strip().str.upper() == 'APEX']

# remove all columns not in the keep list
df = filtered_df[columns_to_keep]

# # extract the house numner and make it into a new column
# df['house_number'] = df['res_street_address'].str.extract(r'^\s*(\d+)', expand=False)

# save cleaned data to a new file
df.to_csv(output_file, index=False)