from pathlib import Path
import csv
import json
import os

import logging

logger = logging.getLogger(__name__)


# Prompt for the JSON input file path with a default value
default_json_path = Path(str(Path.home()) + "/Downloads/AI_Workflow_Automation_Summary.json")
json_file_path = (
    input(f"Enter JSON file path (default: {default_json_path}): ") or default_json_path
)

# Validate that the JSON file exists
if not os.path.exists(json_file_path):
    logger.info(f"Error: The file {json_file_path} does not exist.")
    exit(1)

# Prompt for the CSV output file path with a default value
default_csv_path = Path(str(Path.home()) + "/Documents/output.csv")
csv_file_path = (
    input(f"Enter CSV output file path (default: {default_csv_path}): ")
    or default_csv_path
)

# Load JSON data
with open(json_file_path, "r", encoding="utf-8") as json_file:
    data = json.load(json_file)

# The JSON file is a list; assume the first element is your summary object.
summary = data[0]
mapping = summary.get("mapping", {})

# Prepare rows for CSV: one row per node in the mapping
rows = []
for node_id, node in mapping.items():
    parent = node.get("parent", "N/A")
    children = node.get("children", [])
    children_str = "; ".join(children) if children else ""

    message = node.get("message")
    if message:
        author_role = message.get("author", {}).get("role", "N/A")
        content_parts = message.get("content", {}).get("parts", [])
        # Convert each part to a string. If it's a dict, attempt to use its "text" field, otherwise convert it.
        content = " ".join(
            part if isinstance(part, str) else part.get("text", str(part))
            for part in content_parts
        ).strip()
        status = message.get("status", "N/A")
    else:
        author_role = "N/A"
        content = ""
        status = "N/A"

    rows.append([node_id, parent, children_str, author_role, content, status])

# Write the data to a CSV file
with open(csv_file_path, "w", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)
    # CSV header
    writer.writerow(
        ["Node ID", "Parent", "Children", "Author Role", "Content", "Status"]
    )
    # Write each row
    writer.writerows(rows)

logger.info(f"CSV file created at {csv_file_path}")
