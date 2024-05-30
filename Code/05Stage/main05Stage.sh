#!/bin/bash

# Retrieve the experiment name from the first argument
experimentName="$1"

# Retrieve the club for the experiment from the second argument
club="$2"

# Get the current directory path
currentDirectory=$(dirname "$0")

# Change to the directory containing startFourthStage.py
cd "$currentDirectory"

echo Executing "05Stage"...
echo "" # Blank line

# Execute generateGraph.py
echo "Generating tables from executing getTables.py"
python getTables.py "$experimentName" "$club"
echo "getTables.py executed successfully."
echo ""  # Blank line

# Execute generateGraph.py
echo "Cutting tables from executing cutTables.py"
python cutTables.py "$experimentName"
echo "cutTables.py executed successfully."
echo ""  # Blank line

echo ""  # Blank line
echo "05Satge completed."
echo ""  # Blank line
echo "------------------------------------------"
