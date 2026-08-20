from pathlib import Path
import csv
import html

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_150 = 150
CONSTANT_333 = 333
CONSTANT_555 = 555
CONSTANT_777 = 777


# Set the input/output paths; update these as necessary.
input_csv = Path(str(Path.home()) + "/Documents/QuantumForgeLabs/data.csv")
output_html = Path(str(Path.home()) + "/Documents/QuantumForgeLabs/data.html")

# This is a template for an individual job listing; you can modify the styling or fields.
job_template = """
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
    Description: {description_excerpt}...
  </div>
  <div class="apply-link">
    <a href="{apply_url}" target="_blank">Apply Now</a>
  </div>
</div>
"""


# Function to generate a short description excerpt (for example, first CONSTANT_150 characters)
def create_excerpt(text, length=CONSTANT_150):
    """create_excerpt function."""

    if len(text) <= length:
        return html.escape(text)
    return html.escape(text[:length].strip())  # escape to avoid HTML injection


# Begin constructing the final HTML
html_parts = []
html_parts.append(
    """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <title>LinkedIn Jobs Scraped</title>
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
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
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
    <h1>LinkedIn Jobs Scraped</h1>
"""
)

# Read the CSV file and generate job-listing blocks
with open(input_csv, mode="r", encoding="utf-8-sig") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Retrieve fields from the CSV; use get() with default empty string if missing.
        job_title = row.get("jobTitle", "").strip()
        company_name = row.get("companyName", "").strip()
        location = row.get("location", "").strip()
        posted_time = row.get("postedTimeRelative", "").strip()
        salary = row.get("salary", "").strip()
        description = row.get("description", "").strip()
        apply_url = row.get("applyUrl", "").strip()
        company_url = row.get("companyUrl", "").strip()

        # Create an excerpt of the description text
        description_excerpt = create_excerpt(description)

        # Fill in the job template using format() while escaping the strings as needed
        job_html = job_template.format(
            apply_url=html.escape(apply_url),
            job_title=html.escape(job_title),
            posted_time=html.escape(posted_time),
            company_url=html.escape(company_url) if company_url else "#",
            company_name=html.escape(company_name),
            location=html.escape(location),
            salary=html.escape(salary),
            description_excerpt=description_excerpt,
        )
        html_parts.append(job_html)

# Close off the HTML body
html_parts.append("</body>\n</html>")
final_html = Path("\n").join(html_parts)

# Write the final HTML to the output file
with open(output_html, mode="w", encoding="utf-8") as outfile:
    outfile.write(final_html)

logger.info(f"HTML file generated at: {output_html}")
