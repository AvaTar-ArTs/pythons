"""
Summary of dblsort_from_ai-text-generator.py

This module is part of the AVATARARTS ecosystem.
For more information about the AVATARARTS project, see the main documentation.
"""

import pandas as pd

# Load the CSV file
file_path = "/Users/steven/pythons/fdupes/detailed_duplicate_report.csv"
duplicate_report = pd.read_csv(file_path)

# Sort by Duplicate Count in descending order
sorted_by_duplicates = duplicate_report.sort_values(
    by="Duplicate Count", ascending=False
)

# Filter to show only duplicates (where Duplicate Count > 1)
only_duplicates = sorted_by_duplicates[sorted_by_duplicates["Duplicate Count"] > 1]

# Sort by File Size (assuming sizes are in KB and removing the KB text for sorting)
duplicate_report["File Size"] = (
    duplicate_report["File Size"].str.replace(" KB", "").astype(float)
)
sorted_by_size = duplicate_report.sort_values(by="File Size", ascending=False)

# Display the sorted and filtered dataframes to the user
import ace_tools as tools

tools.display_dataframe_to_user(
    name="Sorted by Duplicate Count", dataframe=sorted_by_duplicates
)
tools.display_dataframe_to_user(name="Only Duplicates", dataframe=only_duplicates)
tools.display_dataframe_to_user(name="Sorted by File Size", dataframe=sorted_by_size)

sorted_by_duplicates.head(), only_duplicates.head(), sorted_by_size.head()
