#!/bin/bash
# Quick run script for Twitter Scanner

cd "$(dirname "$0")"

# Check if venv exists, create if not
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

echo "🐋 Running Twitter Scanner..."
python scanner.py "$@"
