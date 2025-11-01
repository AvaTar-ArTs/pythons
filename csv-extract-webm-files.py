"""
Utilities Misc Extract 22

This module provides functionality for utilities misc extract 22.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import pandas as pd

import logging

logger = logging.getLogger(__name__)


# Path to your input CSV file
csv_path = str(Path.home()) + "/vids-12-05-00:16.csv"

# Output paths for the new CSV and TXT files
output_csv = Path(str(Path.home()) + "/webm_files.csv")
output_txt = Path(str(Path.home()) + "/webm_files.txt")

# Load the CSV file
data = pd.read_csv(csv_path)

# Filter rows where the file path ends with `.webm`
webm_files = data[data["Original Path"].str.endswith(".webm", na=False)]

# Save to a new CSV file
webm_files[["Original Path"]].to_csv(output_csv, index=False)

# Save to a TXT file
webm_files["Original Path"].to_csv(output_txt, index=False, header=False)

logger.info(f"WebM file paths saved to:\n- CSV: {output_csv}\n- TXT: {output_txt}")
