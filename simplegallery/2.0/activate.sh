#!/bin/bash
# SimpleGallery 2.0 Virtual Environment Activation Script

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Activate the virtual environment
source "$SCRIPT_DIR/venv/bin/activate"

echo "✅ SimpleGallery 2.0 virtual environment activated!"
echo "📦 Python: $(python --version)"
echo "📍 Location: $SCRIPT_DIR"
echo ""
echo "To deactivate, run: deactivate"
echo ""

# Add current directory to Python path for imports
export PYTHONPATH="$SCRIPT_DIR:$PYTHONPATH"

