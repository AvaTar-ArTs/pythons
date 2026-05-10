
import pandas as pd
from collections import Counter
import os
from pathlib import Path

def generate_summary_report(csv_file_path, output_file_path):
    """
    Generates a Markdown summary report from the comprehensive_meta.csv file.
    """
    try:
        df = pd.read_csv(csv_file_path)
    except FileNotFoundError:
        with open(output_file_path, "w") as f:
            f.write("# Analysis Summary Report\\n\\n")
            f.write("`comprehensive_meta.csv` not found. No data to summarize.\\n")
        print(f"Error: {csv_file_path} not found.")
        return

    report_lines = []
    report_lines.append("# Python Scripts Analysis Summary Report\n")
    report_lines.append(f"**Date:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    report_lines.append(f"**Source Directory:** `/Users/steven/pythons/`\n")
    report_lines.append(f"**Total Files Analyzed:** {len(df)}\n")

    # Basic Statistics
    report_lines.append("\n## 📊 Basic Statistics\n")
    
    # Files Not Found
    files_not_found = df[df['category'] == 'File Not Found']
    report_lines.append(f"- **Files not found during processing:** {len(files_not_found)} out of {len(df)} total files.\n")
    if not files_not_found.empty:
        report_lines.append("  (These entries indicate that the file was present during initial listing but could not be read during content analysis, possibly due to dynamic file system changes or transient issues during a specific read attempt. Please verify their current existence if unexpected.)\n")

    # Filter out 'File Not Found' for further analysis
    df_filtered = df[df['category'] != 'File Not Found']
    report_lines.append(f"- **Successfully analyzed files:** {len(df_filtered)}\n")

    if not df_filtered.empty:
        # Unique Categories
        unique_categories = df_filtered['category'].nunique()
        report_lines.append(f"- **Unique Categories Identified:** {unique_categories}\n")

        # Top 5 Categories
        top_categories = df_filtered['category'].value_counts().head(5)
        report_lines.append("\n### Top 5 Most Common Categories:\n")
        for category, count in top_categories.items():
            report_lines.append(f"  - `{category}`: {count} files\n")

        # API Usage Summary
        report_lines.append("\n## 🔌 API Usage Summary\n")
        all_apis = []
        df_filtered['apis_used'].dropna().apply(lambda x: all_apis.extend([api.strip() for api in x.split(',')]) if isinstance(x, str) else None)
        
        if all_apis:
            top_apis = Counter(all_apis).most_common(5)
            report_lines.append("\n### Top 5 Most Used APIs:\n")
            for api, count in top_apis:
                report_lines.append(f"  - `{api}`: {count} mentions\n")
        else:
            report_lines.append("- No specific APIs identified or parsed from the scripts.\n")

        # Complexity Distribution
        report_lines.append("\n## 📈 Complexity Distribution\n")
        complexity_counts = df_filtered['complexity'].value_counts()
        for complexity_level in ['high', 'medium', 'low', 'notebook', 'data-file']:
            if complexity_level in complexity_counts:
                report_lines.append(f"- `{complexity_level}`: {complexity_counts[complexity_level]} files\n")
            else:
                report_lines.append(f"- `{complexity_level}`: 0 files\n")

        # General Insights/Recommendations
        report_lines.append("\n## 💡 General Insights & Recommendations\n")
        report_lines.append("Based on the analysis, here are some observations and potential next steps:\n")

        if len(files_not_found) > 0:
            report_lines.append(f"- **File System Consistency**: A notable number of files ({len(files_not_found)}) were listed but not found during content analysis. It is recommended to investigate these discrepancies to ensure file system integrity and prevent issues with automated scripts relying on these paths.\n")
        
        if unique_categories > 10:
            report_lines.append(f"- **Categorization Refinement**: With {unique_categories} unique categories, consider a hierarchical categorization system or merging closely related categories to simplify management and improve discoverability.\n")
        
        high_complexity_files = df_filtered[df_filtered['complexity'] == 'high']
        if len(high_complexity_files) > len(df_filtered) * 0.2: # More than 20% high complexity
            report_lines.append(f"- **High Complexity Scripts**: {len(high_complexity_files)} files are identified as having high complexity. Review these scripts for refactoring opportunities to improve maintainability and reduce potential bug surface areas.\n")

        report_lines.append(f"- **API Integration**: The identified APIs ({', '.join([api for api, count in top_apis]) if all_apis else 'N/A'}) suggest areas of strong external service integration. Ensure consistent API key management and error handling across these integrations.\n")
        report_lines.append("- **Documentation Focus**: Consider generating more detailed documentation or READMEs for scripts in critical categories or those with high complexity to facilitate onboarding and maintenance.\n")
        report_lines.append("- **Deduplication Review**: High counts of data-files and notebooks, along with potential duplicates ('File Not Found' issues might mask actual duplicates if files were moved/deleted), suggest a review of file deduplication and versioning strategies.\n")

    else:
        report_lines.append("\n- No Python files were successfully analyzed for content beyond their path. The `comprehensive_meta.csv` might contain only file paths with 'File Not Found' status, or all relevant files were already processed in previous runs.\n")
        report_lines.append("- Ensure the Python scripts are accessible and readable in the specified directory, and that the analysis process is correctly configured.\n")



    with open(output_file_path, "w") as f:
        f.writelines(report_lines)
    print(f"Summary report generated at: {output_file_path}")

if __name__ == "__main__":
    current_dir = Path("/Users/steven/pythons")
    csv_input = current_dir / "comprehensive_meta.csv"
    markdown_output = current_dir / "COMPREHENSIVE_PYTHON_ANALYSIS_REPORT.md"
    generate_summary_report(csv_input, markdown_output)
