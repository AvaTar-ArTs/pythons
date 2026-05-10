import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
"""
Summary of sort.py

This module is part of the AVATARARTS ecosystem.
For more information about the AVATARARTS project, see the main documentation.
"""

import csv

# Define the input and output file paths
input_csv = "/Users/steven/Pictures/DaLL-E/dalle.csv"
output_csv = "/Users/steven/Pictures/DaLL-E/sorted_dalle.csv"


# Function to parse the input CSV and extract URL and INFO
def parse_csv(input_path):
    with open(input_path, mode="r", newline="", encoding="utf-8") as infile:
        reader = csv.reader(infile)
        next(reader)  # Skip the header row if there is one

        # Collect the data from the input file
        data = []
        for row in reader:
            # Concatenate the URL and INFO if they are split into different rows
            row_data = " ".join(row)
            parts = row_data.split("https://")
            for part in parts:
                if part.strip():
                    url = "https://" + part.split()[0]
                    info = " ".join(part.split()[1:])
                    data.append([url, info])
    return data


# Sort the data based on the URL
def sort_data(data):
    return sorted(data, key=lambda x: x[0])


# Write the sorted data to the output CSV file
def write_csv(data, output_path):
    with open(output_path, mode="w", newline="", encoding="utf-8") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(["URL", "INFO"])  # Write the header row
        writer.writerows(data)


# Main function to process the CSV
def main():
    data = parse_csv(input_csv)
    sorted_data = sort_data(data)
    write_csv(sorted_data, output_csv)
    print(f"Data sorted and saved to {output_csv}")


try:
        main()
except KeyboardInterrupt:
    logger.info("Execution interrupted by user")
    sys.exit(1)
except Exception as e:
    logger.error(f"An error occurred: {e}", exc_info=True)
    sys.exit(1)