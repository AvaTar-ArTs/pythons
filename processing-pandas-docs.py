"""
Data Processing Pandas Docs 10

This module provides functionality for data processing pandas docs 10.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import os
import pandas as pd
from pandas.errors import EmptyDataError

import logging

logger = logging.getLogger(__name__)


def combine_csvs():
    """
    Reads multiple CSV files from specified paths, concatenates them, and
    saves the result as 'all_combined.csv' (or whatever you name it).
    Handles empty or missing files gracefully.
    """

    # List of CSV file paths
    CSV_PATHS = [
        Path(str(Path.home()) + "/clean/clean-csv/combined_csv.csv"),
        Path(str(Path.home()) + "/clean/clean-csv/docs-03-28-18-52.csv"),
        Path(str(Path.home()) + "/clean/clean-csv/docs-03-28-18-57.csv"),
        Path(str(Path.home()) + "/clean/clean-csv/docs-03-29-06-11.csv"),
        Path(str(Path.home()) + "/clean/clean-csv/docs-03-29-11-47.csv"),
        Path(str(Path.home()) + "/clean/clean-csv/docs-03-29-17_49_1.csv"),
        Path(str(Path.home()) + "/clean/clean-csv/docs-03-29-17_49.csv"),
        Path(str(Path.home()) + "/clean/clean-csv/docs-03-29-17-49.csv"),
        Path(str(Path.home()) + "/clean/clean-csv/python-newcho.csv"),
    ]

    dfs = []
    for path in CSV_PATHS:
        if not os.path.exists(path):
            logger.info(f"[WARNING] File not found, skipping: {path}")
            continue

        # Check for 0-byte file
        if os.path.getsize(path) == 0:
            logger.info(f"[WARNING] Empty file, skipping: {path}")
            continue

        try:
            logger.info(f"[INFO] Reading CSV: {path}")
            df = pd.read_csv(path)
            dfs.append(df)
        except EmptyDataError:
            # This means the file is not truly zero-byte but has no columns or invalid CSV format
            logger.info(f"[WARNING] {path} is empty or invalid CSV. Skipping.")
        except Exception as e:
            logger.info(f"[ERROR] Could not read {path}: {e}")

    if not dfs:
        logger.info("[ERROR] No valid CSV files found. Exiting.")
        return

    # Concatenate into one DataFrame
    df_combined = pd.concat(dfs, ignore_index=True)

    # Optionally drop duplicates if you want each row to appear only once
    df_combined.drop_duplicates(inplace=True)

    # Save to a new CSV (or overwrite an existing one)
    output_path = Path(str(Path.home()) + "/clean/clean-csv/all_combined.csv")
    df_combined.to_csv(output_path, index=False)

    logger.info(
        f"\n[SUCCESS] Saved combined CSV with shape {df_combined.shape} to {output_path}!"
    )


if __name__ == "__main__":
    combine_csvs()
