"""
Bubblespider Amazon Scraper

This module provides functionality for bubblespider amazon scraper.

Author: Auto-generated
Date: 2025-11-01
"""

import csv
import os
import re

import logging

logger = logging.getLogger(__name__)


def extract_amazon_urls_to_csv(input_file_path):
    """extract_amazon_urls_to_csv function."""

    # Regular expressions for matching the URLs
    product_url_pattern = re.compile(r"https:\/\/www\.amazon\.com\/dp\/[A-Za-z0-9]+")
    image_url_pattern = re.compile(
        r"https:\/\/m\.media-amazon\.com\/images\/I\/[A-Za-z0-9_-]+\.\w+"
    )

    with open(input_file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Find all matching URLs
    product_urls = product_url_pattern.findall(content)
    image_urls = image_url_pattern.findall(content)

    # Prepare the output CSV file name
    output_csv_path = "output.csv"
    counter = 1
    while os.path.exists(output_csv_path):
        output_csv_path = f"output_{counter}.csv"
        counter += 1

    # Write the extracted URLs to a CSV file
    with open(output_csv_path, "w", newline="", encoding="utf-8") as csvfile:
        csvwriter = csv.writer(csvfile)
        for product_url, image_url in zip(product_urls, image_urls):
            csvwriter.writerow([product_url, image_url])

    logger.info(f"URLs extracted to {output_csv_path}")


# Ask user for the HTML file location
input_file_path = input("Enter the path to your HTML file: ")
extract_amazon_urls_to_csv(input_file_path)
