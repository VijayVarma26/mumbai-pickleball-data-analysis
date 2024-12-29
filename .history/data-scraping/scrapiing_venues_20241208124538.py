import time
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json

driver_path = r'C:/Project/New folder/Picleball/static/chromedriver.exe'

# Create a new instance of the Chrome driver
service = Service(executable_path=driver_path)
driver = Chrome(service=service)
# driver.maximize_window()
driver.implicitly_wait(10)
driver.get("https://hudle.in/pages/pickleball-venues-mumbai")  # Replace with the actual page containing multiple elements


# Wait until the venue elements are present
venue_elements = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.XPATH, '//*[@id="__layout"]/div/div/div/div[3]/div/div/div/div/a'))
)

print(len(venue_elements))
venues = []

for venue in venue_elements:
    try:        
        # Extracting title
        title = venue.find_element(By.XPATH, '//*[@id="__layout"]/div/div/div/div[3]/div/div/div/div/a/div/div/div/div[2]/div/div/div/h2').text
        
        # Extracting location
        location = venue.find_element(By.XPATH, '//*[@id="__layout"]/div/div/div/div[3]/div/div/div/div/a/div/div/div/div[2]/div[1]/div[2]/div/div/div/p').text
        
        # Extracting price
        price = venue.find_element(By.XPATH, '//*[@id="__layout"]/div/div/div/div[3]/div/div/div/div/a/div/div/div/div[2]/div[2]/div[2]/span[1]').text
        
        venue_link = venue.find_element(By.XPATH, '//a[contains(@href, "//*[@id="__layout"]/div/div/div/div[3]/div/div/div/div/a")
        # Save the extracted data into a dictionary
        venue_data = {
            "Title": title,
            "Location": location,
            "Price": price,
            # "Venue Link": venue_link.get_attribute('href')
        }
        venues.append(venue_data)
    except Exception as e:
        print(f"Error extracting details from a container: {e}")

with open('hudle_venues_data.json', 'w') as fp:
    json.dump(venue_data, fp)

print("Output Written to: hudle_venues_data.json")
