import time
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


driver_path = r'C:/Project/New folder/Picleball/static/chromedriver.exe'

# Create a new instance of the Chrome driver
service = Service(executable_path=driver_path)
driver = Chrome(service=service)
driver.maximize_window()
driver.implicitly_wait(10)

# Load your HTML page or URL
driver.get("https://hudle.in/venues/players-x-maniac-pickleball-basketball-academy-malad/876806")

driver.find_element(By.XPATH, '//button[text()='Book']').click()

time.sleep(10)
# Close the driver
driver.quit()
