#!/bin/bash
# View Documentation
# This script opens the generated documentation in your browser

echo "📚 Opening Python Projects Documentation"
echo "========================================"
echo ""

# Check if documentation exists
if [ ! -d "comprehensive_docs" ]; then
    echo "❌ Documentation not found. Please run the analysis first:"
    echo "   python3 simple_analysis_and_docs.py"
    exit 1
fi

echo "📁 Available Documentation:"
echo ""

# Main README
if [ -f "comprehensive_docs/README.md" ]; then
    echo "1. 📖 Main Overview: comprehensive_docs/README.md"
fi

# Sphinx documentation
if [ -d "comprehensive_docs/sphinx" ]; then
    echo "2. 📚 Sphinx Documentation: comprehensive_docs/sphinx/_build/html/index.html"
fi

# PyDoc documentation
if [ -f "comprehensive_docs/pydoc/index.html" ]; then
    echo "3. 🔍 PyDoc Documentation: comprehensive_docs/pydoc/index.html"
fi

# API reference
if [ -f "comprehensive_docs/api/index.md" ]; then
    echo "4. 🔧 API Reference: comprehensive_docs/api/index.md"
fi

# Portfolio
if [ -f "comprehensive_docs/portfolio/README.md" ]; then
    echo "5. 🎨 Portfolio: comprehensive_docs/portfolio/README.md"
fi

# Summary report
if [ -f "comprehensive_docs/ANALYSIS_SUMMARY_REPORT.md" ]; then
    echo "6. 📊 Analysis Report: comprehensive_docs/ANALYSIS_SUMMARY_REPORT.md"
fi

echo ""
echo "🚀 Opening documentation..."

# Try to open the main documentation
if command -v open &> /dev/null; then
    # macOS
    if [ -f "comprehensive_docs/sphinx/_build/html/index.html" ]; then
        echo "Opening Sphinx documentation..."
        open comprehensive_docs/sphinx/_build/html/index.html
    elif [ -f "comprehensive_docs/README.md" ]; then
        echo "Opening main README..."
        open comprehensive_docs/README.md
    fi
elif command -v xdg-open &> /dev/null; then
    # Linux
    if [ -f "comprehensive_docs/sphinx/_build/html/index.html" ]; then
        echo "Opening Sphinx documentation..."
        xdg-open comprehensive_docs/sphinx/_build/html/index.html
    elif [ -f "comprehensive_docs/README.md" ]; then
        echo "Opening main README..."
        xdg-open comprehensive_docs/README.md
    fi
else
    echo "⚠️  Could not automatically open documentation."
    echo "   Please manually open the files listed above."
fi

echo ""
echo "✅ Documentation opened!"
echo ""
echo "💡 Tip: You can also view the files directly in your text editor or IDE."