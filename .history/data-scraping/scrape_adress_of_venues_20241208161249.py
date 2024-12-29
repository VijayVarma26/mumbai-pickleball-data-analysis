from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import os


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

# Load venues data
with open(data_file_path, 'r') as f:
    venues = json.load(f)

for venue in venues:
    try:
        driver.get(venue["Venue Link"])

        address_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class ='txt--blue-70 d-flex']/p"))
        )
        address = address_element.text
        print(f"Venue: {venue['Title']} \tAddress: {address}\n")
        venue["Address"] = address

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
