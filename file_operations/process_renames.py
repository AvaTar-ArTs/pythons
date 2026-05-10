import csv
import os
import re


def clean_filename(title, duration_seconds):
    """Cleans the title and appends duration in MMSS format.
    Rules: No spaces, no hyphens (use underscores), and always append duration in MMSS format.
    """
    cleaned_title = re.sub(
        r"[ -]+",
        "_",
        title,
    )  # Replace spaces and hyphens with underscores
    cleaned_title = re.sub(
        r"[^a-zA-Z0-9_]",
        "",
        cleaned_title,
    )  # Remove special characters except underscores

    # Convert duration to MMSS format
    minutes = int(duration_seconds // 60)
    seconds = int(duration_seconds % 60)
    duration_mmss = f"{minutes:02d}{seconds:02d}"

    return f"{cleaned_title}{duration_mmss}.mp3"


def process_inventory_report(report_path):
    renames = []
    with open(report_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["Status"] == "in_library":
                found_path = row["Found Path"]
                if not found_path:  # Skip if Found Path is empty
                    continue

                current_dir, current_filename = os.path.split(found_path)

                # Extracting title and duration based on how they appear in the CSV
                # The 'Proposed Filename' in the CSV itself needs to be validated against the convention
                # Let's use 'Current Title' and 'Duration (s)' to generate the ideal filename

                current_title = row["Current Title"]
                duration_s_str = row["Duration (s)"]

                # Handle cases where duration might be malformed or missing
                try:
                    duration_seconds = float(duration_s_str)
                except ValueError:
                    print(
                        f"Warning: Could not parse duration '{duration_s_str}' for '{current_title}'. Skipping rename for this entry.",
                    )
                    continue

                proposed_ideal_filename = clean_filename(
                    current_title,
                    duration_seconds,
                )

                if current_filename != proposed_ideal_filename:
                    old_filepath = found_path
                    new_filepath = os.path.join(current_dir, proposed_ideal_filename)
                    renames.append({"old": old_filepath, "new": new_filepath})
    return renames


if __name__ == "__main__":
    # The report file path was provided in the previous step's output
    report_file = "INVENTORY_REPORT_HOME_SCAN_20251128_221059.csv"

    # Ensure the temporary directory exists for the proposed_renames.txt
    temp_dir = "/Users/steven/.gemini/tmp/84a2a6cae9fce89dd173a4e3d25e7a960e9ffcee3772d3c4f015c7d009872d3d"
    os.makedirs(temp_dir, exist_ok=True)

    renames_to_perform = process_inventory_report(report_file)

    if renames_to_perform:
        print("Proposed renames:")
        for rename in renames_to_perform:
            print(f"  '{rename['old']}' -> '{rename['new']}'")

        # This script only proposes renames.
        # The actual renaming will be done in a subsequent step after user confirmation.
        # For now, let's write the renames to a file for later use.
        with open(
            os.path.join(temp_dir, "proposed_renames.txt"),
            "w",
            encoding="utf-8",
        ) as f:
            for rename in renames_to_perform:
                f.write(f"{rename['old']}|{rename['new']}\n")
        print(
            f"\n{len(renames_to_perform)} renames proposed and saved to proposed_renames.txt in the temporary directory.",
        )
    else:
        print("No renames needed based on the report.")
