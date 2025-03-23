from geopy.geocoders import Nominatim
import pandas as pd
import time
import json

# Initialize geolocator
geolocator = Nominatim(user_agent="geo_locator")

# Venue data
# Read the JSON file
with open('../data-scraping/scraped_data/hudle_venues_data_22-03-2025.json', 'r') as file:
    venues_data = json.load(file)

# Extract venue addresses
venues = [{"address": venue["address"]} for venue in venues_data]

# Function to get latitude and longitude
def get_lat_lon(address):
    try:
        location = geolocator.geocode(address)
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except:
        return None, None

# Convert to DataFrame
df = pd.DataFrame(venues)

# Fetch lat/lon with delay to avoid rate limits
df["Latitude"], df["Longitude"] = zip(*df["address"].apply(lambda x: get_lat_lon(x) or (None, None)))

# Display the DataFrame
print(df)
