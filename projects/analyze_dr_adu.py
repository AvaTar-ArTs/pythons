import pandas as pd
import os

pd.set_option('display.max_colwidth', None)

def analyze_dr_adu_duplicates(csv_file):
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print(f"Error: The file {csv_file} was not found.")
        return

    if df.empty:
        print("The CSV file is empty. No duplicates to analyze.")
        return

    # Filter for files related to "Dr_Adu"
    dr_adu_df = df[df['file_path'].str.contains("Dr_Adu", na=False)]
    
    if dr_adu_df.empty:
        print("No duplicate files related to 'Dr_Adu' found.")
        return

    print("--- Analysis of 'Dr. Adu' Duplicate Sets ---")
    
    # Get up to 3 example sets
    example_sets = dr_adu_df['set_id'].unique()[:3]
    
    if len(example_sets) == 0:
        print("No complete sets found for 'Dr. Adu' to analyze as examples.")
        return

    print("Here are a few example sets of duplicates related to 'Dr. Adu'.")
    print("Please review each set and tell me which file you would like to keep.")
    
    for set_id in example_sets:
        print(f"\n--- Set ID: {set_id} ---")
        set_files = df[df['set_id'] == set_id]['file_path']
        # Add an index for easier selection by the user
        for i, file_path in enumerate(set_files):
            print(f"  {i+1}: {file_path}")

if __name__ == '__main__':
    analyze_dr_adu_duplicates('/Users/steven/duplicates.csv')
