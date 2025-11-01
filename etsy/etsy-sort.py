"""
Etsy Csv Sort

This module provides functionality for etsy csv sort.

Author: Auto-generated
Date: 2025-11-01
"""

import pandas as pd

import logging

logger = logging.getLogger(__name__)


def organize_etsy_csv():
    """organize_etsy_csv function."""

    # Prompt for file locations
    input_file_path = input("Enter the path to your input CSV file: ")
    output_file_path = input(
        "Enter the path to save the organized output CSV file (with .csv extension): "
    )

    # Read the input CSV file
    try:
        df = pd.read_csv(input_file_path)

        # Define expected columns and provide options to rename if needed
        required_columns = {
            "iD": "Listing URL",
            "Title": "Etsy Listing",
            "price": "price",
            "est_total_sales": "est_total_sales",
            "favorites": "favorites",
            "views": "views",
            "visibility_score": "visibility_score",
            "conversion_rate": "conversion_rate",
            "tags": "tags",
            "Title": "Title",
        }

        # Check for missing columns and prompt for alternatives
        for col, display_name in required_columns.items():
            if col not in df.columns:
                alternative_col = input(
                    f"Column '{col}' not found. Please provide an alternative column name for '{display_name}', or press Enter to skip: "
                )
                if alternative_col:
                    df[display_name] = df[alternative_col]
                else:
                    df[display_name] = None  # Create an empty column if not provided

        # Extract IDs from 'Listing URL' if available
        if "Listing URL" in df.columns:
            df["iD"] = df["Listing URL"].apply(
                lambda x: x.split("/")[-2] if pd.notnull(x) else None
            )

        # Organize into the desired structure
        organized_df = pd.DataFrame(
            {
                "iD": df["iD"],
                "Title": df["Title"],
                "Etsy Listing": df["Etsy Listing"],
                "Listing URL": df["Listing URL"],
                "tags": df["tags"],
                "price": df["price"],
                "est_total_sales": df["est_total_sales"],
                "favorites": df["favorites"],
                "views": df["views"],
                "visibility_score": df["visibility_score"],
                "conversion_rate": df["conversion_rate"],
            }
        )

        # Save the organized DataFrame to a new CSV file
        organized_df.to_csv(output_file_path, index=False)
        logger.info(f"Organized CSV has been saved to: {output_file_path}")

    except FileNotFoundError:
        logger.info(
            "The file path you provided does not exist. Please check and try again."
        )
    except Exception as e:
        logger.info(f"An error occurred: {e}")


# Run the function
organize_etsy_csv()
