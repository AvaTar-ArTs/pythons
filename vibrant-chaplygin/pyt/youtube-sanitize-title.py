from pathlib import Path

import pandas as pd
import requests

import logging

logger = logging.getLogger(__name__)


# Other necessary code ...


# Function to sanitize the title
def sanitize_title(title):
    """sanitize_title function."""

    return title.replace(" ", "_").replace("/", "_").replace("|", "").replace(",", "")


# Read the original CSV file
csv_file = Path(str(Path.home()) + "/Downloads/NeAt/Misc/reformatted_mydesigns - Sheet1.csv")
df = pd.read_csv(csv_file)

# Directory where images will be downloaded
base_dir = Path(Path(str(Path.home()) + "/csv2/"))
base_dir.mkdir(exist_ok=True)

# Process each row in the DataFrame
for index, row in df.iterrows():
    title = sanitize_title(row["TITLE"])
    product_dir = base_dir / title
    product_dir.mkdir(exist_ok=True)

    # Download images and update the DataFrame with new paths
    for i in range(1, 11):
        image_col_name = f"IMAGE{i}"
        if image_col_name in row and pd.notna(row[image_col_name]):
            url = row[image_col_name]
            try:
                response = requests.get(url)
                response.raise_for_status()

                # Save the image to the new path
                filename = f"{title}_{i}.jpg"
                file_path = product_dir / filename
                with open(file_path, "wb") as file:
                    file.write(response.content)
                logger.info(f"Downloaded {filename}")

                # Update the DataFrame with the new path
                df.at[index, image_col_name] = str(file_path)

            except requests.RequestException as e:
                logger.info(f"Error downloading {url}: {e}")

# Save the updated DataFrame to a new Excel file
updated_excel_path = base_dir / "updated_image_paths.xlsx"
df.to_excel(updated_excel_path, index=False, engine="openpyxl")
logger.info(f"Updated Excel file saved to {updated_excel_path}")
