from pathlib import Path
import pandas as pd

import logging

logger = logging.getLogger(__name__)


# ------------------------------------------------------------------------------
# 1) Read the TWO old CSVs and COMBINE them into one DataFrame
# ------------------------------------------------------------------------------

OLD_CSV_1 = Path("/Users/steven/Documents/DeepSeek/docs-03-29-17_49.csv")
OLD_CSV_2 = Path("/Users/steven/clean/docs-03-29-17-49.csv")
OLD_CSV_3 =Path("/Users/steven/clean/clean-csv/docs-03-28-18-52.csv")
OLD_CSV_4 =Path("/Users/steven/clean/clean-csv/docs-03-28-18-57.csv")
OLD_CSV_5 =Path("/Users/steven/clean/clean-csv/docs-03-29-06-11.csv")
OLD_CSV_6 =Path("/Users/steven/clean/clean-csv/docs-03-29-11-47.csv")
OLD_CSV_7 =Path("/Users/steven/clean/clean-csv/docs-03-29-17_49_1.csv")
OLD_CSV_8 =Path("/Users/steven/clean/clean-csv/docs-03-29-17_49.csv")
OLD_CSV_9 =Path("/Users/steven/clean/clean-csv/docs-03-29-17-49.csv")
OLD_CSV_10 =Path("/Users/steven/clean/clean-csv/python-newcho.csv")

df_old_1 = pd.read_csv(OLD_CSV_1)
df_old_2 = pd.read_csv(OLD_CSV_2)

# Combine them (optionally drop duplicates, depending on your preference)
df_old_combined = pd.concat([df_old_1, df_old_2], ignore_index=True)
df_old_combined.drop_duplicates(inplace=True)

logger.info(f"Combined old CSV shape: {df_old_combined.shape}")

# ------------------------------------------------------------------------------
# 2) Read the NEW CSV
# ------------------------------------------------------------------------------

NEW_CSV = "OLD_CSV_==Path("/Users/steven/clean/docs_cleaned.csv")
df_new = pd.read_csv(NEW_CSV)

logger.info(f"New CSV shape: {df_new.shape}")

# ------------------------------------------------------------------------------
# 3) Merge the combined old DataFrame with the new DataFrame
#    Decide which columns serve as unique identifiers (keys) for matching rows.
#    Typically: ["Filename", "Original Path"] if they exist in both sets.
# ------------------------------------------------------------------------------

merge_cols = ["Filename", "Original Path"]

df_compare = pd.merge(
    df_old_combined, 
    df_new,
    on=merge_cols,
    how="outer",
    indicator=True,
    suffixes=("_old", "_new")
)

# ------------------------------------------------------------------------------
# 4) Identify rows that are:
#    - only in old ("Removed")
#    - only in new ("Added")
#    - in both (potentially "Modified")
# ------------------------------------------------------------------------------

rows_only_in_old = df_compare[df_compare["_merge"] == "left_only"].copy()
rows_only_in_new = df_compare[df_compare["_merge"] == "right_only"].copy()
rows_in_both     = df_compare[df_compare["_merge"] == "both"].copy()

logger.info("Rows only in OLD:", rows_only_in_old.shape[0])
logger.info("Rows only in NEW:", rows_only_in_new.shape[0])
logger.info("Rows in BOTH:    ", rows_in_both.shape[0])

# ------------------------------------------------------------------------------
# 5) Check for changes in certain columns among rows that appear in both
#    Adjust 'cols_to_check' to match columns that might differ between old vs new
# ------------------------------------------------------------------------------

cols_to_check = ["File Size", "Creation Date"]

# We'll create a mask that is True if any column among 'cols_to_check' differs.
changed_mask = False

for col in cols_to_check:
    old_col = col + "_old"
    new_col = col + "_new"
    # We'll create a new boolean column indicating difference in this column
    diff_col = f"{col.lower().replace(' ', '_')}_changed"
    rows_in_both[diff_col] = rows_in_both[old_col] != rows_in_both[new_col]
    changed_mask = changed_mask | rows_in_both[diff_col]

rows_changed_in_both = rows_in_both[changed_mask].copy()

logger.info("Rows in BOTH that have changed columns:", rows_changed_in_both.shape[0])

# ------------------------------------------------------------------------------
# 6) Export difference sets to separate CSVs
# ------------------------------------------------------------------------------

rows_only_in_old.to_csv("docs_removed.csv", index=False)
rows_only_in_new.to_csv("docs_added.csv", index=False)
rows_changed_in_both.to_csv("docs_modified.csv", index=False)

# ------------------------------------------------------------------------------
# 7) Optionally combine them into one difference summary CSV, with a 'DiffType' column
# ------------------------------------------------------------------------------

df_diff = pd.concat([
    rows_only_in_old.assign(DiffType="Removed"),
    rows_only_in_new.assign(DiffType="Added"),
    rows_changed_in_both.assign(DiffType="Modified")
], ignore_index=True)

df_diff.to_csv("docs_difference_summary.csv", index=False)

logger.info("All done! Differences exported as:")
logger.info("- docs_removed.csv        (only in old)")
logger.info("- docs_added.csv          (only in new)")
logger.info("- docs_modified.csv       (in both, but changed in specified columns)")
logger.info("- docs_difference_summary.csv (combined overview)")
