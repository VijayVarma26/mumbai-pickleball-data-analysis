from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import os
import time


driver_path = r'C:/Project/New folder/Picleball/static/chromedriver.exe'

service = Service(executable_path=driver_path)
driver = Chrome(service=service)
driver.maximize_window()
driver.implicitly_wait(10)


data_file_path = "./data-scraping/scraped-data/hudle_venues_data.json"
if not os.path.exists(data_file_path):
    print(f"JSON file not found at {data_file_path}. Please check the file path.")
    driver.quit()
    exit()

with open(data_file_path, 'r') as f:
    venues = json.load(f)


def select_activity_pickleball(venue):
    try:
        driver.get(venue["Venue Link"])
        book_pickleball_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//p[contains(text(), 'Pickleball')]/ancestor::div[contains(@class, 'style_bookingCard__E1MOb')]//button[contains(@class, 'style_btnBook__vzqXl')]"))
        )
        book_pickleball_button.click()
        time.sleep(2)
        return True
    except Exception as e:
        print(f"Error fetching address for {venue['Title']}: {e}")    
        return False

def get_court_details(venue):
    



# iterating over Venues (Opening Venue Pages)
for venue in venues:
      open_venue_page = select_activity_pickleball(venue)
      if open_venue_page:
          pass
      else:
          pass


try:
    with open(data_file_path, 'w') as fp:
        json.dump(venues, fp, indent=4)
    print(f"Output written to: {data_file_path}")

except Exception as e:
    print(f"Error writing output to JSON: {e}")

driver.quit()