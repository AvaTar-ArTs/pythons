import pandas as pd
import os
import shutil

def move_dr_adu_duplicates(csv_file, destination_folder):
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print(f"Error: The file {csv_file} was not found.")
        return

    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
        print(f"Created destination folder: {destination_folder}")

    dr_adu_df = df[df['file_path'].str.contains("Dr_Adu", na=False)]
    
    if dr_adu_df.empty:
        print("No duplicate files related to 'Dr_Adu' found to move.")
        return

    print(f"Moving {len(dr_adu_df)} 'Dr. Adu' duplicate files to {destination_folder}...")

    for index, row in dr_adu_df.iterrows():
        original_path = row['file_path']
        set_id = row['set_id']
        
        if not os.path.exists(original_path):
            print(f"Warning: Source file not found, skipping: {original_path}")
            continue

        base_name = os.path.basename(original_path)
        name, ext = os.path.splitext(base_name)
        
        # Create a unique name to avoid conflicts
        new_name = f"{name}_set_{set_id}_copy_{index}{ext}"
        destination_path = os.path.join(destination_folder, new_name)
        
        try:
            shutil.move(original_path, destination_path)
            print(f"Moved: {original_path} -> {destination_path}")
        except Exception as e:
            print(f"Error moving {original_path}: {e}")

if __name__ == '__main__':
    destination = '/Users/steven/documents/DrAdu'
    move_dr_adu_duplicates('/Users/steven/duplicates.csv', destination)
