import requests
import json
# from includes.common_functions import get_config
from datetime import datetime
import os
import pandas as pd

# config = get_config()
TODAY = datetime.now().strftime("%d-%m-%Y")
OUTPUT_FOLDER = "../../data/raw_data/injested_data/"
COURT_DATA_CSV = "../../data/raw_data/courts_data/hudle_court_data.csv"

def get_data_from_api(hudle_venue_id, hudle_court_id, venue_id, court_id):
    url = f"https://api.hudle.in/api/v1/venues/{hudle_venue_id}/facilities/{hudle_court_id}/slots"
    params = {
        "start_date": "2025-03-26",
        "end_date": "2025-03-27",
        "grid": 1
    }
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        "api-secret": "hudle-api1798@prod",
        "Connection": "keep-alive",
        "Host": "api.hudle.in",
        "Origin": "https://hudle.in",
        "Referer": "https://hudle.in/",
        "Sec-CH-UA": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
        "Sec-CH-UA-Mobile": "?0",
        "Sec-CH-UA-Platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        "x-app-id": "250100646453736134000537361200192024"
    }

    # Start a session to maintain cookies
    session = requests.Session()
    session.get("https://hudle.in/", headers=headers)
    
    response = session.get(url, params=params, headers=headers)
    
    if response.status_code == 200:
        print("✅ API Request Successful!")
        write_data_to_json(venue_id, court_id, response.json()) 
    else:
        print(f"❌ API Request Failed! Status Code: {response.status_code}")
        print(f"Error on the venue = {venue_id}, court = {court_id}")

def write_data_to_json(venue_id, court_id, json_data):
    file_path = f"{OUTPUT_FOLDER}/{venue_id}/{TODAY}"
    file_name = f"{file_path}/{court_id}.json"
    
    # Ensure the required folder exists
    os.makedirs(file_path, exist_ok=True)
    
    try:
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=4)
            print(f"Data written to {file_name}")
    except Exception as e:
        print(f"Error writing JSON file: {e}")

if __name__ == "__main__":
    # Read court data from CSV
    try:
        court_data = pd.read_csv(COURT_DATA_CSV)
    except FileNotFoundError:
        print(f"❌ Court data CSV not found at {COURT_DATA_CSV}")
        exit(1)
        
    # Apply lambda function to court_data to call get_data_from_api
    court_data.apply(
        lambda row: get_data_from_api(
            row['hudle_venue_id'], 
            row['hudle_court_id'], 
            row['venue_id'], 
            row['court_id']
        ), 
        axis=1
    )
