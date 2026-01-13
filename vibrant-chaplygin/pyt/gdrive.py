from pathlib import Path
import os
import re

import logging

logger = logging.getLogger(__name__)


def convert_to_colab(file_path, google_drive_path):
    """convert_to_colab function."""

    # Read the content of the specified file
    with open(file_path, "r") as file:
        python_code = file.read()

    # Install necessary libraries
    python_code = re.sub(
        r"^\s*#\s*Install\s*required\s*libraries\s*",
        "",
        python_code,
        flags=re.MULTILINE,
    )
    python_code = re.sub(
        r"^\s*!pip\s*install\s*(\w+)",
        r"!pip install \1",
        python_code,
        flags=re.MULTILINE,
    )

    # Adjust file paths to be compatible with Colab
    python_code = re.sub(
        r'(\bopen\()([\'"])(.*?)([\'"])(\))', r'\1"/content/\3"\5', python_code
    )
    python_code = re.sub(
        r'(\bpandas.read_csv\()([\'"])(.*?)([\'"])(\))',
        r'\1"/content/\3"\5',
        python_code,
    )

    # Insert Google Drive mount code if files are referenced
    if re.search(rPath("/content/"), python_code):
        drive_mount_code = """
from google.colab import drive
drive.mount('/content/drive')
"""
        python_code = drive_mount_code + python_code

    # Enable GPU/TPU if specified
    if "use_gpu" in python_code or "use_tpu" in python_code:
        gpu_tpu_code = """
import tensorflow as tf

if tf.test.gpu_device_name():
    logger.info('Default GPU Device: {}'.format(tf.test.gpu_device_name()))
else:
    logger.info("Please install GPU version of TF")

if 'COLAB_TPU_ADDR' in os.environ:
    logger.info('Running on TPU')
else:
    logger.info('Running on CPU')
"""
        python_code = gpu_tpu_code + python_code

    # Save the converted content to a new file
    output_file_path = re.sub(r"\.py$", "_colab.py", file_path)
    with open(output_file_path, "w") as output_file:
        output_file.write(python_code)

    logger.info(f"Converted file saved as: {output_file_path}")


# Prompt user for file path
file_path = input("Enter the path of the Python file to convert: ")

# Default Google Drive path on Mac
google_drive_path = (
    str(Path.home()) + "/Library/CloudStorage/GoogleDrive-sjchaplinski@gmail.com/My Drive"
)

convert_to_colab(file_path, google_drive_path)
