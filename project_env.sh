#!/usr/bin/env bash

# Specify the path to your virtual environment
VENV_DIR=".venv"

# Check if the virtual environment exists
if [ -d "$VENV_DIR" ]; then
    # Activate the virtual environment
    source "$VENV_DIR/bin/activate"
    echo "Virtual environment activated."
else
    echo "Virtual environment not found. Please create it first."
fi
