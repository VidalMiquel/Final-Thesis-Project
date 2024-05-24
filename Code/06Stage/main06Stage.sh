#!/bin/bash

# Retrieve the experiment name from the first argument
experimentName="$1"

# Retrieve the club for the experiment from the second argument
club="$2"

# Get the current directory path
currentDirectory=$(dirname "$0")

# Change to the directory containing startFourthStage.py
cd "$currentDirectory"

echo Executing "06Stage"...
echo "" # Blank line

# Execute generateGraph.py
echo "Generating graphics from executing getGraphics.py"
#python getGraphics.py "$experimentName"
echo "getGraphics.py executed successfully."
echo ""  # Blank line


echo ""  # Blank line
echo "06Satge completed."
echo ""  # Blank line
echo "------------------------------------------"
