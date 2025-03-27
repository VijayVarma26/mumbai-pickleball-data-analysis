import requests

# API Endpoint
url = "https://api.hudle.in/api/v1/venues/ce7f35e8-8486-4623-8d9c-0a7d01e3f40f/facilities/5ee2b31f-af67-4453-9cd0-cc63a3485215/slots"

# Query Parameters
params = {
    "start_date": "2025-03-26",
    "end_date": "2025-03-27",
    "grid": 1
}

# Headers exactly as seen in the browser request
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

# Step 1: Visit the homepage to get session cookies (optional)
session.get("https://hudle.in/", headers=headers)

# Step 2: Make the actual API request using the session
response = session.get(url, params=params, headers=headers)

# Step 3: Check the response
if response.status_code == 200:
    print("✅ API Request Successful!")
    print(response.json())  # Print the JSON response
else:
    print(f"❌ API Request Failed! Status Code: {response.status_code}")
    print(response.text)  # Print error details if any
