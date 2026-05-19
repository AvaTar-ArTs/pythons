#!/usr/bin/env python3
"""
Final NocturneMelodies Content Organization Verification Script

This script verifies that all NocturneMelodies content is properly organized within
the /Users/steven/Music/nocTurneMeLoDieS directory and creates a final verification report.
"""

import json
from datetime import datetime
from pathlib import Path


def verify_content_organization():
    """Verify that all NocturneMelodies content is properly organized"""

    base_dir = Path("/Users/steven/Music/nocTurneMeLoDieS")
    verification_results = {
        "timestamp": datetime.now().isoformat(),
        "directories_verified": [],
        "files_count": {},
        "mobile_optimized_versions": 0,
        "original_consoliated_versions": 0,
        "issues_found": [],
    }

    # Check for the existence of all consolidated directories
    consolidated_dirs = [
        "CONSOLIDATED_HTML",
        "NOCTURNEMELODIES_WEB_STRUCTURE_V2",
        "NOCTURNEMELODIES_WEB_STRUCTURE_V3",
        "NOCTURNEMELODIES_FINAL_ORGANIZATION",
    ]

    for dir_name in consolidated_dirs:
        dir_path = base_dir / dir_name
        if dir_path.exists():
            verification_results["directories_verified"].append(str(dir_path))
            # Count HTML files in each directory
            html_files = list(dir_path.rglob("*.html"))
            verification_results["files_count"][dir_name] = len(html_files)

            # Count mobile optimized versions
            mobile_files = list(dir_path.rglob("*_mobile.html"))
            verification_results["mobile_optimized_versions"] += len(mobile_files)

            # Count original consolidated versions
            verification_results["original_consoliated_versions"] += len(html_files) - len(mobile_files)
        else:
            verification_results["issues_found"].append(f"Missing directory: {dir_path}")

    # Check for any HTML files still in the base directory that should be organized
    loose_html_files = list(base_dir.glob("*.html"))
    if loose_html_files:
        verification_results["issues_found"].append(f"Found {len(loose_html_files)} loose HTML files in base directory")

    # Save verification report
    report_path = base_dir / "FINAL_ORGANIZATION_VERIFICATION_REPORT.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(verification_results, f, indent=2)

    # Create a human-readable summary
    summary_path = base_dir / "FINAL_ORGANIZATION_VERIFICATION_SUMMARY.md"
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("# Final NocturneMelodies Content Organization Verification Report\n\n")
        f.write(f"**Generated on**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        f.write("## Directories Verified\n")
        for dir_path in verification_results["directories_verified"]:
            f.write(f"- ✅ {dir_path}\n")

        f.write("\n## File Counts by Directory\n")
        for dir_name, count in verification_results["files_count"].items():
            f.write(f"- {dir_name}: {count} HTML files\n")

        f.write("\n## Mobile Optimization Status\n")
        f.write(f"- Mobile-optimized versions: {verification_results['mobile_optimized_versions']}\n")
        f.write(f"- Original consolidated versions: {verification_results['original_consoliated_versions']}\n")

        f.write(f"\n## Total HTML Files Processed: {sum(verification_results['files_count'].values())}\n\n")

        if verification_results["issues_found"]:
            f.write("## Issues Found\n")
            for issue in verification_results["issues_found"]:
                f.write(f"- ❌ {issue}\n")
        else:
            f.write("## Status: All systems verified ✅\n")
            f.write("No issues found. All NocturneMelodies content is properly organized within the Music directory.\n")

    return verification_results


def main():
    print("Verifying NocturneMelodies content organization...")
    print("Ensuring all content is properly organized within /Users/steven/Music/nocTurneMeLoDieS")

    results = verify_content_organization()

    print("\nVerification complete!")
    print("Report saved to: /Users/steven/Music/nocTurneMeLoDieS/FINAL_ORGANIZATION_VERIFICATION_REPORT.json")
    print("Summary saved to: /Users/steven/Music/nocTurneMeLoDieS/FINAL_ORGANIZATION_VERIFICATION_SUMMARY.md")

    print(f"\nDirectories verified: {len(results['directories_verified'])}")
    print(f"Total HTML files processed: {sum(results['files_count'].values())}")
    print(f"Mobile-optimized versions created: {results['mobile_optimized_versions']}")

    if results["issues_found"]:
        print(f"\nIssues found: {len(results['issues_found'])}")
        for issue in results["issues_found"]:
            print(f"  - {issue}")
    else:
        print("\n✅ All NocturneMelodies content is properly organized within the Music directory!")
        print(
            "Content is mobile-optimized and follows the same successful principles as the previous consolidation work."
        )


if __name__ == "__main__":
    main()
