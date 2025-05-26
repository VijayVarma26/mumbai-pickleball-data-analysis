import os
import pandas as pd
from datetime import datetime, timedelta

# === CONFIGURATION ===
CSV_FILE_PATH = r"C:\Project\New folder\Pickleball\data\raw_data\venue_data\hudle_venues_data.csv"
INJESTED_DATA_ROOT = r"C:\Project\New folder\Pickleball\data\raw_data\injested_data"
REPORT_OUTPUT_PATH = r"C:\Project\New folder\Pickleball\data\Venue_Data_Date_Tracker.csv"
END_DATE = datetime.strptime("24-05-2025", "%d-%m-%Y")


def read_venue_data(csv_path):
    """Read the CSV and return a DataFrame with cleaned data."""
    df = pd.read_csv(csv_path, parse_dates=["venue_start_date"], dayfirst=True, 
                     date_parser=lambda x: pd.to_datetime(x, format="%d-%m-%Y %H:%M", errors='coerce'))
    df["venue_id"] = df["venue_id"].astype(str)
    df = df.dropna(subset=["venue_start_date"])  # Remove rows with invalid or missing dates
    return df



def generate_date_range(start_date, end_date):
    """Generate a list of dates from start_date to end_date."""
    if pd.isna(start_date):
        return []
    return [(start_date + timedelta(days=i)).strftime("%d-%m-%Y")
            for i in range((end_date - start_date).days + 1)]



def check_venue_data(venue_id, start_date, root_path):
    """Check if the expected date folders exist for a given venue."""
    venue_path = os.path.join(root_path, venue_id)

    if not os.path.exists(venue_path):
        return {"missing_venue_folder": True, "missing_dates": []}

    existing_date_folders = set(os.listdir(venue_path))
    expected_dates = generate_date_range(start_date, END_DATE)

    missing_dates = [date for date in expected_dates if date not in existing_date_folders]
    return {"missing_venue_folder": False, "missing_dates": missing_dates}


def audit_injested_data(venue_df, root_path):
    """Check all venues and collect missing data info."""
    report_rows = []

    for _, row in venue_df.iterrows():
        venue_id = row["venue_id"]
        start_date = row["venue_start_date"]
        result = check_venue_data(venue_id, start_date, root_path)

        if result["missing_venue_folder"]:
            report_rows.append({
                "venue_id": venue_id,
                "missing_venue_folder": True,
                "missing_dates": ""
            })
        else:
            report_rows.append({
                "venue_id": venue_id,
                "missing_venue_folder": False,
                "missing_dates": ", ".join(result["missing_dates"]) if result["missing_dates"] else "None"
            })

    return pd.DataFrame(report_rows)


def save_report_to_csv(df_report, output_path):
    """Save the final report to CSV."""
    df_report.to_csv(output_path, index=False)
    print(f"Report saved to: {output_path}")


def main():
    venue_df = read_venue_data(CSV_FILE_PATH)
    report_df = audit_injested_data(venue_df, INJESTED_DATA_ROOT)
    save_report_to_csv(report_df, REPORT_OUTPUT_PATH)


if __name__ == "__main__":
    main()
