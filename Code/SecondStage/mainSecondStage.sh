#!/bin/bash

# Retrieve the experiment name from the first argument
experimentName="$1"

# Retrieve the club for the experiment from the second argument
club="$2"

# Get the current directory path
currentDirectory=$(dirname "$0")

# Change to the directory containing startSecondStage.py
cd "$currentDirectory"

echo Executing SecondStage...
echo "" # Blank line

# Execute startSecondStage.py
#echo "Creating necessary directories with startSecondStage.py..."
#python startSecondStage.py "$experimentName"
#echo "startSecondStage.py executed successfully."

# Execute splitByGoals.py
echo "Executing splitByGoals.py..."
python splitByGoals.py "$experimentName" "$club"
echo "splitByGoals.py executed successfully."

# Execute filterByTeam.py
echo "" # Blank line
echo "Executing filterByTeam.py..."
python filterByTeam.py "$experimentName" "$club"
echo "filterByTeam.py executed successfully."

echo ""  # Blank line
echo "SecondStage completed."
echo ""  # Blank line
echo "------------------------------------------"
