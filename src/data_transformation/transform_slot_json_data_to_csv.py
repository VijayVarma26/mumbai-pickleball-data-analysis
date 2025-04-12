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
    df = df.drop(columns=['is_empty', 'id', 'facility_id', 'has_linked_facilities', 'created_at', 'updated_at'])
    # Rearrange columns in the desired order
    column_order = ['assigned_venue_id', 'assigned_court_id', 'facility_name', 'facility_uuid', 'date', 'start_time',
                    'end_time', 'price', 'total_count', 'available_count', 'is_available', 'is_booked']
    df = df[column_order]
    # Extract only the time part from the 'start_time' and 'end_time' columns
    df['start_time'] = pd.to_datetime(df['start_time']).dt.time
    df['end_time'] = pd.to_datetime(df['end_time']).dt.time
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


def main():
    # Define the directory containing JSON files
    directory_path = r'C:\Project\New folder\Pickleball\data\raw_data\injested_data'

    # Get all JSON files in the directory
    json_files = get_all_json_files(directory_path)

    for json_file in json_files:
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


if __name__ == "__main__":
    main()