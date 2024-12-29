import time
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


driver_path = r'C:/Project/New folder/Picleball/static/chromedriver.exe'

# Create a new instance of the Chrome driver
service = Service(executable_path=driver_path)
driver = Chrome(service=service)
driver.maximize_window()
driver.implicitly_wait(10)
driver.get("https://hudle.in/pages/pickleball-venues-mumbai")  # Replace with the actual page containing multiple elements


# Wait until the venue elements are present
venue_elements = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.XPATH, '//div[@class="card2-inner-section"]'))
)

print(len(venue_elements))
venues = []

for venue in venue_elements:
    try:
        # Extracting image URL
        image_url = venue.find_element(By.XPATH, './/div[@class="card2-inner-image"]/img').get_attribute('src')
        
        # Extracting title
        title = venue.find_element(By.XPATH, './/h2[@class="title-head"]').text
        
        # Extracting location
        location = venue.find_element(By.XPATH, './/div[@class="loc-icon"]/p').text
        
        # Extracting rating
        rating = venue.find_element(By.XPATH, './/span[@class="vue-rate-it-rating-text"]').text
        
        # Extracting price
        price = venue.find_element(By.XPATH, './/span[@class="info-text2x"]').text
        
        # Save the extracted data into a dictionary
        venue_data = {
            "Title": title,
            "Location": location,
            "Rating": rating,
            "Price": price,
            "Image URL": image_url
        }
        venues.append(venue_data)
    except Exception as e:
        print(f"Error extracting details from a container: {e}")

# Output all venues in a dictionary format
print(venues)
