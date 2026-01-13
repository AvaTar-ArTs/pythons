from pathlib import Path
import pandas as pd

import logging

logger = logging.getLogger(__name__)


def load_excel(file_path):
    """load_excel function."""

    try:
        df = pd.read_excel(file_path)
        logger.info("Excel file loaded successfully.")
        return df
    except Exception as e:
        logger.info(f"Error loading Excel file: {e}")
        return None

    """check_missing_data function."""


def check_missing_data(df):
    if df is not None:
        logger.info("Missing data in each column:")
        logger.info(df.isnull().sum())
    else:
        logger.info("DataFrame is empty or not loaded.")


if __name__ == "__main__":
    file_path = Path(str(Path.home()) + "/Downloads/Document/Ytube.xlsx")
    df = load_excel(file_path)
    if df is not None:
        check_missing_data(df)
