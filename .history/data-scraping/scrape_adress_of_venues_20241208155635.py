from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


with open("\scraped-data\hudle_venues_data.json"
driver_path = r'C:/Project/New folder/Picleball/static/chromedriver.exe'
# Create a new instance of the Chrome driver
service = Service(executable_path=driver_path)
driver = Chrome(service=service)
driver.maximize_window()
driver.implicitly_wait(10)


with open("./data-scraping/scraped-data/hudle_venues_data.json") as f:
    venues = json.load(f)


for venue in venues:
    driver.get(venue["Venue Link"])
    time.sleep(5)
    address = driver.find_element(By.XPATH, "//div[@class ='txt--blue-70 d-flex']/p").text
    print(f"Venue: {venue['Title']}\tAddress: {address}\n")
    venue["Address"] = address

    

# Open Venue
driver.get("https://hudle.in/venues/padel-360-worli/496598")

driver.find_element(By.XPATH, "//div[@class='card-body']").click()

time.sleep(10)
# Close the driver
driver.quit()
