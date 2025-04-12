import pandas as pd
import json
import os

# Define the input JSON file path
input_json_path = r'C:\Project\New folder\Pickleball\data\raw_data\injested_data\180016\2025-01-30\101.json'

# Define the output CSV file path
output_csv_path = r'C:\Project\New folder\Pickleball\data\raw_data\injested_data\180016\2025-01-30\101.csv'

# Extract assigned_venue_id and assigned_court_id from the file path
assigned_venue_id = os.path.basename(os.path.dirname(os.path.dirname(input_json_path)))
assigned_court_id = os.path.splitext(os.path.basename(input_json_path))[0]

# Load the JSON data
with open(input_json_path, 'r') as json_file:
    data = json.load(json_file)

# Extract the 'slot_data' list from the JSON data
slot_data = data['data']['slot_data']

# Flatten the nested 'slots' list within each slot_data entry
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

# Convert the flattened data to a pandas DataFrame
df = pd.DataFrame(flattened_data)

# drop extra columns
df = df.drop(columns=[ 'is_empty', 'id', 'facility_id', 'has_linked_facilities', 'created_at', 'updated_at'])

# Rearrange columns in the desired order
column_order = ['assigned_venue_id', 'assigned_court_id', 'facility_name', 'facility_uuid', 'date', 'start_time', 'end_time', 'price', 'total_count', 'available_count','is_available', 'is_booked']
df = df[column_order]

# Extract only the time part from the 'start_time' and 'end_time' columns
df['start_time'] = pd.to_datetime(df['start_time']).dt.time
df['end_time'] = pd.to_datetime(df['end_time']).dt.time


os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
df.to_csv(output_csv_path, index=False)

print(f"Data successfully transformed and saved to {output_csv_path}")