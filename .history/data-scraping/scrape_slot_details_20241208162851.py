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

for venue in venues:
    try:
        driver.get(venue["Venue Link"])

        book_pickleball_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class ='txt--blue-70 d-flex']/p"))
        )
        
        time.sleep(5)



    except Exception as e:
        print(f"Error fetching address for {venue['Title']}: {e}")
        

try:
    with open(data_file_path, 'w') as fp:
        json.dump(venues, fp, indent=4)
    print(f"Output written to: {data_file_path}")

except Exception as e:
    print(f"Error writing output to JSON: {e}")

driver.quit()