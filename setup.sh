#!/bin/bash
# Setup script for AbruvaCare

echo "Setting up AbruvaCare..."

# Check if venv exists, if not create it
if [ ! -d "venv" ]; then
    echo "Creating virtual environment with Python 3.9..."
    # Try python3.9 first, fallback to python3
    if command -v python3.9 &> /dev/null; then
        python3.9 -m venv venv
    else
        python3 -m venv venv
    fi
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

echo ""
echo "Setup complete! To run the application:"
echo "  source venv/bin/activate"
echo "  uvicorn app.main:app --reload"
echo ""
echo "Or use: ./run.sh"

