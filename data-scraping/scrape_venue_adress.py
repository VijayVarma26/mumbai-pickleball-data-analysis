from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from includes.common_functions import initialize_selenium_driver
import json
import os


driver = initialize_selenium_driver()
data_file_path = "./data-scraping/scraped-data/hudle_venues_data.json"


if not os.path.exists(data_file_path):
    print(f"JSON file not found at {data_file_path}. Please check the file path.")
    driver.quit()
    exit()

# Load venues data
with open(data_file_path, 'r') as f:
    venues = json.load(f)

for venue in venues:
    try:
        driver.get(venue["venue_link"])

        address_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class ='txt--blue-70 d-flex']/p"))
        )
        address = address_element.text
        venue["address"] = address

    except Exception as e:
        print(f"Error fetching address for {venue['Title']}: {e}")
        venue["Address"] = "N/A" 

try:
    with open(data_file_path, 'w') as fp:
        json.dump(venues, fp, indent=4)
    print(f"Output written to: {data_file_path}")

except Exception as e:
    print(f"Error writing output to JSON: {e}")

driver.quit()
