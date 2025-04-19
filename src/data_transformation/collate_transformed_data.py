import os
import pandas as pd

def get_csv_files(input_folder):
    """Recursively collect all CSV files in the folder and its subfolders, ignoring files with 'combined' in the name."""
    csv_files = []
    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.endswith('.csv') and 'combined' not in file:
                csv_files.append(os.path.join(root, file))
    return csv_files

def read_csv_files(input_folder, csv_files):
    """Read each CSV file and return a list of dataframes."""
    dataframes = []
    for csv_file in csv_files:
        file_path = os.path.join(input_folder, csv_file)
        df = pd.read_csv(file_path)
        dataframes.append(df)
    return dataframes

def combine_dataframes(dataframes):
    """Concatenate all dataframes into a single dataframe."""
    return pd.concat(dataframes, ignore_index=True)

def save_combined_dataframe(combined_df, output_file):
    """Save the combined dataframe to the output file."""
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    combined_df.to_csv(output_file, index=False)
    print(f"Combined CSV file saved to: {output_file}")

def get_output_file_name(input_folder):
    """Generate the output file name based on the input folder."""
    folder_name = os.path.basename(input_folder)
    return f"{folder_name}_combined.csv"

def get_all_venue_ids(venue_data_file):
    """Extract all court IDs from the venue data file."""
    df = pd.read_csv(venue_data_file)
    return df['venue_id'].unique().tolist()

def delete_all_files_in_folder(folder_path):
    """Delete all files in the specified folder."""
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            os.remove(file_path)
    print(f"All files in {folder_path} have been deleted.")

def collate_transformed_data_by_venue_id(venue_id):
    input_folder = r'C:\Project\New folder\Pickleball\data\raw_data\injested_data\\' + str(venue_id)
    output_folder = r'C:\Project\New folder\Pickleball\data\transformed_data\slot_data'
    output_file_name = f"{venue_id}_data.csv"
    output_file = os.path.join(output_folder, output_file_name)

    csv_files = get_csv_files(input_folder)
    dataframes = read_csv_files(input_folder, csv_files)
    combined_df = combine_dataframes(dataframes)
    save_combined_dataframe(combined_df, output_file)

def collate_all_venue_slot_data():
    input_folder = r'C:\Project\New folder\Pickleball\data\transformed_data\slot_data'
    output_file = os.path.join(input_folder, 'final_slot_data.csv')

    csv_files = get_csv_files(input_folder)
    dataframes = read_csv_files(input_folder, csv_files)
    combined_df = combine_dataframes(dataframes)
    save_combined_dataframe(combined_df, output_file)


def main():
    # Delete all files in the transformed_data folder before collating new data
    delete_all_files_in_folder(r'C:\Project\New folder\Pickleball\data\transformed_data\slot_data')
    
    venue_id_list = get_all_venue_ids(r'C:\Project\New folder\Pickleball\data\raw_data\venue_data\hudle_venues_data.csv')

    for venue_id in venue_id_list:
        collate_transformed_data_by_venue_id(venue_id)
    print("Created combined.csv files in for each venue.")

    collate_all_venue_slot_data()
    print("Created final_slot_data.csv file in the slot_data folder.")
    
if __name__ == "__main__":
    main()