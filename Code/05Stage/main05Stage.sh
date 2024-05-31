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

echo "Normalizating metrics exectuing normalizateMetrics.py"
python normalizateMetrics.py "$experimentName" 
echo "normalizateMetrics.py executed successfully."
echo ""  # Blank line

echo "Classifying metrics exectuing classificateMetrics.py"
python classificateMetrics.py "$experimentName" 
echo "classificateMetrics.py executed successfully."
echo ""  # Blank line

echo ""  # Blank line
echo "05Satge completed."
echo ""  # Blank line
echo "------------------------------------------"
