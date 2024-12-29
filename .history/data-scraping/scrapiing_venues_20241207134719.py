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

try:
    # Load the webpage
    driver.get("https://hudle.in/pages/pickleball-venues-mumbai")
    
    # Extract the data using XPaths
    title_xpath = '//h2[@class="title-head text-truncate" and contains(@style, "color")]'
    location_xpath = '//div[contains(@class, "info-content-address")]/p[@class="ellipsis" and contains(@style, "color")]'
    price_xpath = '//div[@class="info-right"]/span[@class="info-text" and contains(@style, "color")]'

    # Fetch the elements
    title = driver.find_element(By.XPATH, title_xpath).text
    # location = driver.find_element(By.XPATH, location_xpath).text
    # price = driver.find_element(By.XPATH, price_xpath).text

    # Print the results
    print(f"Title: {title}")
    # print(f"Location: {location}")
    # print(f"Price: ₹{price}")

finally:
    # Quit the driver
    driver.quit()