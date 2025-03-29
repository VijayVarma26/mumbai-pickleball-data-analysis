import requests


def get_data_from_api(hudle_venue_id, hudle_court_id, params, headers):
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
        print(response.json())  
    else:
        print(f"❌ API Request Failed! Status Code: {response.status_code}")
        print(response.text)  # Print error details if any

