from includes.common_functions import initialize_selenium_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import json
import os
from datetime import datetime

driver = initialize_selenium_driver()


driver.implicitly_wait(10)
driver.get("https://hudle.in/pages/pickleball-venues-mumbai")

# Wait until the venue elements are present
venue_elements = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.XPATH, "//div[@class='row']/div"))
)

venues = []

for venue in venue_elements:
    try:
        title = venue.find_element(By.XPATH, ".//h2[@class='title-head text-truncate']").text
        location = venue.find_element(By.XPATH, ".//p[@class='ellipsis']").text
        price = venue.find_element(By.XPATH, ".//span[@class='info-text']").text
        venue_link = venue.find_element(By.XPATH, ".//a[contains(@href, 'hudle.in/venues')]").get_attribute("href")

        venue_data = {
            "title": title,
            "location": location,
            "price": price,
            "venue_link": venue_link
        }

        venues.append(venue_data)
    except Exception as e:
        print(f"Error extracting details from a venue: {e}")

driver.quit()

output_dir = './scraped_data/'
os.makedirs(output_dir, exist_ok=True)

# Get the current date in dd-mm-yyyy format
current_date = datetime.now().strftime("%d-%m-%Y")
output_file = os.path.join(output_dir, f'hudle_venues_data_{current_date}.json')
try:
    with open(output_file, 'w') as fp:
        json.dump(venues, fp, indent=4)

    print(f"Output written to: {output_file}")

except Exception as e:
    print(f"Error writing output to JSON: {e}")
