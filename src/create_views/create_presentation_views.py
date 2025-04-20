import pandas as pd

# Define the file path
file_path = r'C:\Project\New folder\Pickleball\data\transformed_data\slot_data\final_slot_data.csv'


# Read the CSV file
def read_csv_file(file_path):
    """Read a CSV file and return a DataFrame."""
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except pd.errors.EmptyDataError:
        print(f"No data in file: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def group_by_venue_and_date(df):
    """Group the DataFrame by venue_id and date, and aggregate the data."""
    try:
        df['date'] = pd.to_datetime(df['date']).dt.date  # Convert to date only
        grouped_df = df.groupby(['assigned_venue_id', 'date']).agg(
            total_slots=('total_slot_count', 'sum'),
            booked_slots=('booked_slot_count', 'sum')
        ).reset_index()
        return grouped_df
    except Exception as e:
        print(f"An error occurred while grouping: {e}")

def main():
    # Read the CSV file
    df = read_csv_file(file_path)
    if df is not None:
        # Group the DataFrame by venue_id and date
        grouped_df = group_by_venue_and_date(df)
        if grouped_df is not None:
            # Save the grouped DataFrame to a new CSV file
            output_file_path = r'C:\Project\New folder\Pickleball\data\presentation_data\grouped_by_venue_and_date.csv'
            grouped_df.to_csv(output_file_path, index=False)
            print(f"Grouped data saved to {output_file_path}")
            
main()            