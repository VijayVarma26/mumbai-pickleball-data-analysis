import pandas as pd
import json
import os


def extract_ids_from_path(input_json_path):
    """Extract assigned_venue_id and assigned_court_id from the file path."""
    assigned_venue_id = os.path.basename(os.path.dirname(os.path.dirname(input_json_path)))
    assigned_court_id = os.path.splitext(os.path.basename(input_json_path))[0]
    return assigned_venue_id, assigned_court_id


def load_json_data(input_json_path):
    """Load JSON data from the given file path."""
    with open(input_json_path, 'r') as json_file:
        return json.load(json_file)


def flatten_slot_data(data, assigned_venue_id, assigned_court_id):
    """Flatten the nested 'slot_data' list within the JSON data."""
    slot_data = data['data']['slot_data']
    flattened_data = []
    for entry in slot_data:
        date = entry['date']
        is_empty = entry['is_empty']
        for slot in entry['slots']:
            slot['date'] = date
            slot['is_empty'] = is_empty
            slot['assigned_venue_id'] = assigned_venue_id
            slot['assigned_court_id'] = assigned_court_id
            flattened_data.append(slot)
    return flattened_data


def transform_to_dataframe(flattened_data):
    """Transform the flattened data into a pandas DataFrame."""
    df = pd.DataFrame(flattened_data)
    # Drop extra columns
    df = df.drop(columns=['is_empty', 'id', 'facility_id', 'has_linked_facilities', 'created_at', 'updated_at', 'facility_name', 'facility_uuid', 'is_available', 'is_booked'])
    
    
    # Rename columns
    df = df.rename(columns={'total_count': 'total_slot_count', 'available_count': 'available_slot_count', 'price': 'slot_price'})

    # Add a column for the booked slot count
    df['booked_slot_count'] = df['total_slot_count'] - df['available_slot_count']

    # Add a column for earnings from slot
    df['earnings'] = df['booked_slot_count'] * df['slot_price']
    
    # Add a column for the day of the week based on the 'date' column
    df['day_of_week'] = pd.to_datetime(df['date']).dt.strftime('%A')

    # Add a column for day category based on the day of the week
    df['day_category'] = df['day_of_week'].apply(lambda x: 'weekend' if x in ['Saturday', 'Sunday'] else 'weekday')


    # Add a column for slot category based on the 'start_time' column
    def categorize_slot(start_time):
        start_time = pd.to_datetime(start_time).time()  # Convert to datetime.time for comparison
        if pd.Timestamp('04:00:00').time() <= start_time <= pd.Timestamp('08:59:59').time():
            return 'Early Morning'
        elif pd.Timestamp('09:00:00').time() <= start_time <= pd.Timestamp('11:59:59').time():
            return 'Late Morning'
        elif pd.Timestamp('12:00:00').time() <= start_time <= pd.Timestamp('17:59:59').time():
            return 'Afternoon'
        elif pd.Timestamp('18:00:00').time() <= start_time <= pd.Timestamp('21:59:59').time():
            return 'Evening'
        elif pd.Timestamp('21:00:00').time() <= start_time <= pd.Timestamp('23:59:59').time() or pd.Timestamp('00:00:00').time() <= start_time < pd.Timestamp('03:59:59').time():
            return 'Late Night'
        else:
            return 'Other'

    df['slot_category'] = df['start_time'].apply(categorize_slot)

    # Extract only the time part from the 'start_time' and 'end_time' columns
    df['start_time'] = pd.to_datetime(df['start_time']).dt.time
    df['end_time'] = pd.to_datetime(df['end_time']).dt.time

    # Rearrange columns in the desired order
    column_order = ['assigned_venue_id', 'assigned_court_id', 'date', 'day_of_week', 'day_category','start_time','end_time', 'slot_category','slot_price', 'total_slot_count','booked_slot_count', 'available_slot_count', 'earnings']
    df = df[column_order]
    
    return df


def save_to_csv(df, output_csv_path):
    """Save the DataFrame to a CSV file."""
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
    df.to_csv(output_csv_path, index=False)


def get_all_json_files(directory_path):
    """Get the file paths of all JSON files in the given directory and its subdirectories."""
    json_files = []
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.json'):
                json_files.append(os.path.join(root, file))
    return json_files


def process_single_file(json_file):
    """Process a single JSON file and save the transformed data to a CSV file."""
    try:
        # Extract IDs from the file path
        assigned_venue_id, assigned_court_id = extract_ids_from_path(json_file)

        # Define the output CSV file path based on the JSON file path
        output_csv_path = os.path.splitext(json_file)[0] + '.csv'

        # Load the JSON data
        data = load_json_data(json_file)

        # Flatten the slot data
        flattened_data = flatten_slot_data(data, assigned_venue_id, assigned_court_id)

        # Transform the flattened data into a DataFrame
        df = transform_to_dataframe(flattened_data)

        # Save the DataFrame to a CSV file
        save_to_csv(df, output_csv_path)

        print(f"Data successfully transformed and saved to {output_csv_path}")
    except Exception as e:
        print(f"An error occurred while processing {json_file}: {e}")


def process_all_files(directory_path):
    """Process all JSON files in the given directory."""
    # Get all JSON files in the directory
    json_files = get_all_json_files(directory_path)

    for json_file in json_files:
        process_single_file(json_file)


def main():
    # Define the directory containing JSON files
    directory_path = r'C:\Project\New folder\Pickleball\data\raw_data\injested_data'

    # Process all JSON files in the directory
    process_all_files(directory_path)


if __name__ == "__main__":
    main()
    # process_single_file(r'C:\Project\New folder\Pickleball\data\raw_data\injested_data\960306\2025-01-29\102.json')