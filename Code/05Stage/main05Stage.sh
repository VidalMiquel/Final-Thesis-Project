#!/bin/bash

# Retrieve the experiment name from the first argument
experimentName="$1"

# Retrieve the club for the experiment from the second argument
club="$2"

# Get the current directory path
currentDirectory=$(dirname "$0")

# Change to the directory containing start05Stage.py
cd "$currentDirectory"

echo Executing "05Stage"...
echo "" # Blank line

echo "Getting graphs metrics exectuing getMetrics.py"
python getMetrics.py "$experimentName" "$club"
echo "getMetrics.py executed successfully."
echo ""  # Blank line

echo "05Satge completed."
echo ""  # Blank line
echo "------------------------------------------"
