from includes.common_functions import initialize_selenium_driver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import json


DATA_FILE_PATH = "./data-scraping/scraped-data/"
DATA_FILE_NAME = "hudle_venues_data.json"
driver = initialize_selenium_driver()

if not os.path.exists(DATA_FILE_PATH):
    print(f"JSON file not found at {DATA_FILE_PATH}. Please check the file path.")
    driver.quit()
    exit()

with open(DATA_FILE_PATH, 'r') as f:
    venues = json.load(f)


# This is used to click on select Activity Pickleball
def select_activity_pickleball(venue):
    try:
        driver.get(venue["venue_link"])
        book_pickleball_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//p[contains(text(), 'Pickleball')]/ancestor::div[contains(@class, 'style_bookingCard__E1MOb')]//button[contains(@class, 'style_btnBook__vzqXl')]"))
        )
        book_pickleball_button.click()
        time.sleep(2)
        return True
    except Exception as e:
        print(f"Error fetching address for {venue['title']}: {e}")    
        return False

def get_court_data():
    facility_cards = driver.find_elements(By.CLASS_NAME, "style_bookingCard__33ck6")
    courts = []
    for card in facility_cards:
        facility_name = card.find_element(By.CLASS_NAME, "style_facilityName__2rCni").text
        operating_hours = card.find_element(By.CLASS_NAME, "txt--blue-light").text
        price = card.find_element(By.CLASS_NAME, "fw--600").text

        courts.append({
            "facility_name": facility_name,
            "operating_hours": operating_hours,
            "price": price
        })

    courts_json = json.dumps(courts, indent=4)
    return courts_json

def check_if_multiple_courts(venue):
    try:
        courts = driver.find_elements(By.XPATH, "//div[contains(@class, 'style_bookingCard__33ck6')]")
        if len(courts) > 1:
            courts = get_court_data()
            return courts
    except Exception as e:
        return False
    
def get_number_of_courts(venue):
    try:
        return len(driver.find_elements(By.XPATH, "//div[contains(@class, 'style_bookingCard__33ck6')]"))
    except Exception as e:
        return 1

# Iterating over Venues Pages
for venue in venues:
    open_venue_page = select_activity_pickleball(venue)
    if open_venue_page:
        select_activity_pickleball(venue)
        get_number_of_courts(venue)

        courts = check_if_multiple_courts(venue)
        if courts:
            venue["courts"] = courts
        else:
            venue["courts"] = []
        


driver.quit()