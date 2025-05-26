import os
import json
import requests
import pandas as pd
from datetime import datetime

# === CONFIGURATION ===
OUTPUT_FOLDER = "../../data/raw_data/injested_data"
COURT_DATA_CSV = "../../data/raw_data/courts_data/hudle_court_data.csv"
MISSING_DATE_TRACKER_CSV = "../../data/Venue_Data_Date_Tracker.csv"

HEADERS = {
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


def fetch_slot_for_date(session, hudle_venue_id, hudle_court_id, venue_id, court_id, date_obj):
    date_str = date_obj.strftime("%Y-%m-%d")
    url = f"https://api.hudle.in/api/v1/venues/{hudle_venue_id}/facilities/{hudle_court_id}/slots"
    params = {"start_date": date_str, "end_date": date_str, "grid": 1}

    try:
        response = session.get(url, headers=HEADERS, params=params, timeout=10)
        if response.status_code == 200:
            print(f"✅ Success: Venue {venue_id}, Court {court_id}, Date {date_str}")
            save_json_data(venue_id, court_id, date_str, response.json())
        else:
            print(f"❌ Failed: Venue {venue_id}, Court {court_id}, Date {date_str} - Status: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: Venue {venue_id}, Court {court_id}, Date {date_str} - {e}")


def save_json_data(venue_id, court_id, date_str, data):
    folder_path = os.path.join(OUTPUT_FOLDER, str(venue_id), date_str)
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, f"{court_id}.json")
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"❌ Failed to write file: {file_path} - {e}")


def main():
    # Load missing dates file
    try:
        missing_df = pd.read_csv(MISSING_DATE_TRACKER_CSV, dtype={"venue_id": str})
    except Exception as e:
        print(f"❌ Failed to read missing date tracker: {e}")
        return

    # Load full court info
    try:
        court_df = pd.read_csv(COURT_DATA_CSV, dtype={"venue_id": str, "court_id": str})
    except Exception as e:
        print(f"❌ Failed to read court data: {e}")
        return

    session = requests.Session()
    try:
        session.get("https://hudle.in", headers=HEADERS, timeout=5)
    except Exception as e:
        print(f"❌ Session init failed: {e}")
        return

    for _, row in missing_df.iterrows():
        venue_id = str(row['venue_id'])
        missing_dates = str(row['missing_dates']).split(',')

        venue_courts = court_df[court_df['venue_id'] == venue_id]

        if venue_courts.empty:
            print(f"⚠️ No court data found for venue_id {venue_id}")
            continue

        for date_str in missing_dates:
            date_str = date_str.strip()
            try:
                date_obj = datetime.strptime(date_str, "%d-%m-%Y")
            except Exception as e:
                print(f"❌ Invalid date format: {date_str} for venue {venue_id}")
                continue

            for _, court_row in venue_courts.iterrows():
                fetch_slot_for_date(
                    session,
                    court_row['hudle_venue_id'],
                    court_row['hudle_court_id'],
                    court_row['venue_id'],
                    court_row['court_id'],
                    date_obj
                )


if __name__ == "__main__":
    main()
