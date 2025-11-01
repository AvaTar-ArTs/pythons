import pandas as pd

import logging

logger = logging.getLogger(__name__)


def read_csv():
    # Prompt the user for the path to the CSV file
    file_path = input("Enter the path to the CSV file: ")
    # Load the CSV data
    data = pd.read_csv(file_path, header=None, names=['date', 'url'])
    return data

# Test the function
data = read_csv()
logger.info(data.head())  # Print the first 5 rows to check the data
/Users/steven/Pictures/mid-date/3/march.csv   