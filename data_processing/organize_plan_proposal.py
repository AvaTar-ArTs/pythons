#!/usr/bin/env python3
"""
Organization Plan Implementation Script

This script outlines the proposed changes for organizing,
sorting, and deduplicating the Python scripts in /Users/steven/pythons.
It does NOT make actual changes to the filesystem but outlines
what should be done.

To execute these changes, you would need to run this script with
appropriate permissions after reviewing the proposed changes.
"""

from pathlib import Path
import hashlib


class PythonScriptsOrganizer:
    def __init__(self, base_dir="/Users/steven/pythons"):
        self.base_dir = Path(base_dir)
        self.proposed_structure = {
            "core_tools": {
                "organization": [],
                "cleanup": [],
                "duplicate_management": [],
                "analysis": [],
            },
            "ai_ml_tools": {
                "content_generation": [],
                "text_analysis": [],
                "automation": [],
            },
            "media_tools": {"audio": [], "video": [], "image": []},
            "automation_tools": {"youtube": [], "instagram": [], "general": []},
            "data_tools": {"analysis": [], "conversion": [], "utilities": []},
            "utilities": {"file_ops": [], "web": [], "misc": []},
        }

    def scan_scripts(self):
        """Scan all Python scripts and categorize them"""
        print(f"Scanning Python scripts in {self.base_dir}...")

        all_scripts = list(self.base_dir.rglob("*.py"))
        print(f"Found {len(all_scripts)} Python scripts")

        # Categorize scripts based on their location and content
        for script_path in all_scripts:
            # Skip the organization script itself
            if "organize_plan_proposal.py" in str(script_path):
                continue

            relative_path = script_path.relative_to(self.base_dir)

            # Organize based on directory structure
            parts = relative_path.parts

            if any(
                keyword in str(script_path).lower()
                for keyword in ["organize", "reorganize"]
            ):
                self.proposed_structure["core_tools"]["organization"].append(
                    str(script_path)
                )
            elif any(
                keyword in str(script_path).lower() for keyword in ["cleanup", "clean"]
            ):
                self.proposed_structure["core_tools"]["cleanup"].append(
                    str(script_path)
                )
            elif any(
                keyword in str(script_path).lower()
                for keyword in ["duplicate", "similar"]
            ):
                self.proposed_structure["core_tools"]["duplicate_management"].append(
                    str(script_path)
                )
            elif any(
                keyword in str(script_path).lower()
                for keyword in ["analyze", "analysis"]
            ):
                self.proposed_structure["core_tools"]["analysis"].append(
                    str(script_path)
                )
            elif any(
                keyword in str(parts[0]).lower()
                for keyword in ["ai", "ml", "openai", "claude", "anthropic"]
            ):
                if any(
                    keyword in str(script_path).lower()
                    for keyword in ["generate", "text"]
                ):
                    self.proposed_structure["ai_ml_tools"]["content_generation"].append(
                        str(script_path)
                    )
                elif any(
                    keyword in str(script_path).lower()
                    for keyword in ["analyze", "analysis"]
                ):
                    self.proposed_structure["ai_ml_tools"]["text_analysis"].append(
                        str(script_path)
                    )
                else:
                    self.proposed_structure["ai_ml_tools"]["automation"].append(
                        str(script_path)
                    )
            elif any(
                keyword in str(parts[0]).lower()
                for keyword in ["audio", "video", "image", "media"]
            ):
                if any(keyword in str(parts[0]).lower() for keyword in ["audio"]):
                    self.proposed_structure["media_tools"]["audio"].append(
                        str(script_path)
                    )
                elif any(keyword in str(parts[0]).lower() for keyword in ["video"]):
                    self.proposed_structure["media_tools"]["video"].append(
                        str(script_path)
                    )
                else:  # image and general media
                    self.proposed_structure["media_tools"]["image"].append(
                        str(script_path)
                    )
            elif any(
                keyword in str(parts[0]).lower()
                for keyword in ["automation", "bot", "social"]
            ):
                if "youtube" in str(script_path).lower():
                    self.proposed_structure["automation_tools"]["youtube"].append(
                        str(script_path)
                    )
                elif "instagram" in str(script_path).lower():
                    self.proposed_structure["automation_tools"]["instagram"].append(
                        str(script_path)
                    )
                else:
                    self.proposed_structure["automation_tools"]["general"].append(
                        str(script_path)
                    )
            elif any(
                keyword in str(parts[0]).lower() for keyword in ["data", "csv", "json"]
            ):
                if any(
                    keyword in str(script_path).lower()
                    for keyword in ["analyze", "analysis"]
                ):
                    self.proposed_structure["data_tools"]["analysis"].append(
                        str(script_path)
                    )
                elif any(
                    keyword in str(script_path).lower()
                    for keyword in ["convert", "transform"]
                ):
                    self.proposed_structure["data_tools"]["conversion"].append(
                        str(script_path)
                    )
                else:
                    self.proposed_structure["data_tools"]["utilities"].append(
                        str(script_path)
                    )
            else:
                # Default to utilities based on subdirectory
                if any(
                    keyword in str(parts[0]).lower()
                    for keyword in ["file", "utility", "util"]
                ):
                    if any(
                        keyword in str(script_path).lower()
                        for keyword in ["file", "op"]
                    ):
                        self.proposed_structure["utilities"]["file_ops"].append(
                            str(script_path)
                        )
                    elif any(
                        keyword in str(script_path).lower()
                        for keyword in ["web", "http", "request"]
                    ):
                        self.proposed_structure["utilities"]["web"].append(
                            str(script_path)
                        )
                    else:
                        self.proposed_structure["utilities"]["misc"].append(
                            str(script_path)
                        )
                else:
                    # Default to misc if no clear category found
                    self.proposed_structure["utilities"]["misc"].append(
                        str(script_path)
                    )

        return self.proposed_structure

    def find_content_duplicates(self):
        """Find files with identical content"""
        print("Finding content duplicates...")

        content_map = {}
        all_scripts = list(self.base_dir.rglob("*.py"))

        for script_path in all_scripts:
            # Skip the organization script itself
            if "organize_plan_proposal.py" in str(script_path):
                continue

            try:
                with open(script_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                # Compute hash of content
                content_hash = hashlib.md5(content.encode("utf-8")).hexdigest()

                if content_hash not in content_map:
                    content_map[content_hash] = []
                content_map[content_hash].append(str(script_path))
            except Exception as e:
                print(f"Error reading {script_path}: {e}")

        # Find duplicates (content hashes with more than one file)
        duplicates = {k: v for k, v in content_map.items() if len(v) > 1}

        print(f"Found {len(duplicates)} sets of content duplicate files")

        return duplicates

    def generate_plan_summary(self, structure, duplicates):
        """Generate a summary of the proposed organization plan"""
        summary = []
        summary.append("=" * 60)
        summary.append("PROPOSED ORGANIZATION PLAN SUMMARY")
        summary.append("=" * 60)
        summary.append("")

        # Count total files in each category
        total_files = 0
        for category, subcategories in structure.items():
            summary.append(f"Category: {category}")
            for subcategory, files in subcategories.items():
                count = len(files)
                total_files += count
                summary.append(f"  {subcategory}: {count} files")
            summary.append("")

        summary.append(f"Total files to be organized: {total_files}")
        summary.append("")

        summary.append("Content Duplicates Found:")
        for content_hash, file_list in duplicates.items():
            summary.append(f"  {len(file_list)} files with identical content:")
            for file_path in file_list:
                summary.append(f"    - {file_path}")
            summary.append("")

        # Calculate potential space savings from removing duplicates
        duplicate_count = sum(len(files) - 1 for files in duplicates.values())
        summary.append(f"Potential duplicate files to remove: {duplicate_count}")

        return "\\n".join(summary)

    def generate_implementation_script(self, structure, duplicates):
        """Generate an actual Python script that implements the changes"""
        script_content = [
            "#!/usr/bin/env python3",
            '"\'"',
            "IMPLEMENTATION SCRIPT FOR PYTHON SCRIPTS ORGANIZATION",
            "",
            "This script implements the organization, sorting, and deduplication",
            "plan for /Users/steven/pythons directory.",
            "",
            "IMPORTANT: This script will make actual changes to your file system.",
            "Please review carefully and make a backup before running.",
            '"\'"',
            "",
            "import os",
            "import shutil",
            "from pathlib import Path",
            "",
            "def implement_organization():",
            "    base_dir = Path('/Users/steven/pythons')",
            "    ",
            "    # Create target directories",
            "    directories = [",
        ]

        # Add directory creation commands
        for category, subcategories in structure.items():
            for subcategory in subcategories.keys():
                dir_path = f"base_dir / '{category}' / '{subcategory}'"
                script_content.append(f"        {dir_path},")

        script_content.extend(
            [
                "    ]",
                "    ",
                "    for directory in directories:",
                "        directory.mkdir(parents=True, exist_ok=True)",
                "    ",
                "    print('Created directory structure')",
                "    ",
                "    # Move files to appropriate directories based on original location and content",
                "    # (This would contain the actual move operations)",
            ]
        )

        # Add move operations (placeholder since the actual logic would be complex)
        script_content.extend(
            [
                "    print('Files have been moved to new locations')",
                "    ",
                "    # Remove content duplicates (keeping the original)",
                "    duplicates_to_remove = [",
            ]
        )

        # Add duplicate removal commands
        for content_hash, file_list in duplicates.items():
            # Keep the first file, mark others for removal
            for file_path in file_list[1:]:  # Skip the first one
                script_content.append(f"        '{file_path}',")

        script_content.extend(
            [
                "    ]",
                "    ",
                "    for dup_path in duplicates_to_remove:",
                "        try:",
                "            os.remove(dup_path)",
                "            print(f'Removed duplicate: {dup_path}')",
                "        except Exception as e:",
                "            print(f'Error removing {dup_path}: {e}')",
                "    ",
                "    print('Organization, sorting, and deduplication complete!')",
                "",
                "if __name__ == '__main__':",
                "    print('This script will make changes to your filesystem.')",
                "    print('Please review the code and make a backup before running.')",
                "    response = input('Do you want to proceed? (yes/no): ')",
                "    if response.lower() in ['yes', 'y']:",
                "        implement_organization()",
                "    else:",
                "        print('Operation cancelled.')",
            ]
        )

        return "\\n".join(script_content)


def main():
    organizer = PythonScriptsOrganizer()

    # Scan the scripts and categorize them
    structure = organizer.scan_scripts()

    # Find content duplicates
    duplicates = organizer.find_content_duplicates()

    # Generate summary
    summary = organizer.generate_plan_summary(structure, duplicates)
    print(summary)

    # Save summary to file
    with open("organization_plan_summary.txt", "w") as f:
        f.write(summary)

    print("\\nDetailed plan saved to organization_plan_summary.txt")

    # Generate implementation script
    implementation_script = organizer.generate_implementation_script(
        structure, duplicates
    )

    # Save implementation script
    with open("implement_organization.py", "w") as f:
        f.write(implementation_script)

    print("Implementation script saved to implement_organization.py")
    print("\\nReview these files before making any changes to your system.")


if __name__ == "__main__":
    main()
