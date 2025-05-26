import os
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# --- Configuration ---
CHROMEDRIVER_PATH = r'C:/Project/New folder/Pickleball/static/chromedriver.exe'
MASTER_CSV_PATH = r"C:\Project\New folder\Pickleball\data\raw_data\venue_data\hudle_venues_data.csv"
ADDRESS_XPATH = "//div[@class ='txt--blue-70 d-flex']/p"

# --- Functions ---

def initialize_driver(driver_path=CHROMEDRIVER_PATH):
    service = Service(executable_path=driver_path)
    driver = Chrome(service=service)
    driver.maximize_window()
    driver.implicitly_wait(10)
    return driver

def load_master_data(filepath: str) -> pd.DataFrame:
    """Load master CSV into a DataFrame"""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"[ERROR] File not found: {filepath}")

    df = pd.read_csv(filepath, dtype=str)
    df.fillna("", inplace=True)
    print(f"[INFO] Loaded {len(df)} rows from master CSV")
    return df


def get_missing_address_indices(df: pd.DataFrame) -> pd.Index:
    """Return indices where address is missing or empty"""
    return df[df['address'].str.strip() == ""].index


def fetch_address_from_venue(driver, venue_url: str) -> str:
    """Use Selenium to extract address from a venue URL"""
    try:
        driver.get(venue_url)
        address_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, ADDRESS_XPATH))
        )
        return address_element.text.strip()
    except Exception as e:
        print(f"[WARN] Failed to fetch address from {venue_url}: {e}")
        return "N/A"


def update_addresses(df: pd.DataFrame, indices: pd.Index, driver) -> pd.DataFrame:
    """Update the DataFrame with scraped addresses for missing entries"""
    for idx in indices:
        venue_link = df.at[idx, "venue_link"]
        venue_name = df.at[idx, "venue_name"]
        print(f"[INFO] Scraping address for: {venue_name} | URL: {venue_link}")

        address = fetch_address_from_venue(driver, venue_link)
        df.at[idx, "address"] = address
        print(f"[{idx}] Updated address: {address}")

    return df


def save_updated_data(df: pd.DataFrame, filepath: str):
    """Save DataFrame back to CSV"""
    try:
        df.to_csv(filepath, index=False)
        print(f"[INFO] Master CSV successfully updated at: {filepath}")
    except Exception as e:
        print(f"[ERROR] Failed to save CSV: {e}")


def main():
    # Step 1: Load data
    df = load_master_data(MASTER_CSV_PATH)

    # Step 2: Find missing addresses
    missing_indices = get_missing_address_indices(df)
    if not missing_indices.any():
        print("[INFO] No missing addresses to update.")
        return

    print(f"[INFO] Found {len(missing_indices)} venues with missing addresses")

    # Step 3: Initialize Selenium
    driver = initialize_driver()

    try:
        # Step 4: Update missing addresses
        df = update_addresses(df, missing_indices, driver)

        # Step 5: Save updated CSV
        save_updated_data(df, MASTER_CSV_PATH)

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
