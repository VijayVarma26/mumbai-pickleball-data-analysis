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

def get_output_file_name(input_folder):
    """Generate the output file name based on the input folder."""
    folder_name = os.path.basename(input_folder)
    return f"{folder_name}_combined.csv"

def main():
    input_folder = r'C:\Project\New folder\Pickleball\data\raw_data\injested_data\987643\2025-01-29'
    output_file_name = get_output_file_name(input_folder)
    output_file = os.path.join(input_folder, output_file_name)

    csv_files = get_csv_files(input_folder)
    dataframes = read_csv_files(input_folder, csv_files)
    combined_df = combine_dataframes(dataframes)
    save_combined_dataframe(combined_df, output_file)

if __name__ == "__main__":
    main()