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
    driver.get("https://hudle.in/pages/pickleball-venues-mumbai")  # Replace with the actual page containing multiple elements

    # Define the XPaths for elements
    container_xpath = '//div[@class="article col-sm-6 col-md-4 col-12"]'
    title_xpath = './/h2[@class="title-head text-truncate"]'
    location_xpath = './/div[contains(@class, "info-content-address")]/p[@class="ellipsis"]'
    price_xpath = './/div[@class="info-right"]/span[@class="info-text"]'
    link_xpath = './/a[contains(@href, "venues") and @target="_blank"]'  # Updated XPath

    # Find all containers for items
    containers = driver.find_elements(By.XPATH, container_xpath)

    # Initialize a list to hold the venue dictionaries
    venues = []

    # Iterate over each container and extract data
    for container in containers:
        try:
            # Extract details
            title = container.find_element(By.XPATH, title_xpath).text
            location = container.find_element(By.XPATH, location_xpath).text
            price = container.find_element(By.XPATH, price_xpath).text
            
            # Attempt to extract the link
            try:
                link = container.find_element(By.XPATH, link_xpath).get_attribute("href")
            except:
                link = "No link available"

            # Create a dictionary for the current venue
            venue_details = {
                "Title": title,
                "Location": location,
                "Price": price,
                "Link": link
            }

            # Add the dictionary to the list
            venues.append(venue_details)
            print(venue_details)
        except Exception as e:
            print(f"Error extracting details from a container: {e}")

    # Print the consolidated dictionary
    print(len(venues))

finally:
    # Quit the driver
    driver.quit()
