from pathlib import Path
import pandas as pd

import logging

logger = logging.getLogger(__name__)


# Load the CSV file
file_path = Path(str(Path.home()) + "/Pictures/DALLe/pic.csv")  # Replace with your file path
df = pd.read_csv(file_path)

# Extract URLs (assuming they start with "http")
urls = df[df.iloc[:, 0].str.startswith("http")]

# Extract info (assuming they don't start with "http")
info = df[~df.iloc[:, 0].str.startswith("http")]

# Resetting indices
urls.reset_index(drop=True, inplace=True)
info.reset_index(drop=True, inplace=True)

# Combine into a new dataframe
result_df = pd.DataFrame({"URL": urls.iloc[:, 0], "Info": info.iloc[:, 0]})

# Save to CSV
# Replace with your desired output path
output_path = Path(str(Path.home()) + "/Pictures/DALLe/output.csv")
result_df.to_csv(output_path, index=False)

logger.info(f"Ordered CSV file saved to {output_path}")
