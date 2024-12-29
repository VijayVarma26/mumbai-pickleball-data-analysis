from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
driver_path = r'./static/driver'

# Create a new instance of the Chrome driver
service = Service(executable_path=driver_path)
driver = Chrome(service=service)
driver.maximize_window()
driver.implicitly_wait(10)

# Navigate to the website
driver.get("https://fiu.az/sanctions/internal-sanctioned")

# Find the table element
table = driver.find_elements(By.XPATH,"//div[contains(@class, 'sanctioned-table')]//table//tr//td[2]")

# Loop through the rows and print the data
for row in table:
        print(row.text)

# Close the webdriver
driver.quit()