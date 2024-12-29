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

    driver.get("https://hudle.in/pages/pickleball-venues-mumbai")
   
    title_xpath = '//h2[@class="title-head text-truncate" and contains(@style, "color")]'
    location_xpath = '//div[contains(@class, "info-content-address")]/p[@class="ellipsis" and contains(@style, "color")]'
    price_xpath = '//div[@class="info-right"]/span[@class="info-text" and contains(@style, "color")]'
    link_xpath = '//a[@href and @target="_blank"]'

    # Fetch the elements
    title = driver.find_elements(By.XPATH, title_xpath)
    location = driver.find_elements(By.XPATH, location_xpath)
    price = driver.find_elements(By.XPATH, price_xpath)
    link = driver.find_elements(By.XPATH, link_xpath)


    venues = []
    for t, l, p, li in zip(title, location, price, link):
        venues.append({"title": t.text, "location": l.text, "price": p.text, "link": li.text})

    print(venues)

finally:
    driver.quit()