"""
Summary of csv_to_db_importer.py

This module is part of the AVATARARTS ecosystem.
For more information about the AVATARARTS project, see the main documentation.
"""

import sqlite3
import csv
import os
import json
from datetime import datetime

DATABASE_NAME = os.path.expanduser("~/scan_database/scans.db")
TABLE_NAME = "scans_unified"

def create_table(cursor):
    """Creates the scans_unified table if it doesn't exist."""
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_path TEXT UNIQUE NOT NULL,
            file_name TEXT NOT NULL,
            main_category TEXT,
            scan_timestamp TEXT NOT NULL,
            source_csv_name TEXT NOT NULL,
            metadata JSON
        )
    """)

def get_file_mapping(csv_file_name):
    """
    Returns a dictionary mapping generic field names to specific CSV column names
    and determines the main_category based on the CSV file name.
    """
    mapping = {
        'file_path': None,
        'file_name': None,
        'main_category': 'general'
    }

    if "Ability_Preview" in csv_file_name and "LLM_Tools" in csv_file_name:
        mapping['file_path'] = 'Primary_Path'
        mapping['file_name'] = 'Tool_Name'
        mapping['main_category'] = 'ai_llm_tools'
    elif "steven-scan-audio" in csv_file_name:
        mapping['file_path'] = 'Original Path'
        mapping['file_name'] = 'Filename'
        mapping['main_category'] = 'audio_scan'
    elif "cleaned_python_inventory" in csv_file_name or "real_python_scripts" in csv_file_name:
        mapping['file_path'] = 'Path'
        mapping['file_name'] = 'Filename'
        mapping['main_category'] = 'python_scripts'
    elif "MASTER_BEFORE_AFTER_MIGRATION" in csv_file_name:
        mapping['file_path'] = 'Before_Path' # Using Before_Path as canonical, After_Path goes to metadata
        mapping['file_name'] = 'Filename'
        mapping['main_category'] = 'migration_report'
    elif "migration_mapping" in csv_file_name:
        mapping['file_path'] = 'CurrentPath'
        mapping['file_name'] = 'Filename'
        mapping['main_category'] = 'migration_map'
    elif "home-scan" in csv_file_name:
        mapping['file_path'] = 'path'
        mapping['file_name'] = 'name'
        mapping['main_category'] = 'general_scan'
    
    # Default fallback for file_path and file_name if not specifically mapped
    if mapping['file_path'] is None:
        if 'path' in csv_file_name: # Common column name for paths
             mapping['file_path'] = 'path'
        elif 'Path' in csv_file_name: # Common column name for paths
            mapping['file_path'] = 'Path'
        elif 'Primary_Path' in csv_file_name: # Common column name for paths
            mapping['file_path'] = 'Primary_Path'
        elif 'Original Path' in csv_file_name: # Common column name for paths
            mapping['file_path'] = 'Original Path'
        elif 'Before_Path' in csv_file_name: # Common column name for paths
            mapping['file_path'] = 'Before_Path'
        elif 'CurrentPath' in csv_file_name: # Common column name for paths
            mapping['file_path'] = 'CurrentPath'
        else: # Fallback to a generic 'path' if it exists or log a warning
            pass # We'll handle missing later

    if mapping['file_name'] is None:
        if 'name' in csv_file_name: # Common column name for names
            mapping['file_name'] = 'name'
        elif 'Filename' in csv_file_name: # Common column name for names
            mapping['file_name'] = 'Filename'
        elif 'Tool_Name' in csv_file_name: # Common column name for names
            mapping['file_name'] = 'Tool_Name'
        else: # Fallback to a generic 'name' if it exists or log a warning
            pass # We'll handle missing later


    return mapping


def import_csv_to_db(csv_file_path, db_path=DATABASE_NAME):
    """Imports data from a single CSV file into the SQLite database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    create_table(cursor)

    source_csv_name = os.path.basename(csv_file_path)
    current_scan_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    mapping = get_file_mapping(source_csv_name)
    file_path_col = mapping['file_path']
    file_name_col = mapping['file_name']
    main_category = mapping['main_category']

    print(f"Importing {source_csv_name} into category '{main_category}'...")

    try:
        with open(csv_file_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            # Verify critical columns are present
            if not file_path_col or file_path_col not in reader.fieldnames:
                print(f"Error: Required 'file_path' column '{file_path_col}' not found in {source_csv_name}. Skipping.")
                return
            if not file_name_col or file_name_col not in reader.fieldnames:
                print(f"Error: Required 'file_name' column '{file_name_col}' not found in {source_csv_name}. Skipping.")
                return

            for row in reader:
                try:
                    # Extract common fields
                    file_path_val = row.get(file_path_col)
                    file_name_val = row.get(file_name_col)

                    # Create metadata dictionary with all other columns
                    metadata = {k: v for k, v in row.items() if k not in [file_path_col, file_name_col]}
                    metadata_json = json.dumps(metadata)

                    if not file_path_val or not file_name_val:
                        print(f"Skipping row in {source_csv_name} due to missing critical 'file_path' or 'file_name'. Row: {row}")
                        continue

                    cursor.execute(f"""
                        INSERT OR REPLACE INTO {TABLE_NAME}
                        (file_path, file_name, main_category, scan_timestamp, source_csv_name, metadata)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (
                        file_path_val,
                        file_name_val,
                        main_category,
                        current_scan_timestamp,
                        source_csv_name,
                        metadata_json
                    ))
                except Exception as e:
                    print(f"An error occurred for row in {source_csv_name}: {e}. Row: {row}")

        conn.commit()
        print(f"Successfully imported {source_csv_name}.")
    except Exception as e:
        print(f"Error processing {csv_file_path}: {e}")
    finally:
        conn.close()

def main():
    csv_files = [
        "/Users/steven/Ability_Preview_AI_LLM_Tools.csv",
        "/Users/steven/Ability_Preview_Data_Analysis.csv",
        "/Users/steven/Ability_Preview_Database_Infrastructure.csv",
        "/Users/steven/Ability_Preview_Documentation_Tools.csv",
        "/Users/steven/Ability_Preview_General_Utilities.csv",
        "/Users/steven/Ability_Preview_Media_Processing.csv",
        "/Users/steven/Ability_Preview_Social_Media_Automation.csv",
        "/Users/steven/Ability_Preview_YouTube_Tools.csv",
        "/Users/steven/cleaned_python_inventory.csv",
        "/Users/steven/home-scan-2026-01-12.csv",
        "/Users/steven/MASTER_BEFORE_AFTER_MIGRATION.csv",
        "/Users/steven/migration_mapping.csv",
        "/Users/steven/real_python_scripts.csv",
        "/Users/steven/steven-scan-audio-2026-01-14.csv", # User provided these, so include them
        "/Users/steven/steven-scan-audio-2026-01-15.csv",
        "/Users/steven/steven-scan-audio-2026-01-17.csv"
    ]

    if not csv_files:
        print("No CSV files specified for import.")
        return

    for csv_file in csv_files:
        if os.path.exists(csv_file):
            import_csv_to_db(csv_file)
        else:
            print(f"Warning: CSV file not found: {csv_file}. Skipping.")

if __name__ == "__main__":
    main()