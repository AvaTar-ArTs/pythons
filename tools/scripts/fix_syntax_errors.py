#!/usr/bin/env python3
"""
Script to fix common syntax errors in Python files.
"""

import re
import sys
from pathlib import Path


def fix_duplicate_function_definitions(content):
    """Remove duplicate function definitions (async def followed by def)."""
    lines = content.split("\n")
    fixed_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        # Check if this is an async def followed by a def on next line
        if i + 1 < len(lines) and re.match(r"^\s*async def ", line):
            next_line = lines[i + 1]
            # If next line is a duplicate def with same function name
            async_match = re.match(r"^(\s*)async def (\w+)", line)
            def_match = re.match(r"^(\s*)def (\w+)", next_line)
            if async_match and def_match and async_match.group(2) == def_match.group(2):
                # Keep async version, skip the duplicate def line
                fixed_lines.append(line)
                i += 1
                # Skip the duplicate def line and any malformed return type annotation
                if i < len(lines) and "->" in lines[i] and ":" not in lines[i]:
                    i += 1
                continue
        fixed_lines.append(line)
        i += 1
    return "\n".join(fixed_lines)


def fix_malformed_function_definitions(content):
    """Fix function definitions with return type annotations in wrong place."""
    # Pattern: "def func(...): -> Type" should be "def func(...) -> Type:"
    content = re.sub(
        r"def (\w+)\(([^)]*)\):\s*->\s*(\w+)", r"def \1(\2) -> \3:", content
    )
    return content


def remove_orphaned_decorators(content):
    """Remove decorators that are not followed by function/class definitions."""
    lines = content.split("\n")
    fixed_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        # Check if this is a decorator
        if re.match(r"^\s*@\w+", line):
            # Look ahead to see if next non-empty line is a def/class/async def
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines):
                next_line = lines[j]
                # If next line is not a function/class definition, remove decorator
                if not re.match(r"^\s*(def|class|async def)", next_line):
                    # Skip this decorator line
                    i += 1
                    continue
        fixed_lines.append(line)
        i += 1
    return "\n".join(fixed_lines)


def fix_incomplete_statements(content):
    """Fix incomplete statements."""
    lines = content.split("\n")
    fixed_lines = []
    for i, line in enumerate(lines):
        # Fix incomplete save statements
        if "im_resized.save(file_path, dpi = (DPI_300, DPI_DPI_300), format" in line:
            line = line.replace("format", 'format="PNG")')
        if (
            'img.save(image_path, format = "PNG", dpi' in line
            and not line.rstrip().endswith(")")
        ):
            line = line.rstrip() + "=(300, 300))"

        # Fix incomplete function definitions
        if re.search(r"async def \w+\([^)]*,\s*upscale\s*$", line):
            line = line.rstrip() + "=False):"
        if re.search(r"async def \w+\([^)]*,\s*upscale\s*$", line):
            line = line.rstrip() + "=False):"

        # Fix incomplete resize calls
        if re.search(r"img = img\.resize\($", line) or re.search(
            r"im = im\.resize\($", line
        ):
            # Look for next line with size tuple
            if i + 1 < len(lines):
                next_line = lines[i + 1]
                if "width" in next_line or "height" in next_line:
                    # Skip this incomplete line, it will be handled by removing orphaned code
                    continue

        # Fix incomplete Image.MAX_IMAGE_PIXELS assignments
        if "Image.MAX_IMAGE_PIXELS = (" in line and not line.rstrip().endswith(")"):
            line = line.rstrip() + " None)"

        # Fix function definitions without colons (missing indented block)
        if re.match(r"^\s*async def \w+\([^)]+\)\s*$", line):
            # Check if next line is not indented (should be function body)
            if i + 1 < len(lines):
                next_line = lines[i + 1]
                if next_line.strip() and not next_line.startswith(
                    " " * (len(line) - len(line.lstrip()) + 4)
                ):
                    # Add colon and pass statement
                    line = line.rstrip() + ":"
                    fixed_lines.append(line)
                    # Add pass statement on next iteration
                    continue

        # Fix spacing issues in operators
        line = re.sub(r"\+\s*=", "+=", line)
        line = re.sub(r"-\s*=", "-=", line)
        line = re.sub(r"\*\s*=", "*=", line)
        line = re.sub(r"/\s*=", "/=", line)

        # Remove duplicate variable assignments on consecutive lines
        if i > 0:
            prev_line = lines[i - 1]
            if re.match(r"^\s*width, height = ", prev_line) and re.match(
                r"^\s*width, height = ", line
            ):
                # Skip duplicate
                continue

        fixed_lines.append(line)
    return "\n".join(fixed_lines)


def fix_class_definition_issues(content):
    """Remove code fragments from class definitions."""
    lines = content.split("\n")
    fixed_lines = []
    in_class = False
    in_function = False
    class_indent = 0
    function_indent = 0
    i = 0

    while i < len(lines):
        line = lines[i]
        # Detect class definition
        class_match = re.match(r"^(\s*)class \w+", line)
        if class_match:
            in_class = True
            class_indent = len(class_match.group(1))
            fixed_lines.append(line)
            i += 1
            continue

        # Detect function definition
        func_match = re.match(r"^(\s*)(def|async def) \w+", line)
        if func_match:
            in_function = True
            function_indent = len(func_match.group(1))
            # Check if function has a body
            if ":" in line:
                fixed_lines.append(line)
                i += 1
                # Check if next line is properly indented
                if i < len(lines):
                    next_line = lines[i]
                    if next_line.strip() and not next_line.startswith(
                        " " * (function_indent + 4)
                    ):
                        # Add pass statement
                        fixed_lines.append(" " * (function_indent + 4) + "pass")
                continue
            else:
                # Function definition without colon - add it
                line = line.rstrip() + ":"
                fixed_lines.append(line)
                i += 1
                if i < len(lines):
                    next_line = lines[i]
                    if next_line.strip() and not next_line.startswith(
                        " " * (function_indent + 4)
                    ):
                        fixed_lines.append(" " * (function_indent + 4) + "pass")
                continue

        if in_class:
            # Check if we're still in the class
            if (
                line.strip()
                and not line.startswith(" " * (class_indent + 1))
                and not line.startswith(" " * class_indent + "#")
            ):
                in_class = False
            elif in_class:
                # Remove obvious code fragments that shouldn't be in class
                if re.search(
                    r"(cache\[|key = |file_path = |directory = input|@lru_cache|width, height = |current_size = |img = |im = )",
                    line,
                ):
                    i += 1
                    continue

        if in_function:
            # Check if we're still in the function
            if line.strip():
                if line.startswith(" " * (function_indent + 4)) or line.startswith(
                    " " * function_indent + "#"
                ):
                    # Still in function
                    pass
                elif line.startswith(" " * function_indent) and not line.startswith(
                    " " * (function_indent + 1)
                ):
                    # Same level as function - function ended
                    in_function = False
                else:
                    # Different indentation - function ended
                    in_function = False

        # Remove orphaned code fragments (variable assignments that are clearly out of place)
        if (
            not in_class
            and not in_function
            and re.match(
                r"^\s*(width, height|current_size|image_path|input_directory|upscale|directory) = ",
                line,
            )
        ):
            # Check if this looks like it should be part of a function
            # If previous line is not a function definition, skip this orphaned line
            if i > 0:
                prev_line = lines[i - 1]
                if not re.search(r"(def |async def |:\s*$)", prev_line):
                    i += 1
                    continue

        fixed_lines.append(line)
        i += 1

    return "\n".join(fixed_lines)


def fix_string_literals(content):
    """Fix unterminated string literals."""
    lines = content.split("\n")
    fixed_lines = []
    for line in lines:
        # Fix malformed quotes like '"' or "'"
        line = re.sub(r"['\"]\"['\"]", r"'\''", line)  # Fix '"' -> "'"
        line = re.sub(r"['\"]'['\"]", r'"\'"', line)  # Fix "'" -> "'"

        # Count quotes
        single_quotes = line.count("'") - line.count("\\'")
        double_quotes = line.count('"') - line.count('\\"')
        # If odd number of quotes and line seems incomplete
        if (
            single_quotes % 2 == 1 or double_quotes % 2 == 1
        ) and not line.rstrip().endswith(('"', "'", "\\")):
            # Try to fix common patterns
            if line.count('"') % 2 == 1 and '"' in line:
                # Find the opening quote and add closing quote
                last_quote_idx = line.rfind('"')
                if last_quote_idx > 0:
                    line = line[: last_quote_idx + 1] + '"' + line[last_quote_idx + 1 :]
        fixed_lines.append(line)
    return "\n".join(fixed_lines)


def fix_missing_indented_blocks(content):
    """Fix missing indented blocks after function/class/if definitions."""
    lines = content.split("\n")
    fixed_lines = []
    i = 0

    while i < len(lines):
        line = lines[i]
        fixed_lines.append(line)

        # Check if this line defines something that needs a body
        needs_body = False
        indent_level = len(line) - len(line.lstrip())

        # Function definition
        if re.match(r"^\s*(def|async def) \w+.*:\s*$", line):
            needs_body = True
        # Class definition
        elif re.match(r"^\s*class \w+.*:\s*$", line):
            needs_body = True
        # If/elif/else/for/while/try/except
        elif re.match(r"^\s*(if|elif|else|for|while|try|except|finally):\s*$", line):
            needs_body = True

        if needs_body and i + 1 < len(lines):
            next_line = lines[i + 1]
            # If next line is not indented more, add a pass statement
            if next_line.strip():
                next_indent = len(next_line) - len(next_line.lstrip())
                if next_indent <= indent_level:
                    # Add pass statement
                    fixed_lines.append(" " * (indent_level + 4) + "pass")

        i += 1

    return "\n".join(fixed_lines)


def fix_async_init(content):
    """Fix async __init__ methods (__init__ cannot be async)."""
    # Replace "async def __init__" with "def __init__"
    content = re.sub(r"async def __init__", "def __init__", content)

    # Fix cases where __init__ has pass but then code follows
    lines = content.split("\n")
    fixed_lines = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Check if this is __init__ definition
        if re.match(r"^(\s*)def __init__", line):
            indent = len(re.match(r"^(\s*)", line).group(1))
            fixed_lines.append(line)
            i += 1

            # Look for pass statement followed by unindented code that should be in __init__
            while i < len(lines):
                next_line = lines[i]
                if not next_line.strip():
                    fixed_lines.append(next_line)
                    i += 1
                    continue

                next_indent = len(next_line) - len(next_line.lstrip())

                # If line starts with self. and is at wrong indentation level
                if (
                    next_line.strip().startswith("self.")
                    and next_indent == indent
                    and not next_line.strip().startswith("#")
                ):
                    # This should be indented inside __init__
                    fixed_lines.append(" " * (indent + 4) + next_line.lstrip())
                    i += 1
                elif next_indent > indent:
                    # Already properly indented
                    fixed_lines.append(next_line)
                    i += 1
                else:
                    # End of __init__ method
                    break
            continue

        fixed_lines.append(line)
        i += 1

    return "\n".join(fixed_lines)


def fix_file(filepath):
    """Fix syntax errors in a single file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return False

    original_content = content

    # Apply fixes
    content = fix_duplicate_function_definitions(content)
    content = fix_malformed_function_definitions(content)
    content = remove_orphaned_decorators(content)
    content = fix_incomplete_statements(content)
    content = fix_class_definition_issues(content)
    content = fix_string_literals(content)
    content = fix_missing_indented_blocks(content)
    content = fix_async_init(content)

    if content != original_content:
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Error writing {filepath}: {e}")
            return False

    return False


def main():
    """Main function to fix files."""
    if len(sys.argv) > 1:
        files = [Path(f) for f in sys.argv[1:]]
    else:
        # Fix all Python files in current directory
        files = list(Path(".").rglob("*.py"))

    fixed_count = 0
    for filepath in files:
        if filepath.name == "fix_syntax_errors.py":
            continue
        if fix_file(filepath):
            print(f"Fixed: {filepath}")
            fixed_count += 1

    print(f"\nFixed {fixed_count} files")


if __name__ == "__main__":
    main()
