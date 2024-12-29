import time
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
driver_path = r'C:/Project/New folder/Picleball/static/chromedriver.exe'

# Create a new instance of the Chrome driver
service = Service(executable_path=driver_path)
driver = Chrome(service=service)
driver.maximize_window()
driver.implicitly_wait(10)
driver.get("https://hudle.in/pages/pickleball-venues-mumbai")  # Replace with the actual page containing multiple elements

# Locate the containers that hold venue details
venue_elements = driver.find_elements(By.XPATH, '//div[@class="article col-sm-6 col-md-4 col-12"]')

print(len(venue_elements))

driver.quit()
venues = []

for venue in venue_elements:
    try:
        title = venue.find_element(By.XPATH, './/h2[@class="title-head text-truncate"]').text
        location = venue.find_element(By.XPATH, './/p[@class="ellipsis"]').text
        price = venue.find_element(By.XPATH, './/span[@class="info-text"]').text

        print(f"Title: {title}") 
#         link = venue.find_element(By.XPATH, './/a[contains(@href, "https://hudle.in/venues/")]').get_attribute("href")
        
#         # Save the extracted data into a dictionary
        venue_data = {
            "Title": title,
            "Location": location,
            "Price": price,
            # "Link": link
        }
        venues.append(venue_data)
        print(venue_data)

        break
    except Exception as e:
        print(f"Error extracting details from a container: {e}")


# print(venues)
