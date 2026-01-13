import csv
import os
import shutil


def copy_files_with_structure(csv_file_path, destination_base_path):
    with open(csv_file_path, "r") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            original_path = row["Original Path"]
            destination_path = os.path.join(
                destination_base_path, original_path.lstrip(os.sep)
            )

            # Create the destination directory if it doesn't exist
            destination_dir = os.path.dirname(destination_path)
            if not os.path.exists(destination_dir):
                os.makedirs(destination_dir)

            # Copy the file to the destination
            shutil.copy2(original_path, destination_path)
            print(f"Copied {original_path} to {destination_path}")


if __name__ == "__main__":
    csv_file_path = "/Users/steven/Documents/Python/clean/docs-07-15-20:42.csv"
    destination_base_path = "/Volumes/oG-bAk/organized/steven"

    copy_files_with_structure(csv_file_path, destination_base_path)
    print("All files have been copied successfully.")
