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

# Locate the slot table
slot_table = driver.find_element(By.CSS_SELECTOR, "div.style_slotTable__1t-1a")

# Extract header (dates and days)
headers = slot_table.find_elements(By.CSS_SELECTOR, "tr.style_topRowTr__1XsL5 td.style_filledTopSlot__WoOB7")
dates = [{"date": h.find_element(By.CSS_SELECTOR, ".style_date__vVFsu").text,
          "day": h.find_element(By.CSS_SELECTOR, ".style_day__1K73h").text} for h in headers]

# Initialize result structure
slots_data = []

# Extract rows (times and slots)
rows = slot_table.find_elements(By.CSS_SELECTOR, "tr.style_slot-row-wrapper__2ttUt")
for row in rows:
    time_cell = row.find_element(By.CSS_SELECTOR, ".style_time__3lz2a")
    time = time_cell.text

    # Extract slot details
    slot_cells = row.find_elements(By.CSS_SELECTOR, "td")[1:]  # Skip time column
    slot_info = []
    for cell in slot_cells:
        if "slot-item" in cell.get_attribute("class"):
            price = cell.find_element(By.CSS_SELECTOR, ".price").text.replace("₹", "").strip()
            left = cell.find_element(By.CSS_SELECTOR, ".left").text.replace("left", "").strip()
            slot_info.append({"price": price, "left": left})
        else:
            slot_info.append({"price": None, "left": None})

    # Combine time and slot information
    slots_data.append({"time": time, "slots": slot_info})

# Compile final JSON structure
result = {
    "dates": dates,
    "slots": slots_data
}

# Print or save as JSON
print(json.dumps(result, indent=4))

# Close the driver
driver.quit()
