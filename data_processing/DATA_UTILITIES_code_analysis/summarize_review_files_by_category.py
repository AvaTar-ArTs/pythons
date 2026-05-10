import glob
import os

import pandas as pd


def get_latest_analysis_file(pythons_dir):
    """Find the most recent _all_scripts_analysis_*.csv file."""
    list_of_files = glob.glob(os.path.join(pythons_dir, "_all_scripts_analysis_*.csv"))
    if not list_of_files:
        return None
    return max(list_of_files, key=os.path.getctime)


def summarize_review_files_by_category():
    '\''Summarizes files marked for 'REVIEW' by their category.'\''

    pythons_dir = "/Users/steven/pythons"
    analysis_csv = get_latest_analysis_file(pythons_dir)

    if not analysis_csv:
        print("Error: Could not find the analysis CSV file.")
        return

    print(f"Reading analysis from: {os.path.basename(analysis_csv)}...")

    try:
        df_analysis = pd.read_csv(analysis_csv)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    review_df = df_analysis[df_analysis["action"] == "REVIEW"]

    if review_df.empty:
        print("No files marked for 'REVIEW' were found.")
        return

    category_summary = (
        review_df.groupby("category")
        .agg(file_count=("current_name", "count"))
        .reset_index()
        .sort_values(by="file_count", ascending=False)
    )

    print("\n--- Summary of Files Marked for 'REVIEW' by Category ---")
    print(f"Total files marked for 'REVIEW': {len(review_df)}\n")
    print(category_summary.to_string(index=False))


if __name__ == "__main__":
    summarize_review_files_by_category()
