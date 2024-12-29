from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
from bs4 import BeautifulSoup
import json



DRIVER_PATH = r'C:/Project/New folder/Picleball/static/chromedriver.exe'
DATA_FILE_PATH = "./data-scraping/scraped-data/hudle_venues_data.json"

service = Service(executable_path=DRIVER_PATH)
driver = Chrome(service=service)
driver.maximize_window()
driver.implicitly_wait(10)


if not os.path.exists(DATA_FILE_PATH):
    print(f"JSON file not found at {DATA_FILE_PATH}. Please check the file path.")
    driver.quit()
    exit()

with open(DATA_FILE_PATH, 'r') as f:
    venues = json.load(f)


# This is used to click  selecting Activity Pickleball
def select_activity_pickleball(venue):
    try:
        driver.get(venue["venue_link"])
        book_pickleball_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//p[contains(text(), 'Pickleball')]/ancestor::div[contains(@class, 'style_bookingCard__E1MOb')]//button[contains(@class, 'style_btnBook__vzqXl')]"))
        )
        book_pickleball_button.click()
        time.sleep(2)
        return True
    except Exception as e:
        print(f"Error fetching address for {venue['title']}: {e}")    
        return False

def check_if_multiple_courts(venue):
    try:
        courts = driver.find_elements(By.XPATH, "//div[contains(@class, 'style_bookingCard__33ck6')]")
        if len(courts) > 1:
            return True
        return False
    except Exception as e:
        return False
    
def get_number_of_courts(venue):
    try:
        return len(driver.find_elements(By.XPATH, "//div[contains(@class, 'style_bookingCard__33ck6')]"))
    except Exception as e:
        return 1


# Get The table of court slots
def get_slot_table():
    try:
        slot_table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'p--15-mob pb--50-mob card-body')]//table[contains(@class,'style_table__gYUfm')]"))
        )
        return slot_table
    except Exception as e:
        print(f"Error fetching slot table: {e}")
        return None

def get_available_slot_price_from_col(day_num, row):
    row_data = {}
    
    row_data['time'] = row.find_all('td')[0].text
    row_data['is_available'] = True if row.find_all('td')[day_num].text else False
    
    # Extract price and left elements
    price_div = row.find_all('td')[day_num].find('div', class_='slot-item available')
    if price_div:
        row_data['price'] = price_div.find('p', class_='price').text.strip()
        row_data['left'] = price_div.find('p', class_='left').text.strip()
    else:
        row_data['price'] = "N/A"
        row_data['left'] = "N/A"

    return row_data

def get_slot_data_from_table(table):
    table_html = table.get_attribute('outerHTML')
    soup = BeautifulSoup(table_html, 'html.parser')

    table_data = []
    days = []
    row_num = 1
    day1 = []
    day2= []
    day3 = []
    day4 = []

    for row in soup.find('tbody').find_all('tr'):
        if row_num == 1:
            days = [day.text for day in row.find_all('td')]
            print(f"Days: {days}")
        else:
            day1.append(get_available_slot_price_from_col(1, row))
            day2.append(get_available_slot_price_from_col(2, row))
            day3.append(get_available_slot_price_from_col(3, row))
            day4.append(get_available_slot_price_from_col(4, row))
        row_num += 1

    table_data.append({
        "slot_date": days[1],
        "slots": day1
    })
    table_data.append({
        "slot_date": days[2],
        "slots": day2
    })
    table_data.append({
        "slot_date": days[3],
        "slots": day3
    })
    table_data.append({
        "slot_date": days[4],
        "slots": day4
    })

    # Convert the table data to JSON format
    table_json = json.dumps(table_data, indent=4)
    return table_json


# Iterating over Venues (Opening Venue Pages)
for venue in venues:
    open_venue_page = select_activity_pickleball(venue)
    if open_venue_page:
        venue["is_multiple_court"]  = check_if_multiple_courts(venue)
        venue["court_count"] = get_number_of_courts(venue)
    else:
        venue["is_multiple_court"]  = check_if_multiple_courts(venue)
        venue["court_count"] = get_number_of_courts(venue)
    slot_table = get_slot_table()    
    if slot_table:
        slots_data = get_slot_data_from_table(slot_table)
        # print(slot_table)
    break   





# # Writing The output to json file
# try:
#     with open(DATA_FILE_PATH, 'w') as fp:
#         json.dump(venues, fp, indent=4)
#     print(f"Output written to: {DATA_FILE_PATH}")

# except Exception as e:
#     print(f"Error writing output to JSON: {e}")

driver.quit()