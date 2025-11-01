#!/bin/bash
# Complete Analysis and Documentation Generation
# This script runs the complete analysis and documentation generation process

echo "🚀 Complete Analysis and Documentation Generation"
echo "=================================================="
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed or not in PATH"
    echo "Please install Python 3 and try again"
    exit 1
fi

echo "✅ Python 3 is available"
echo ""

# Run the master analysis and documentation generator
echo "🔍 Running deep content analysis and documentation generation..."
echo "This may take several minutes depending on the size of your codebase..."
echo ""

python3 master_analysis_and_docs.py

echo ""
echo "🎉 Complete analysis and documentation generation finished!"
echo ""
echo "📁 Check the generated files:"
echo "  - Documentation: comprehensive_docs/"
echo "  - Analysis results: deep_analysis_results_*.json"
echo "  - Summary report: comprehensive_docs/ANALYSIS_SUMMARY_REPORT.md"
echo ""
echo "🚀 Next steps:"
echo "  1. View documentation: open comprehensive_docs/sphinx/_build/html/index.html"
echo "  2. Upload to GitHub: ./upload_python_projects.sh"
echo "  3. Review analysis: open comprehensive_docs/ANALYSIS_SUMMARY_REPORT.md"