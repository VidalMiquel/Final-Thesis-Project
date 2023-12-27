#!/bin/bash

# Retrieve the experiment name from the first argument
experimentName="$1"

# Retrieve the club for the experiment from the second argument
club="$2"

# Get the current directory path
currentDirectory=$(dirname "$0")

# Change to the directory containing start_FirstStage.py
cd "$currentDirectory"

echo Executing SecondStage...

# Execute start_SecondStage.py
echo "Creating necessary directories with start_SecondStage.py..."
python start_SecondStage.py "$experimentName"

# Execute splitByGoals.py
echo ""
echo "Splitting files by goals..."
python splitByGoals.py "$experimentName"

# Execute filterByTeam.py
echo ""
echo "Filtering files by team..."
python filterByTeam.py "$experimentName" "$club"

echo ""  # Blank line
echo "Process completed."
echo ""  # Blank line
