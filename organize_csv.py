import pandas as pd

# --------------------------------------------------------------------------------
# 1) Read the CSV files
# --------------------------------------------------------------------------------

df_vids  = pd.read_csv("/Users/steven/clean/vids-03-29-17-53.csv")
df_other = pd.read_csv("/Users/steven/clean/other-03-29-17-52.csv")
df_img   = pd.read_csv("/Users/steven/clean/image_data-03-29-17-51.csv")
df_docs  = pd.read_csv("/Users/steven/clean/docs-03-29-17-49.csv")
df_audio = pd.read_csv("/Users/steven/clean/audio-03-29-17-49.csv")

# --------------------------------------------------------------------------------
# 2) Basic analysis: shapes, duplicates, and a few lines to see structure
# --------------------------------------------------------------------------------

def analyze_df(df, df_name):
    print(f"--- Analyzing {df_name} ---")
    print("Shape (rows, columns):", df.shape)
    print("Duplicated rows count:", df.duplicated().sum())
    print("Column Info:")
    df.info()
    print("Head (first few rows):")
    print(df.head(), "\n")

analyze_df(df_vids,  "Vids")
analyze_df(df_other, "Other")
analyze_df(df_img,   "Images")
analyze_df(df_docs,  "Docs")
analyze_df(df_audio, "Audio")

# --------------------------------------------------------------------------------
# 3) Deduplicate and sort
#    NOTE: Adjust your deduplication method and sorting columns to suit your data
# --------------------------------------------------------------------------------

# For each dataset, remove exact duplicates across ALL columns
df_vids_clean  = df_vids.drop_duplicates()
df_other_clean = df_other.drop_duplicates()
df_img_clean   = df_img.drop_duplicates()
df_docs_clean  = df_docs.drop_duplicates()
df_audio_clean = df_audio.drop_duplicates()

# Example sorting approach:
# For instance, let's assume we want to sort:
# - Videos by "Creation Date" then "Filename"
# - Others similarly, if those columns exist
# Make sure these columns actually exist in each DataFrame before sorting
sort_cols = ["Creation Date", "Filename"]

if set(sort_cols).issubset(df_vids_clean.columns):
    df_vids_clean = df_vids_clean.sort_values(by=sort_cols, ascending=True)

if set(sort_cols).issubset(df_other_clean.columns):
    df_other_clean = df_other_clean.sort_values(by=sort_cols, ascending=True)

if set(sort_cols).issubset(df_img_clean.columns):
    df_img_clean = df_img_clean.sort_values(by=sort_cols, ascending=True)

if set(sort_cols).issubset(df_docs_clean.columns):
    df_docs_clean = df_docs_clean.sort_values(by=sort_cols, ascending=True)

if set(sort_cols).issubset(df_audio_clean.columns):
    df_audio_clean = df_audio_clean.sort_values(by=sort_cols, ascending=True)

# --------------------------------------------------------------------------------
# 4) (Optional) Standardize or rename columns, convert data types, etc.
#    For example, lowercasing columns or renaming:
# --------------------------------------------------------------------------------

def standardize_columns(df):
    df.columns = (
        df.columns
        .str.strip()           # remove any leading/trailing whitespace
        .str.lower()           # convert all column names to lowercase
        .str.replace(' ', '_') # replace spaces with underscores
    )
    return df

df_vids_clean = standardize_columns(df_vids_clean)
df_other_clean = standardize_columns(df_other_clean)
df_img_clean = standardize_columns(df_img_clean)
df_docs_clean = standardize_columns(df_docs_clean)
df_audio_clean = standardize_columns(df_audio_clean)

# Example: rename columns if needed
# df_vids_clean.rename(columns={"file_size": "filesize_bytes"}, inplace=True)

# Convert creation_date to a datetime if it exists
for df_clean in [df_vids_clean, df_other_clean, df_img_clean, df_docs_clean, df_audio_clean]:
    if "creation_date" in df_clean.columns:
        df_clean["creation_date"] = pd.to_datetime(df_clean["creation_date"], errors="coerce")

# --------------------------------------------------------------------------------
# 5) Save the cleaned, organized results
# --------------------------------------------------------------------------------

df_vids_clean.to_csv("/Users/steven/clean/vids_cleaned.csv",  index=False)
df_other_clean.to_csv("/Users/steven/clean/other_cleaned.csv", index=False)
df_img_clean.to_csv("/Users/steven/clean/image_data_cleaned.csv", index=False)
df_docs_clean.to_csv("/Users/steven/clean/docs_cleaned.csv", index=False)
df_audio_clean.to_csv("/Users/steven/clean/audio_cleaned.csv", index=False)

print("Cleaning and organization complete!")
