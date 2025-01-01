#!/bin/bash
# To run this script, copy paste the following
# chmod +x setup.sh; ./setup.sh
# Only run the script if app.py doesn't run.
# Create a virtual environment (optional but recommended)
echo "Setting up a virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Update pip to the latest version
echo "Updating pip..."
pip install --upgrade pip

# Install required Python packages
echo "Installing dependencies..."
pip install Flask pymongo flask_cors pyopenssl flask_cors

# Confirm successful installation
echo "Dependencies installed successfully!"

# Instructions to start MongoDB if it's not running
echo "Please make sure MongoDB is running locally on port 27017."
echo "To start MongoDB, run: sudo systemctl start mongod (Linux) or brew services start mongodb-community (Mac, if installed via Homebrew)."

# Instructions for starting the Flask application
echo "To start the Flask server, activate the virtual environment with 'source venv/bin/activate' and 