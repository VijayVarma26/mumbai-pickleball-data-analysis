from includes.common_functions import initialize_selenium_driver , read_json_file
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import json
import pandas as pd


DATA_FILE_PATH = "./scraped_data/venue_data/"
DATA_FILE_NAME = "hudle_venues_data_22-03-2025.csv"

# Clicking on Activity Pickleball
def select_activity_pickleball(venue):
    try:
        driver.get(venue)
        book_pickleball_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//p[contains(text(), 'Pickleball')]/ancestor::div[contains(@class, 'style_bookingCard__E1MOb')]//button[contains(@class, 'style_btnBook__vzqXl')]"))
        )
        book_pickleball_button.click()
        time.sleep(2)
        return True
    except Exception as e:
        print(f"Error fetching address for {venue['title']}: {e}")
        return False

# fetching number of courts in the venue 
def get_number_of_courts():
    try:
        return len(driver.find_elements(By.XPATH, "//div[contains(@class, 'style_bookingCard__33ck6')]"))
    except Exception as e:
        return 1

def read_csv(data_folder, file_name):
    full_path = os.path.join(data_folder, file_name)
    try:
        return pd.read_csv(full_path)
    except Exception as e:
        print(f"Error reading CSV file at {full_path}: {e}")
        return None

def scrape_number_of_courts(venue_url):
    try:
        select_activity_pickleball(venue_url)
        return get_number_of_courts()
    except Exception as e:
        print(f"Error fetching number of courts: {e}")
        return "Error: Check Manually"

driver = initialize_selenium_driver()

# Load venues data
venues = read_csv(DATA_FILE_PATH, DATA_FILE_NAME)

results = []

for index, venue in venues.iterrows():
    venue_url = venue.get("venue_link")
    if venue_url:
        courts = scrape_number_of_courts(venue_url)
        venues.at[index, "court_count"] = courts

# Save results to a new CSV file
output_file_path = os.path.join(DATA_FILE_PATH, f"{DATA_FILE_NAME.split('.')[0]}_with_courts.csv")
venues.to_csv(output_file_path, index=False)

driver.quit()