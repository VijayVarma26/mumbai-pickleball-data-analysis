import os
import pandas as pd

def get_csv_files(input_folder):
    """Collect all CSV files in the folder."""
    return [f for f in os.listdir(input_folder) if f.endswith('.csv')]

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

def main():
    input_folder = os.path.dirname(__file__)  # Current folder
    output_file = r'C:\Project\New folder\Pickleball\data\raw_data\injested_data\960306\2025-03-30\2025-03-03.csv'
    
    csv_files = get_csv_files(input_folder)
    dataframes = read_csv_files(input_folder, csv_files)
    combined_df = combine_dataframes(dataframes)
    save_combined_dataframe(combined_df, output_file)

if __name__ == "__main__":
    main()