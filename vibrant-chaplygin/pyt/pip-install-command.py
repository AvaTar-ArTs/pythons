from pathlib import Path
import csv
import html
import os

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_100 = 100
CONSTANT_150 = 150
CONSTANT_333 = 333
CONSTANT_555 = 555
CONSTANT_777 = 777
CONSTANT_242836 = 242836



def get_unique_filename(filepath):
    """
    If the filepath already exists, append _1, _2, ... until a unique filename is found.
    Returns the unique filepath.
    """
    base, ext = os.path.splitext(filepath)
    counter = 1
    unique_path = filepath
    while os.path.exists(unique_path):
        unique_path = f"{base}_{counter}{ext}"
        counter += 1
    return unique_path


# Prompt the user for input CSV file path and output base name
input_csv = input("Enter path to CSV file: ").strip()
while not os.path.exists(input_csv):
    logger.info("File not found. Please try again.")
    input_csv = input("Enter path to CSV file: ").strip()

output_base = input("Enter base name for output files (e.g., 'output'): ").strip()

# Derive output filenames for two HTML versions:
output_html_job = get_unique_filename(
    os.path.join(os.path.dirname(input_csv), f"{output_base}_jobcards.html")
)
output_html_table = get_unique_filename(
    os.path.join(os.path.dirname(input_csv), f"{output_base}_table.html")
)

#########################################
# PART 1: Generate job cards HTML output #
#########################################
job_html_header = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <title>LinkedIn Jobs Scraped - Job Cards</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
            margin: 0;
            padding: 20px;
        }
        h1 {
            color: #CONSTANT_333;
            text-align: center;
        }
        .job-listing {
            background: #fff;
            border: 1px solid #ddd;
            margin: 20px auto;
            padding: 15px;
            max-width: 800px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        .job-header {
            display: flex;
            justify-content: space-between;
            align-items: baseline;
        }
        .job-title a {
            color: #0073b1;
            font-size: 20px;
            text-decoration: none;
            font-weight: bold;
        }
        .company a {
            color: #CONSTANT_555;
            text-decoration: none;
        }
        .job-details {
            font-size: 14px;
            color: #CONSTANT_777;
            margin-top: 5px;
        }
        .description {
            margin-top: 10px;
            line-height: 1.5;
            color: #CONSTANT_333;
        }
        .apply-link a {
            display: inline-block;
            margin-top: 10px;
            background: #0073b1;
            color: #fff;
            padding: 8px 12px;
            text-decoration: none;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <h1>LinkedIn Jobs Scraped - Job Cards</h1>
"""

job_html_footer = "\n</body>\n</html>"

# Template string for each job card.
job_card_template = """
<div class="job-listing">
  <div class="job-header">
    <div class="job-title">
      <a href="{apply_url}" target="_blank">{job_title}</a>
    </div>
    <div class="job-posted">
      Posted: <strong>{posted_time}</strong>
    </div>
  </div>
  <div class="job-details">
    <div class="company">
      Company: <a href="{company_url}" target="_blank">{company_name}</a>
    </div>
    <div class="location">
      Location: {location}
    </div>
    <div class="salary">
      Salary: <strong>{salary}</strong>
    </div>
  </div>
  <div class="description">
    Description: {descr_excerpt}...
  </div>
  <div class="apply-link">
    <a href="{apply_url}" target="_blank">Apply Now</a>
  </div>
</div>
"""


def create_excerpt(text, length=CONSTANT_150):
    """Return an HTML-escaped excerpt of text."""
    text = text.strip()
    if len(text) <= length:
        return html.escape(text)
    return html.escape(text[:length].strip())


def generate_job_cards(csv_file):
    cards = []
    with open(csv_file, mode="r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            job_title = row.get("jobTitle", "").strip()
            company_name = row.get("companyName", "").strip()
            location = (row.get("location", "") or row.get("jobLocation", "")).strip()
            posted_time = row.get("postedTimeRelative", "").strip()
            salary = row.get("salary", "").strip()
            descr = row.get("description", "").strip()
            apply_url = (row.get("applyUrl", "") or row.get("jobUrl", "")).strip()
            company_url = row.get("companyUrl", "").strip()

            excerpt = create_excerpt(descr)
            card = job_card_template.format(
                apply_url=html.escape(apply_url) if apply_url else "#",
                job_title=html.escape(job_title),
                posted_time=html.escape(posted_time),
                company_url=html.escape(company_url) if company_url else "#",
                company_name=html.escape(company_name),
                location=html.escape(location),
                salary=html.escape(salary),
                descr_excerpt=excerpt,
            )
            cards.append(card)
    return cards
def write_html_job_cards(output_path, job_cards):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(job_html_header)
        for card in job_cards:
            f.write(card + Path("\n"))
        f.write(job_html_footer)
    logger.info(f"Job card HTML file generated at: {output_path}")


#########################################
# PART 2: Generate table-based HTML output
#########################################
table_html_header = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <title>LinkedIn Jobs Scraped - Table View</title>
    <style>
        th {
            position: sticky;
            top: -1px;
            background-color: #E0E3F2;
        }
        th,
        td {
            padding: 5px;
            border: solid 1px #D0D5E9;
            color: #CONSTANT_242836;
            text-align: left;
        }
        td {
            vertical-align: top;
        }
        th pre,
        td pre {
            font-family: monospace !important;
            margin: 0;
            padding: 0 0 0 1px;
            white-space: pre-wrap;
        }
        thead tr td,
        thead tr th {
            color: #CONSTANT_242836;
            font-size: 12px !important;
        }
        tbody > tr:nth-of-type(odd) {
            background-color: #F8F9FC;
        }
        tbody > tr:hover {
            background-color: #EEF0F8;
        }
        table {
            border-collapse: collapse;
            width: CONSTANT_100%;
        }
    </style>
</head>
<body>
    <table>
        <thead>
            <tr>
"""

def generate_table_header(csv_file):
    with open(csv_file, mode="r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames if reader.fieldnames else []
        th_cells = [f"<th><pre>{html.escape(h)}</pre></th>" for h in headers]
        header_html = "            <tr>\n" + Path("\n").join(th_cells) + "\n            </tr>\n"
        return header_html, headers


def generate_table_body(csv_file, headers):
    rows_html = []
    with open(csv_file, mode="r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cell_htmls = []
            for h in headers:
                value = row.get(h, "")
                cell_htmls.append(f"<td><pre>{html.escape(value)}</pre></td>")
            row_html = "            <tr>\n" + Path("\n").join(cell_htmls) + "\n            </tr>"
            rows_html.append(row_html)
    return Path("\n").join(rows_html)


table_html_footer = """        </tbody>
    </table>
</body>
</html>
"""


def write_html_table(output_path, header_html, body_html):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(table_html_header)
        f.write(header_html)
        f.write("        </thead>\n        <tbody>\n")
        f.write(body_html)
        f.write("\n        </tbody>\n    </table>\n</body>\n</html>")
    logger.info(f"Table HTML file generated at: {output_path}")


def main():
    # Generate job cards HTML output file
    job_cards = generate_job_cards(input_csv)
    write_html_job_cards(output_html_job, job_cards)

    # Generate table-based HTML output file
    header_html, headers = generate_table_header(input_csv)
    body_html = generate_table_body(input_csv, headers)
    write_html_table(output_html_table, header_html, body_html)


if __name__ == "__main__":
    main()
