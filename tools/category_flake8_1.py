import re
from collections import defaultdict


def categorize_flake8_output(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

    issues = defaultdict(list)

    for line in lines:
        match = re.match(r"(./[^:]+):(\d+):\d+: (\w\d+) (.+)", line)
        if match:
            file_name, line_number, code, message = match.groups()
            issues[code].append((file_name, line_number, message))

    return issues


def display_issues(issues):
    for code, details in sorted(issues.items()):
        print(f"\nIssues of type {code}:")
        for file_name, line_number, message in details:
            print(f"{file_name}:{line_number} - {message}")


if __name__ == "__main__":
    flake8_output_path = "flake8_output.txt"  # Path to your flake8 output
file
issues = categorize_flake8_output(flake8_output_path)
display_issues(issues)
