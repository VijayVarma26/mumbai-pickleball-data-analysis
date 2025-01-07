import json
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
import os

# Initializing the selenium Driver
def initialize_selenium_driver():
    DRIVER_PATH = r'C:/Project/New folder/Picleball/static/chromedriver.exe'
    service = Service(executable_path=DRIVER_PATH)
    driver = Chrome(service=service)
    driver.maximize_window()
    driver.implicitly_wait(10)
    return driver

# Write data to json file with file_name
def write_slot_to_json(file_name, json_data):
    try:
        with open(file_name, 'w') as f:
            json_data = json.dump(json_data, f, indent=4)
            print(f"Data written to {file_name}")
    except Exception as e:
        print(f"Error writing JSON file: {e}")
        

# Read data from json file with file_name
def read_json_file(file_path, file_name):
    try:
        file = os.path.join(file_path, file_name)
        with open(file, 'r') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return None
    
    