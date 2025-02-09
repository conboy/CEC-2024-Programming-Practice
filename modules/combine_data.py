import os
import pandas as pd

def combine_data(dataset_folder, output_file):
    """
    This function combines all the data from the CSV files in the dataset folder into a CSV specified at output_file.
    It also returns the combined data as a pandas DataFrame.
    Each CSV file in the dataset_folder must contain a 100x100 grid of values with columns 'x', 'y', and 'value'.
    Also, the CSV file names must end with '_array_data.csv'.
    """
    # Get list of all CSV files in the dataset folder
    csv_files = [f for f in os.listdir(dataset_folder) if f.endswith('_array_data.csv')]

    # Initialize an empty dataframe to store the combined data
    combined_df = pd.DataFrame()

    # Loop through each CSV file and merge the data
    for csv_file in csv_files:
        file_path = os.path.join(dataset_folder, csv_file)
        material_name = csv_file.replace('_array_data.csv', '')
        df = pd.read_csv(file_path)
        df.rename(columns={'value': f'{material_name}'}, inplace=True)

        if combined_df.empty:
            combined_df = df
        else:
            combined_df = pd.merge(combined_df, df, on=['x', 'y'], how='outer')
            # Take the absolute value of all numerical columns
            combined_df = combined_df.abs()

    # Save the combined dataframe to a new CSV file
    combined_df.to_csv(output_file, index=False)

    return combined_df