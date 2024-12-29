from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import os
import time


DRIVER_PATH = r'C:/Project/New folder/Picleball/static/chromedriver.exe'
DATA_FILE_PATH = "./data-scraping/scraped-data/hudle_venues_data.json"

service = Service(executable_path=DRIVER_PATH)
driver = Chrome(service=service)
driver.maximize_window()
driver.implicitly_wait(10)


if not os.path.exists(DATA_FILE_PATH):
    print(f"JSON file not found at {DATA_FILE_PATH}. Please check the file path.")
    driver.quit()
    exit()

with open(DATA_FILE_PATH, 'r') as f:
    venues = json.load(f)


# This is used to click  selecting Activity Pickleball
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

def check_if_multiple_courts(venue):
    courts = driver.find_elements(By.XPATH, "//div[contains(@class, 'style_bookingCard__33ck6')]")
    if len(courts) > 1:
        return True
    return False

def get_number_of_courts(venue):
    return len(driver.find_elements(By.XPATH, "//div[contains(@class, 'style_bookingCard__33ck6')]"))

def get_court_details(venue):
    pass



# iterating over Venues (Opening Venue Pages)
for venue in venues:
      open_venue_page = select_activity_pickleball(venue)
      if open_venue_page:
          venue["is-multiple_court"]  = check_if_multiple_courts(venue)
      else:
          venue["is-multiple_court"]  = check_if_multiple_courts(venue)
      venue["court_count"] = get_number_of_courts(venue)       


# Writing The output to json file
try:
    with open(DATA_FILE_PATH, 'w') as fp:
        json.dump(venues, fp, indent=4)
    print(f"Output written to: {DATA_FILE_PATH}")

except Exception as e:
    print(f"Error writing output to JSON: {e}")

driver.quit()