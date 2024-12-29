from selenium import webdriver

# Set the path to the chromedriver executable
chromedriver_path = "../static/chromedriver.exe"

# Create a new instance of the Chrome driver
driver = webdriver.Chrome(executable_path=chromedriver_path)

# Open a website
driver.get("http://www.example.com")


# Close the driver
driver.quit()


