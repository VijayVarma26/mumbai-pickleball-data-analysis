import os
import csv
from datetime import datetime
import pandas as pd
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- Config ---
CHROMEDRIVER_PATH = r'C:/Project/New folder/Pickleball/static/chromedriver.exe'
VENUES_URL = "https://hudle.in/pages/pickleball-venues-mumbai"
OUTPUT_DIR = 'C:/Project/New folder/Pickleball/data/raw_data/venue_data/'
MASTER_CSV = os.path.join(OUTPUT_DIR, "hudle_venues_data.csv")


def initialize_driver(driver_path=CHROMEDRIVER_PATH):
    service = Service(executable_path=driver_path)
    driver = Chrome(service=service)
    driver.maximize_window()
    driver.implicitly_wait(10)
    return driver


def scrape_venues(driver, url=VENUES_URL):
    driver.get(url)
    try:
        venue_anchors = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//a[.//div[contains(@class, 'small-card-flex')]]"))
        )
    except Exception as e:
        print(f"[ERROR] Could not locate venue elements: {e}")
        return []

    print(f"[INFO] Found {len(venue_anchors)} venue cards")
    venues = []

    for idx, venue_anchor in enumerate(venue_anchors, start=1):
        try:
            venue_link = venue_anchor.get_attribute("href")
            venue_div = venue_anchor.find_element(By.XPATH, ".//div[contains(@class, 'small-card-flex')]")
            card_container = venue_anchor.find_element(By.XPATH, ".//div[contains(@class, 'card-inner')]")

            title = venue_div.find_element(By.XPATH, ".//h2[contains(@class, 'title-head')]").text.strip()
            location = venue_div.find_element(By.XPATH, ".//p[contains(@class, 'ellipsis')]").text.strip()
            price = venue_div.find_element(By.XPATH, ".//span[contains(@class, 'info-text')]").text.strip()
            image_url = card_container.find_element(By.XPATH, ".//div[contains(@class, 'base-image')]/img").get_attribute("src")

            venue_data = {
                "title": title,
                "city": location,
                "price": price,
                "venue_link": venue_link,
                "image_url": image_url,
                "venue_id": venue_link.split('/')[-1] if '/' in venue_link else None,
                "hudle_venue_id": image_url.split('/')[-3] if '/' in image_url else None,
            }

            venues.append(venue_data)

        except Exception as e:
            print(f"[{idx}] Skipped due to error: {e}")

    return venues


def deduplicate_and_save(data, output_dir=OUTPUT_DIR, master_csv=MASTER_CSV):
    os.makedirs(output_dir, exist_ok=True)
    today_str = datetime.now().strftime("%Y-%m-%d")
    today_file = os.path.join(output_dir, f"hudle_venues_{today_str}.csv")

    if not data:
        print("[INFO] No data scraped.")
        return

    # Transform scraped data to match master CSV schema
    transformed_data = []
    for item in data:
        transformed_data.append({
            "venue_id": item.get("venue_id", ""),
            "venue_name": item.get("title", ""),
            "city": item.get("location", ""),
            "venue_link": item.get("venue_link", ""),
            "address": "",
            "lattitude": "",
            "longitude": "",
            "is_new": True,
            "locality": "",
            "locality_zone": "",
            "court_count": "",
            "venue_image_api_url": item.get("image_url", ""),
            "hudle_venue_id": item.get("hudle_venue_id", ""),
        })

    new_df = pd.DataFrame(transformed_data)

    # Load master file if it exists
    if os.path.exists(master_csv):
        existing_df = pd.read_csv(master_csv, dtype=str)
        new_df = new_df[~new_df['venue_id'].isin(existing_df['venue_id'])]
    else:
        existing_df = pd.DataFrame()

    if new_df.empty:
        print("[INFO] No new venues to add.")
        return

    # Save today's new data
    new_df.to_csv(today_file, index=False)
    print(f"[INFO] {len(new_df)} new venue(s) written to {today_file}")

    # Append new rows to master CSV
    header_needed = not os.path.exists(master_csv) or os.path.getsize(master_csv) == 0
    with open(master_csv, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=new_df.columns)
        if header_needed:
            writer.writeheader()
        writer.writerows(new_df.to_dict(orient='records'))

    print(f"[INFO] Master file updated: {master_csv}")


def main():
    driver = initialize_driver()
    try:
        venues = scrape_venues(driver)
    finally:
        driver.quit()

    deduplicate_and_save(venues)


if __name__ == "__main__":
    main()
