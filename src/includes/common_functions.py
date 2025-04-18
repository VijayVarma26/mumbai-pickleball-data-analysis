import json
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
import os
import csv
import pandas as pd

# Initializing the selenium Driver
def initialize_selenium_driver():
    DRIVER_PATH = r'C:/Project/New folder/Pickleball/static/chromedriver.exe'
    service = Service(executable_path=DRIVER_PATH)
    driver = Chrome(service=service)
    driver.maximize_window()
    driver.implicitly_wait(10)
    return driver

# Write data to json file with file_name
def write_slot_to_json(file_name, json_data):
    try:
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=4)
            print(f"Data written to {file_name}")
    except Exception as e:
        print(f"Error writing JSON file: {e}")

# Read data from json file with file_name
def read_json_file(file_path, file_name):
    try:
        file = os.path.join(file_path, file_name)
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return None

# Convert JSON data to CSV file
def json_to_csv(json_data, csv_file_name):
    try:
        # Open CSV file for writing
        with open(csv_file_name, 'w', newline='', encoding='utf-8') as csv_file:
            # Create a CSV writer object
            csv_writer = csv.writer(csv_file)
            # Write the header row
            header = json_data[0].keys()
            csv_writer.writerow(header)
            # Write the data rows
            for row in json_data:
                csv_writer.writerow(row.values())
                
        print(f"Data successfully written to {csv_file_name}")
    except Exception as e:
        print(f"Error converting JSON to CSV: {e}")
 

#  Read csv file
def read_csv_file(file_path):
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None

def get_config():
    try:
        with open('../../static/config.json', 'r') as config_file:
            config = json.load(config_file)
            return config
    except Exception as e:
        print(f"Error reading config file: {e}")
        return None
  