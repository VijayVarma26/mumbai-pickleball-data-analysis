from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import json
import os

# Path to ChromeDriver
driver_path = r'C:/Project/New folder/Picleball/static/chromedriver.exe'
service = Service(executable_path=driver_path)
driver = Chrome(service=service)

driver.implicitly_wait(10)
driver.get("https://hudle.in/pages/pickleball-venues-mumbai")

# Wait until the venue elements are present
venue_elements = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.XPATH, "//div[@class='row']/div"))
)

print(f"Number of venues found: {len(venue_elements)}")

venues = []

for venue in venue_elements:
    try:
        # Extracting title
        title = venue.find_element(By.XPATH, ".//h2[@class='title-head text-truncate']").text
        
        # Extracting location
        location = venue.find_element(By.XPATH, ".//p[@class='ellipsis']").text
        
        # Extracting price
        price = venue.find_element(By.XPATH, ".//span[@class='info-text']").text
        
        # Extracting venue link
        venue_link = venue.find_element(By.XPATH, ".//a[contains(@href, 'hudle.in/venues')]").get_attribute("href")

        venue_data = {
            "Title": title,
            "Location": location,
            "Price": price,
            "Venue Link": venue_link
        }
        
        print(f"Extracted: {venue_data}")
        venues.append(venue_data)
    except Exception as e:
        print(f"Error extracting details from a venue: {e}")

driver.quit()

# Ensure the directory exists
output_dir = './data-scraping/scraped-data/'
os.makedirs(output_dir, exist_ok=True)

# Write the extracted data to a JSON file
output_file = os.path.join(output_dir, 'hudle_venues_data.json')
try:
    with open(output_file, 'w') as fp:
        json.dump(venues, fp, indent=4)

    print(f"Output written to: {output_file}")

except Exception as e:
    print(f"Error writing output to JSON: {e}")
