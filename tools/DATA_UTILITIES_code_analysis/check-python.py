import os
import subprocess


def check_with_pylint(file_path):
    """Run pylint on the given Python file to check for errors and style issues.

    :param file_path: Path to the Python file.
    :return: None
    """
    result = subprocess.run(
        ["pylint", file_path], check=False, capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"Pylint issues in {file_path}:")
        print(result.stdout)
    else:
        print(f"No pylint issues found in {file_path}")


def check_with_flake8(file_path):
    """Run flake8 on the given Python file to check for style issues.

    :param file_path: Path to the Python file.
    :return: None
    """
    result = subprocess.run(
        ["flake8", file_path], check=False, capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"Flake8 issues in {file_path}:")
        print(result.stdout)
    else:
        print(f"No flake8 issues found in {file_path}")


def process_directory(input_dir):
    """Recursively process all Python files in the input directory and check for errors.

    :param input_dir: Path to the input directory.
    :return: None
    """
    for root, _, files in os.walk(input_dir):
        for filename in files:
            if filename.lower().endswith(".py"):
                file_path = os.path.join(root, filename)
                check_with_pylint(file_path)
                check_with_flake8(file_path)


if __name__ == "__main__":
    # Define the base input directory
    # Update to your actual input directory
    input_dir = "/Users/steven/Documents/Python/"

    # Process the directory and check Python files for errors
    process_directory(input_dir)
